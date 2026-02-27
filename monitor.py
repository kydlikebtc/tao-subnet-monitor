"""
TAO 子网注册价格监控后端服务

功能概述：
- 定时轮询 Taostats API 获取子网注册费用
- 检测新子网上线
- 价格历史记录持久化到 data/history.json
- WebSocket 实时推送价格更新
- 阈值告警，触发 macOS 通知
- 获取 TAO/USD 实时价格（CoinGecko）
- 从 Taostats 加载3年历史数据（缓存到 data/historical_cache.json）
- 提供 K 线 OHLC 数据接口（5m/1h/4h/1d/1w 颗粒度）
"""

import asyncio
import json
import logging
import os
import subprocess
import sys
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import httpx
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# ---------------------------------------------------------------------------
# 日志配置
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("tao-monitor")

# ---------------------------------------------------------------------------
# 路径常量
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.json"
HISTORY_PATH = BASE_DIR / "data" / "history.json"
HISTORICAL_CACHE_PATH = BASE_DIR / "data" / "historical_cache.json"
STATIC_DIR = BASE_DIR / "static"

# RAO 到 TAO 的转换系数
RAO_PER_TAO = 1_000_000_000

# Taostats API 端点
STATS_API_URL = "https://api.taostats.io/api/stats/latest/v1"
SUBNETS_API_URL = "https://api.taostats.io/api/subnet/latest/v1"
TAOSTATS_HISTORY_URL = "https://api.taostats.io/api/stats/history/v1"

# CoinGecko TAO/USD 价格
COINGECKO_PRICE_URL = (
    "https://api.coingecko.com/api/v3/simple/price?ids=bittensor&vs_currencies=usd"
)

# K 线颗粒度（秒）
GRANULARITY_SECONDS: dict[str, int] = {
    "5m": 300,
    "1h": 3600,
    "4h": 14400,
    "1d": 86400,
    "1w": 604800,
}


# ---------------------------------------------------------------------------
# 数据模型
# ---------------------------------------------------------------------------
class AlertThreshold(BaseModel):
    price_tao: float
    type: str  # "below" | "above"
    triggered: bool = False
    label: str = ""


class AppConfig(BaseModel):
    api_key: str = ""
    alert_thresholds: list[AlertThreshold] = []
    poll_interval_seconds: int = 30
    notification_enabled: bool = True


class PriceRecord(BaseModel):
    timestamp: str
    price_rao: int
    price_tao: float
    price_usd: float = 0.0
    subnet_count: int


class SubnetEvent(BaseModel):
    timestamp: str
    subnet_id: int
    event: str


class HistoryData(BaseModel):
    price_history: list[PriceRecord] = []
    new_subnet_events: list[SubnetEvent] = []


# ---------------------------------------------------------------------------
# 配置与历史数据 I/O（须在 MonitorState 前定义）
# ---------------------------------------------------------------------------
def _load_config() -> AppConfig:
    """从 config.json 加载配置，文件不存在则使用默认值"""
    if CONFIG_PATH.exists():
        try:
            raw = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            logger.info("配置文件已加载: %s", CONFIG_PATH)
            return AppConfig(**raw)
        except Exception:
            logger.exception("加载配置文件失败，使用默认配置")
    return AppConfig()


