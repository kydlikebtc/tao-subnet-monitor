#!/bin/bash
# TAO 子网注册价格监控 - 启动脚本

cd "$(dirname "$0")"

echo "=== TAO 子网监控服务 ==="

# 创建虚拟环境（如不存在）
if [ ! -d "venv" ]; then
  echo "创建虚拟环境..."
  python3 -m venv venv
fi

source venv/bin/activate

echo "安装依赖..."
pip install -r requirements.txt -q

echo "启动服务，访问 http://localhost:8888"
python3 monitor.py