def _save_config(config: AppConfig) -> None:
    """将配置写入 config.json"""
    CONFIG_PATH.write_text(
        json.dumps(config.model_dump(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    logger.info("配置已保存: %s", CONFIG_PATH)


def _load_history() -> HistoryData:
    """从 data/history.json 加载历史数据"""
    if HISTORY_PATH.exists():
        try:
            raw = json.loads(HISTORY_PATH.read_text(encoding="utf-8"))
            logger.info("历史数据已加载，共 %d 条价格记录", len(raw.get("price_history", [])))
            return HistoryData(**raw)
        except Exception:
            logger.exception("加载历史数据失败，使用空数据")
    return HistoryData()


def _save_history(history: HistoryData) -> None:
    """将历史数据写入 data/history.json"""
    HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    HISTORY_PATH.write_text(
        json.dumps(history.model_dump(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _load_historical_cache() -> list[dict]:
    """加载 Taostats 历史数据缓存（可能有3年的数据）"""
    if HISTORICAL_CACHE_PATH.exists():
        try:
            raw = json.loads(HISTORICAL_CACHE_PATH.read_text(encoding="utf-8"))
            if isinstance(raw, list):
                logger.info("历史缓存已加载: %d 条记录", len(raw))
                return raw
        except Exception:
            logger.exception("加载历史缓存失败")
    return []


def _save_historical_cache(records: list[dict]) -> None:
    """将 Taostats 历史数据保存到缓存文件"""
    HISTORICAL_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    HISTORICAL_CACHE_PATH.write_text(
        json.dumps(records, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    logger.info("历史缓存已保存: %d 条记录", len(records))


# ---------------------------------------------------------------------------
# 全局状态
# ---------------------------------------------------------------------------
class MonitorState:
    """运行时状态容器，避免可变全局变量"""

    def __init__(self) -> None:
        self.config: AppConfig = _load_config()
        self.history: HistoryData = _load_history()
        self.historical_cache: list[dict] = _load_historical_cache()
        self.current_price_rao: int = 0
        self.current_price_tao: float = 0.0
        self.current_price_usd: float = 0.0
        self.current_subnet_count: int = 0
        self.known_subnet_ids: set[int] = set()
        self.subnets_list: list[dict[str, Any]] = []
        self.ws_clients: set[WebSocket] = set()
        self.poll_task: asyncio.Task | None = None
        self.last_usd_fetch: datetime | None = None
        self.last_history_fetch: datetime | None = None


state = MonitorState()


# ---------------------------------------------------------------------------
# macOS 通知
# ---------------------------------------------------------------------------
def _send_macos_notification(title: str, message: str) -> None:
    """通过 osascript 发送 macOS 桌面通知"""
    if not state.config.notification_enabled:
        logger.debug("通知已禁用，跳过: %s", message)
        return
    try:
        escaped_msg = message.replace('"', '\\"')
        escaped_title = title.replace('"', '\\"')
        script = (
            f'display notification "{escaped_msg}" '
            f'with title "{escaped_title}" sound name "default"'
        )
        subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            timeout=5,
        )
        logger.info("macOS 通知已发送: [%s] %s", title, message)
    except Exception:
        logger.exception("发送 macOS 通知失败")


# ---------------------------------------------------------------------------
# Taostats API 请求
# ---------------------------------------------------------------------------
def _build_headers() -> dict[str, str]:
    """构造 API 请求头，含可选的 API Key"""
    headers: dict[str, str] = {"Accept": "application/json"}
    if state.config.api_key:
        headers["Authorization"] = state.config.api_key
    return headers


async def _fetch_stats(client: httpx.AsyncClient) -> dict[str, Any] | None:
    """获取 Taostats 最新统计数据"""
    try:
        resp = await client.get(STATS_API_URL, headers=_build_headers(), timeout=15)
        resp.raise_for_status()
        data = resp.json()
        logger.debug("Stats API 原始响应: %s", json.dumps(data, ensure_ascii=False)[:500])
        return data
    except httpx.HTTPStatusError as exc:
        logger.error("Stats API 请求失败 (HTTP %d): %s", exc.response.status_code, exc)
    except Exception:
        logger.exception("Stats API 请求异常")
    return None


async def _fetch_subnets(client: httpx.AsyncClient) -> list[dict[str, Any]] | None:
    """获取子网列表"""
    try:
        resp = await client.get(SUBNETS_API_URL, headers=_build_headers(), timeout=15)
        resp.raise_for_status()
        data = resp.json()
        logger.debug("Subnets API 原始响应长度: %d", len(json.dumps(data)))
        return data
    except httpx.HTTPStatusError as exc:
        logger.error("Subnets API 请求失败 (HTTP %d): %s", exc.response.status_code, exc)
    except Exception:
        logger.exception("Subnets API 请求异常")
    return None


async def _fetch_tao_usd_price(client: httpx.AsyncClient) -> float | None:
    """从 CoinGecko 获取 TAO/USD 实时价格"""
    try:
        resp = await client.get(COINGECKO_PRICE_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        price = data.get("bittensor", {}).get("usd")
        if price is not None:
            logger.info("TAO/USD 价格: $%.4f", price)
            return float(price)
        logger.warning("CoinGecko 响应中未找到 bittensor 价格: %s", data)
    except Exception:
        logger.warning("获取 TAO/USD 价格失败")
    return None


async def _fetch_taostats_history_all(client: httpx.AsyncClient) -> list[dict]:
    """
    分页获取 Taostats 全部历史统计数据。
    每页最多200条，自动翻页直到获取完毕。
    返回按时间升序排列的记录列表。
    """
    all_records: list[dict] = []
    page = 1

    while True:
        try:
            resp = await client.get(
                TAOSTATS_HISTORY_URL,
                headers=_build_headers(),
                params={"limit": 200, "page": page},
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()

            records = data.get("data", [])
            pagination = data.get("pagination", {})
            total_pages = pagination.get("total_pages", 1)

            normalized = []
            for r in records:
                ts = r.get("timestamp", "")
                cost_rao = r.get("subnet_registration_cost")
                if ts and cost_rao:
                    # 标准化时间戳格式（去除毫秒，统一为 +00:00）
                    ts_clean = ts.rstrip("Z").split(".")[0] + "+00:00"
                    normalized.append({
                        "timestamp": ts_clean,
                        "price_rao": int(cost_rao),
                        "price_tao": round(int(cost_rao) / RAO_PER_TAO, 6),
                    })

            all_records.extend(normalized)
            logger.info(
                "历史数据加载: 第 %d/%d 页，本页 %d 条，累计 %d 条",
                page, total_pages, len(normalized), len(all_records),
            )

            if page >= total_pages:
                break
            page += 1

        except Exception:
            logger.exception("获取历史数据第 %d 页失败，停止翻页", page)
            break

    # 按时间戳升序排列
    all_records.sort(key=lambda r: r.get("timestamp", ""))
    logger.info("历史数据加载完成，共 %d 条记录", len(all_records))
    return all_records


# ---------------------------------------------------------------------------
# 价格解析
# ---------------------------------------------------------------------------
def _parse_stats(data: dict[str, Any]) -> tuple[int, float, int]:
    """
    从 Stats API 响应中提取注册费用和子网数。

    返回: (price_rao, price_tao, subnet_count)
    """
    # Taostats 响应可能是 {"data": [...]} 或直接是 dict
    record = data
    if isinstance(data, dict) and "data" in data:
        inner = data["data"]
        if isinstance(inner, list) and len(inner) > 0:
            record = inner[0]
        elif isinstance(inner, dict):
            record = inner

    price_rao = int(record.get("subnet_registration_cost", 0))
    price_tao = round(price_rao / RAO_PER_TAO, 4)
    subnet_count = int(record.get("subnets", 0))

    logger.info(
        "解析结果 — 注册费: %s RAO (%.4f TAO), 子网数: %d",
        f"{price_rao:,}",
        price_tao,
        subnet_count,
    )
    return price_rao, price_tao, subnet_count


def _parse_subnets(data: Any) -> list[dict[str, Any]]:
    """从 Subnets API 响应中提取子网列表"""
    if isinstance(data, dict) and "data" in data:
        subnets = data["data"]
    elif isinstance(data, list):
        subnets = data
    else:
        subnets = []

    if not isinstance(subnets, list):
        logger.warning("子网数据格式异常: %s", type(subnets))
        return []

    return subnets


# ---------------------------------------------------------------------------
# OHLC K 线聚合
# ---------------------------------------------------------------------------
def _build_ohlc(records: list[dict], granularity_seconds: int) -> list[dict]:
    """
    将价格记录列表聚合为 OHLC 蜡烛图数据。

    records: [{"timestamp": "ISO8601", "price_tao": float}, ...]
    granularity_seconds: 每根蜡烛的时间跨度（秒）
    返回: [{"time": unix_ts, "open": float, "high": float, "low": float, "close": float}]
    """
    if not records:
        return []

    buckets: dict[int, list[float]] = {}

    for r in records:
        ts_str = r.get("timestamp", "")
        if not ts_str:
            continue
        try:
            # 处理不同的时间戳格式
            ts_str_clean = ts_str.rstrip("Z").split(".")[0]
            if "+" not in ts_str_clean and len(ts_str_clean) == 19:
                ts_str_clean += "+00:00"
            ts = datetime.fromisoformat(ts_str_clean)
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
            bucket = int(ts.timestamp()) // granularity_seconds * granularity_seconds
            price = float(r.get("price_tao", 0))
            if price > 0:
                buckets.setdefault(bucket, []).append(price)
        except Exception:
            continue

    candles = []
    prev_close: float | None = None

    for ts, prices in sorted(buckets.items()):
        close = prices[-1]
        # 用前一蜡烛的收盘价作为本蜡烛的开盘价（标准日K处理方式）
        # 当每个时间区间只有1个数据点时（如每日快照），这能使蜡烛
        # 显示方向（涨/跌）而不是扁平线
        open_price = prev_close if prev_close is not None else prices[0]
        high = max(max(prices), open_price)
        low = min(min(prices), open_price)

        candles.append({
            "time": ts,
            "open": round(open_price, 6),
            "high": round(high, 6),
            "low": round(low, 6),
            "close": round(close, 6),
        })
        prev_close = close

    return candles


# ---------------------------------------------------------------------------
# 阈值告警检查
# ---------------------------------------------------------------------------
def _check_thresholds(price_tao: float) -> None:
    """检查当前价格是否触发告警阈值"""
    changed = False
    for threshold in state.config.alert_thresholds:
        crossed = (
            (threshold.type == "below" and price_tao <= threshold.price_tao)
            or (threshold.type == "above" and price_tao >= threshold.price_tao)
        )

        if crossed and not threshold.triggered:
            threshold.triggered = True
            changed = True
            direction = "低于" if threshold.type == "below" else "高于"
            msg = (
                f"注册费 {price_tao:.4f} TAO 已{direction} "
                f"{threshold.price_tao} TAO ({threshold.label})"
            )
            logger.warning("阈值告警触发: %s", msg)
            _send_macos_notification("TAO 子网价格告警", msg)

        elif not crossed and threshold.triggered:
            # 价格回到阈值范围外，重置触发状态以便下次再次告警
            threshold.triggered = False
            changed = True
            logger.info("阈值已重置: %s (%.4f TAO)", threshold.label, threshold.price_tao)

    if changed:
        _save_config(state.config)


# ---------------------------------------------------------------------------
# WebSocket 广播
# ---------------------------------------------------------------------------
async def _broadcast_ws(message: dict[str, Any]) -> None:
    """向所有已连接的 WebSocket 客户端广播消息"""
    if not state.ws_clients:
        return

    payload = json.dumps(message, ensure_ascii=False)
    disconnected: set[WebSocket] = set()

    for ws in state.ws_clients:
        try:
            await ws.send_text(payload)
        except Exception:
            disconnected.add(ws)

    if disconnected:
        state.ws_clients -= disconnected
        logger.info("清理已断开的 WebSocket 客户端: %d 个", len(disconnected))


# ---------------------------------------------------------------------------
# 新子网检测
# ---------------------------------------------------------------------------
def _detect_new_subnets(subnets: list[dict[str, Any]]) -> list[int]:
    """检测新上线的子网，返回新子网 ID 列表"""
    current_ids: set[int] = set()
    for s in subnets:
        sid = s.get("netuid") or s.get("subnet_id") or s.get("id")
        if sid is not None:
            current_ids.add(int(sid))

    if not state.known_subnet_ids:
        # 首次运行，初始化已知子网集合
        state.known_subnet_ids = current_ids
        logger.info("初始化已知子网 ID 集合，共 %d 个", len(current_ids))
        return []

    new_ids = sorted(current_ids - state.known_subnet_ids)
    if new_ids:
        logger.info("检测到 %d 个新子网: %s", len(new_ids), new_ids)
        state.known_subnet_ids = current_ids
    return new_ids


# ---------------------------------------------------------------------------
# 历史数据裁剪
# ---------------------------------------------------------------------------
def _trim_history(history: HistoryData, max_hours: int = 168) -> None:
    """裁剪超过 max_hours 小时的历史记录（保留7天本地实时数据）"""
    cutoff = datetime.now(timezone.utc) - timedelta(hours=max_hours)
    cutoff_str = cutoff.isoformat()

    before = len(history.price_history)
    history.price_history = [
        r for r in history.price_history if r.timestamp >= cutoff_str
    ]
    trimmed = before - len(history.price_history)
    if trimmed > 0:
        logger.info("裁剪了 %d 条过期价格记录 (>%dh)", trimmed, max_hours)

    before_events = len(history.new_subnet_events)
    history.new_subnet_events = [
        e for e in history.new_subnet_events if e.timestamp >= cutoff_str
    ]
    trimmed_events = before_events - len(history.new_subnet_events)
    if trimmed_events > 0:
        logger.info("裁剪了 %d 条过期子网事件 (>%dh)", trimmed_events, max_hours)


# ---------------------------------------------------------------------------
# 轮询主循环
# ---------------------------------------------------------------------------
async def _poll_loop() -> None:
    """后台轮询任务：定时拉取 API 数据并处理"""
    logger.info(
        "轮询任务已启动，间隔 %d 秒",
        state.config.poll_interval_seconds,
    )

    async with httpx.AsyncClient() as client:
        while True:
            try:
                await _poll_once(client)
            except asyncio.CancelledError:
                logger.info("轮询任务被取消")
                raise
            except Exception:
                logger.exception("轮询过程中发生未预期的异常")

            await asyncio.sleep(state.config.poll_interval_seconds)


async def _poll_once(client: httpx.AsyncClient) -> None:
    """执行一次完整的轮询周期"""
    now = datetime.now(timezone.utc).isoformat()

    # ---- 每 5 分钟刷新一次 TAO/USD 价格 ----
    need_usd = (
        state.last_usd_fetch is None
        or (datetime.now(timezone.utc) - state.last_usd_fetch).total_seconds() > 300
    )
    if need_usd:
        usd_price = await _fetch_tao_usd_price(client)
        if usd_price is not None:
            state.current_price_usd = usd_price
            state.last_usd_fetch = datetime.now(timezone.utc)

    # ---- 每 6 小时刷新一次 Taostats 历史缓存 ----
    need_history = (
        not state.historical_cache
        or state.last_history_fetch is None
        or (datetime.now(timezone.utc) - state.last_history_fetch).total_seconds() > 21600
    )
    if need_history:
        logger.info("开始刷新 Taostats 历史数据缓存（约需30秒）...")
        new_history = await _fetch_taostats_history_all(client)
        if new_history:
            state.historical_cache = new_history
            state.last_history_fetch = datetime.now(timezone.utc)
            _save_historical_cache(new_history)

    # 并发请求 Stats 和 Subnets API
    stats_data, subnets_data = await asyncio.gather(
        _fetch_stats(client),
        _fetch_subnets(client),
    )

    # ---- 处理 Stats 数据 ----
    if stats_data is not None:
        price_rao, price_tao, subnet_count = _parse_stats(stats_data)
        state.current_price_rao = price_rao
        state.current_price_tao = price_tao
        state.current_subnet_count = subnet_count

        price_usd = round(price_tao * state.current_price_usd, 4) if state.current_price_usd else 0.0

        # 记录价格历史
        record = PriceRecord(
            timestamp=now,
            price_rao=price_rao,
            price_tao=price_tao,
            price_usd=price_usd,
            subnet_count=subnet_count,
        )
        state.history.price_history.append(record)

        # 检查阈值告警
        _check_thresholds(price_tao)

        # 广播 WebSocket 更新
        await _broadcast_ws({
            "type": "price_update",
            "timestamp": now,
            "price_rao": price_rao,
            "price_tao": price_tao,
            "price_usd": price_usd,
            "tao_usd_rate": state.current_price_usd,
            "subnet_count": subnet_count,
        })

    # ---- 处理 Subnets 数据 ----
    if subnets_data is not None:
        subnets = _parse_subnets(subnets_data)
        state.subnets_list = subnets

        new_ids = _detect_new_subnets(subnets)
        for sid in new_ids:
            event = SubnetEvent(
                timestamp=now,
                subnet_id=sid,
                event="new_subnet_detected",
            )
            state.history.new_subnet_events.append(event)
            _send_macos_notification(
                "TAO 新子网上线",
                f"检测到新子网 #{sid} 已上线",
            )
            await _broadcast_ws({
                "type": "new_subnet",
                "timestamp": now,
                "subnet_id": sid,
            })

    # 裁剪并持久化历史数据
    _trim_history(state.history)
    _save_history(state.history)


# ---------------------------------------------------------------------------
# FastAPI 应用
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(_app: FastAPI):
    """应用生命周期管理：启动轮询任务，关闭时取消"""
    logger.info("TAO 子网监控服务启动中...")
    state.poll_task = asyncio.create_task(_poll_loop())
    yield
    logger.info("TAO 子网监控服务关闭中...")
    if state.poll_task:
        state.poll_task.cancel()
        try:
            await state.poll_task
        except asyncio.CancelledError:
            pass
    logger.info("服务已停止")


app = FastAPI(
    title="TAO 子网注册价格监控",
    description="实时监控 Bittensor 子网注册费用",
    version="2.0.0",
    lifespan=lifespan,
)


# ---------------------------------------------------------------------------
# API 端点
# ---------------------------------------------------------------------------
@app.get("/api/current")
async def get_current():
    """获取当前注册费用、子网数量和 USD 价格"""
    price_usd = round(state.current_price_tao * state.current_price_usd, 4) if state.current_price_usd else 0.0
    return {
        "price_rao": state.current_price_rao,
        "price_tao": state.current_price_tao,
        "price_usd": price_usd,
        "tao_usd_rate": state.current_price_usd,
        "subnet_count": state.current_subnet_count,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/api/history")
async def get_history(hours: int = 24):
    """获取价格历史记录（默认最近 24 小时）"""
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    cutoff_str = cutoff.isoformat()

    filtered = [
        r.model_dump() for r in state.history.price_history
        if r.timestamp >= cutoff_str
    ]

    return {
        "hours": hours,
        "count": len(filtered),
        "price_history": filtered,
        "new_subnet_events": [
            e.model_dump() for e in state.history.new_subnet_events
            if e.timestamp >= cutoff_str
        ],
    }


@app.get("/api/kline")
async def get_kline(granularity: str = "1d", days: int = 365):
    """
    获取 K 线 OHLC 数据。

    granularity: "5m" | "1h" | "4h" | "1d" | "1w"
    days: 返回最近多少天的数据（默认365天）
    """
    gran_secs = GRANULARITY_SECONDS.get(granularity, 86400)
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    cutoff_str = cutoff.isoformat()

    all_records: list[dict] = []

    # 1. 加入 Taostats 历史缓存数据
    for r in state.historical_cache:
        if r.get("timestamp", "") >= cutoff_str:
            all_records.append(r)

    # 2. 加入本地实时历史（监控期间累积的高频数据）
    for r in state.history.price_history:
        if r.timestamp >= cutoff_str:
            all_records.append({
                "timestamp": r.timestamp,
                "price_rao": r.price_rao,
                "price_tao": r.price_tao,
            })

    # 构建 OHLC 蜡烛数据
    candles = _build_ohlc(all_records, gran_secs)

    return {
        "granularity": granularity,
        "gran_secs": gran_secs,
        "days": days,
        "count": len(candles),
        "candles": candles,
    }


@app.get("/api/tao-usd")
async def get_tao_usd():
    """获取当前 TAO/USD 汇率"""
    return {
        "tao_usd": state.current_price_usd,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/api/config")
async def get_config():
    """获取当前告警配置"""
    return state.config.model_dump()


@app.post("/api/config")
async def save_config(new_config: AppConfig):
    """保存告警配置"""
    state.config = new_config
    _save_config(new_config)
    logger.info("配置已通过 API 更新")
    return {"success": True, "config": new_config.model_dump()}


@app.get("/api/subnets")
async def get_subnets():
    """获取当前子网列表"""
    return {
        "count": len(state.subnets_list),
        "subnets": state.subnets_list,
    }


@app.get("/api/subnet-registrations")
async def get_subnet_registrations():
    """
    获取子网注册历史记录，包含 TAO 和 USD 成本。
    按注册时间降序返回（最新在前）。
    USD 成本基于当前 TAO/USD 汇率估算。
    """
    current_tao_usd = state.current_price_usd
    registrations = []

    for subnet in state.subnets_list:
        cost_rao = subnet.get("registration_cost", 0)
        if not cost_rao or int(cost_rao) <= 0:
            continue

        netuid = subnet.get("netuid")
        cost_tao = round(int(cost_rao) / RAO_PER_TAO, 6)
        cost_usd = round(cost_tao * current_tao_usd, 2) if current_tao_usd else 0.0

        registrations.append({
            "netuid": netuid,
            "name": subnet.get("name") or f"SN{netuid}",
            "registration_timestamp": subnet.get("registration_timestamp", ""),
            "registration_cost_rao": int(cost_rao),
            "registration_cost_tao": cost_tao,
            "registration_cost_usd": cost_usd,
        })

    # 按注册时间降序排序（最新的子网在最前）
    registrations.sort(
        key=lambda r: r.get("registration_timestamp", ""),
        reverse=True,
    )
    logger.info("子网注册历史: 返回 %d 条记录（USD 汇率: $%.2f）", len(registrations), current_tao_usd)

    return {
        "count": len(registrations),
        "tao_usd_rate": current_tao_usd,
        "registrations": registrations,
    }


# ---------------------------------------------------------------------------
# WebSocket 端点
# ---------------------------------------------------------------------------
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    """WebSocket 连接端点，用于实时推送价格更新"""
    await ws.accept()
    state.ws_clients.add(ws)
    client_host = ws.client.host if ws.client else "unknown"
    logger.info("WebSocket 客户端已连接: %s (当前共 %d 个)", client_host, len(state.ws_clients))

    # 连接后立即推送当前价格
    try:
        price_usd = round(state.current_price_tao * state.current_price_usd, 4) if state.current_price_usd else 0.0
        await ws.send_json({
            "type": "price_update",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "price_rao": state.current_price_rao,
            "price_tao": state.current_price_tao,
            "price_usd": price_usd,
            "tao_usd_rate": state.current_price_usd,
            "subnet_count": state.current_subnet_count,
        })
    except Exception:
        logger.exception("WebSocket 初始推送失败")

    try:
        while True:
            # 保持连接，接收客户端消息（心跳等）
            data = await ws.receive_text()
            logger.debug("收到 WebSocket 消息: %s", data)
    except WebSocketDisconnect:
        logger.info("WebSocket 客户端断开: %s", client_host)
    except Exception:
        logger.debug("WebSocket 连接异常关闭: %s", client_host)
    finally:
        state.ws_clients.discard(ws)


# ---------------------------------------------------------------------------
# 前端静态文件服务
# ---------------------------------------------------------------------------
@app.get("/")
async def serve_index():
    """提供前端页面"""
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return JSONResponse(
        {"message": "TAO 子网监控服务运行中", "docs": "/docs"},
        status_code=200,
    )


# 挂载静态资源目录（如果存在）
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# ---------------------------------------------------------------------------
# 入口
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8888))
    logger.info("启动服务器，端口: %d", port)
    uvicorn.run(
        "monitor:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info",
    )
