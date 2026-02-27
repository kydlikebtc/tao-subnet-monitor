# TAO (Bittensor) 子网注册价格调研报告

> 调研时间：2026年2月27日 | Agent Team 并行调研（6个独立 Agent）
> 链上数据：docsdemo.taostats.io API + Bittensor 主网实时查询（共 248 条注册记录）
> 市场数据：CoinLore · CoinMarketCap · CoinGecko
> ⚠️ USD 折算为估算值，基于月均价；链上 TAO 成本为精确值

---

## 一、机制说明

| 规则 | 参数 |
|------|------|
| 注册触发翻倍 | 每注册一个新子网，成本**立即×2** |
| 自然衰减周期 | 每 **38,880 区块**（≈5.5 天）无注册则**减半** |
| 最短注册间隔 | 7,200 区块（≈1 天） |
| 历史最低底线 | 100 TAO |
| 免疫期 | 注册后 864,000 区块（≈4 个月），不可被注销 |
| 注册后分配 | 1 TAO 注入子网池，其余全部销毁 |

---

## 二、三阶段演变

| 阶段 | 时间 | 机制 | 上限 |
|------|------|------|------|
| 锁定成本时代 | ～2025年2月13日前 | 费用**锁定**，注销时退还 | 32→64 个 |
| dTAO 扩张期 | 2025年2月13日～10月15日 | 费用**销毁**，不可退还 | 128 个 |
| 燃烧制成熟期 | 2025年10月15日起 | 费用**销毁**，重置 2,500 TAO | 128 个（含注销机制） |

---

## 三、TAO 历史价格参考（月均估算）

| 月份 | TAO/USD 月均价 | 关键事件 |
|------|--------------|---------|
| 2024年5月 | ~$400 | — |
| 2024年6月 | ~$255 | — |
| 2024年7月 | ~$225 | — |
| 2024年8月 | ~$215 | — |
| 2024年9月 | ~$275 | — |
| 2024年10月 | ~$450 | — |
| 2024年11月 | ~$490 | — |
| 2024年12月 | ~$558 | 年末回调 |
| 2025年1月 | ~$445 | dTAO 测试网 |
| **2025年2月** | **~$387** | **dTAO 主网上线（2月13日）** |
| 2025年3月 | ~$274 | 持续下跌 |
| 2025年4月 | ~$289 | 触底反弹 |
| 2025年5月 | ~$393 | 回暖 |
| 2025年6月 | ~$382 | 震荡 |
| **2025年10月** | **~$393** | **燃烧制上线（10月15日）** |
| **2025年12月** | **~$253** | **首次减半（12月14日）** |
| 2026年1月 | ~$210 | — |
| 2026年2月 | ~$185 | 当前 |

---

## 四、历史极值记录

| 记录 | 数据 |
|------|------|
| 全网最高成本（TAO本位） | 10,127 TAO — 2024年3月13日全网价格峰值 |
| 全网最高成本（USD本位） | **SN63：9,247.81 TAO × ~$430 ≈ $3,976,558**（2025-02-08，dTAO前5天抢注） |
| 有链上精确记录的最贵单笔 | SN24 Omega：5,146.07 TAO / $2,516,170 |
| dTAO 后最贵 | SN100：378.25 TAO / $109,314（2025-04-29） |
| dTAO 后最便宜 | SN65：37.83 TAO / $14,641（2025-02-18，dTAO后第一个） |
| 多次注册次数最多 | SN38：7次；SN47：6次 |

---

## 五、SN33-SN64 完整注册记录（2024年5月—2025年2月）

> 注：下表为每个 netuid 的**最新一次**注册记录，部分子网有多次注册历史

| netuid | 子网名称 | 区块号 | 注册日期 | 成本(TAO) | TAO/USD | 成本(USD估算) | 当前 Owner 地址 |
|--------|---------|--------|---------|----------|---------|-------------|--------------|
| 33 | ReadyAI | 2,943,950 | 2024-05-12 | 1,626.48 | ~$400 | ~$650,590 | `5HinUfk5SqBUAbkMtgdNoum3VJvwrLgdvwW5sbXA1UPYZ8uB` |
| 34 | BitMind | 3,493,948 | 2024-07-29 | 1,455.30 | ~$225 | ~$327,440 | `5DthmKBR83sUdudSfgFnsxBkTYtYTFLJUgovNfb1TSKVLiTH` |
| 35 | LogicNet | 3,037,158 | 2024-05-26 | 1,191.28 | ~$390 | ~$464,600 | `5EqZVDbW5sKXE5qB5zVaH6SQT2sud3LkmFBo2dn79NdY9RTr` |
| 36 | Web Agents | 4,871,163 | 2025-02-06 | 3,020.59 | ~$430 | ~$1,298,854 | `5DPtMdkMau8G8fGbPxdYSKCBo94oC7mDyHKMvVdNdsLVT3EF` |
| 37 | Finetuning | 3,212,175 | 2024-06-19 | 864.66 | ~$255 | ~$220,488 | `5GRBbS3aDep7cvR1NRm9Awp5HAF1o4HC7t59Y8HoheLZ6ZaP` |
| 38 | Distributed Training | 7,284,230 | 2026-01-09 | 299.57 | ~$210 | ~$62,910 | `5FFFF8AAPLTb8F95BrY9jrkxvwFXNnHY8fgg3jX4Qo7QyUAT` |
| 39 | EdgeMaxxing | 3,280,104 | 2024-06-28 | 1,366.10 | ~$250 | ~$341,525 | `5Fq9HB8RiFug83r44Focqt9Wk2UZJC76wXKqSuTVV9kXYePh` |
| 40 | Chunking | 3,372,582 | 2024-07-12 | **100.00** | ~$230 | ~$23,000 | `5F9Qvcz22Fwq4cm58o2bShiL6n8BnJmhqXB1cispBpqRfN6w` |
| 41 | Sportstensor | 3,394,182 | 2024-07-15 | 535.94 | ~$230 | ~$123,266 | `5FCSevLkofmKZRixMawp6jyyjBty1AeSCLa7N5Fv892DYkXX` |
| 42 | Real-Time Data | 3,613,591 | 2024-08-15 | 1,215.70 | ~$215 | ~$261,376 | `5Gbdb5s2WrRaFXTgMUiVNBKACe3cgSLwZNyK2Vwvjfvf6jUJ` |
| 43 | Graphite | 3,408,582 | 2024-07-17 | 1,641.31 | ~$230 | ~$377,501 | `5HjMs5JDrLH3Hknmfm1gDq7nFYAv6M7t9v3EWMctSRXJS9HC` |
| 44 | Score | 3,550,319 | 2024-08-06 | 1,514.64 | ~$215 | ~$325,647 | `5CaCekuxb9pKQyLoxh3jbkEXig8fxjkeS4AQ6UmZa12xfQ9H` |
| 45 | SWE - Rizzo | 3,633,154 | 2024-08-18 | 1,605.61 | ~$210 | ~$337,178 | `5FbcZiAHA75i2bPVrF7wa9mFaxV1eM27HR63kJtbpb8spvmf` |
| 46 | Neural3D | 3,919,107 | 2024-09-27 | 1,095.94 | ~$275 | ~$301,384 | `5Ft9E2ovN52AVMczVA3713uXmmBPczvUboB4YQpupu3aEYg7` |
| 47 | Condense AI | 7,340,355 | 2026-01-17 | 315.11 | ~$210 | ~$66,173 | `5DDKR8DVDQ4UaAprFR5gfc6WXFgk3cG6WmBpdKZ8Eah4Z6Mu` |
| 48 | Nextplace AI | 3,856,677 | 2024-09-18 | 1,308.07 | ~$270 | ~$353,179 | `5GNH5YMkcX8jEF1PukvxKafifcqz13jp18BT73jRL3AZc4Rc` |
| 49 | Hivetrain AutoML | 6,783,158 | 2025-10-31 | 287.93 | ~$393 | ~$113,157 | `5FL781vfkLNnYBUi58JnhZ3r2waHDMiehxRhzcMaMWvKDfXf` |
| 50 | Synth | 4,763,204 | 2025-01-22 | 2,628.36 | ~$445 | ~$1,169,620 | `5DxyiWpGqN5xXiczXcEGph51BcgTqcYKD5GKZqoACuc2sJkD` |
| 51 | Compute Subnet | 3,966,206 | 2024-10-04 | 1,520.86 | ~$450 | ~$684,387 | `5FqACMtcegZxxopgu1g7TgyrnyD8skurr9QDPLPhxNQzsThe` |
| 52 | Dojo | 3,989,825 | 2024-10-07 | 1,794.46 | ~$450 | ~$807,507 | `5Fv1ZvNPsEvUN6jfia6Mv3ZoefZ6KdoowGMjkPMX61QwRLXx` |
| 53 | Efficient Frontier | 4,203,869 | 2024-11-06 | 1,721.47 | ~$490 | ~$843,520 | `5F2HTUqtk9VWQwXkkUX9oFSXUkAib74qw7s3W7KyZP88AmYe` |
| 54 | WebGenieAI | 4,742,549 | 2025-01-20 | 2,048.90 | ~$445 | ~$911,761 | `5FUfruyVDoDsCty1Sh7tCmHVdpoC3XV1nUZYjhcpfe31Defk` |
| 55 | Precog | 4,703,386 | 2025-01-14 | 1,278.60 | ~$445 | ~$568,977 | `5GeWUxaFP6duJyNg8EUv6Jfcv6ZNkoERywAcbSw4FAuEMpDq` |
| 56 | Gradients | 4,312,927 | 2024-11-21 | 2,016.05 | ~$490 | ~$987,865 | `5EJ1zbdwhumTRYFx3VCGnR6SW7CJWP28tEJCo2gw1dFbVL5g` |
| 57 | Gaia | 4,343,091 | 2024-11-25 | 1,920.56 | ~$490 | ~$941,074 | `5CSBNRxeoGtkFMbdnG9H8QMXkf65b3351BSVHYMaewPSQWU2` |
| 58 | Dippy Speech | 4,367,003 | 2024-11-28 | 2,246.53 | ~$490 | ~$1,100,800 | `5FbjQefcKXjtJ1fuTPbWP6qm1xWB6zxi5cJe2qvvhjKN84kf` |
| 59 | Agent Arena | 4,401,833 | 2024-12-03 | 1,776.16 | ~$558 | ~$991,097 | `5DkPyHKTXK3eTJarh2hAL4FnkpQ5k7QivRucY8yXVN1wug4y` |
| 60 | Bitsec | 4,796,992 | 2025-01-27 | 2,173.14 | ~$445 | ~$967,047 | `5CXLwkK1Scd1uiMUrXYjJUTTPxqqyH2FTJQNLp9uXQhA9rhR` |
| 61 | Red Team | 4,457,976 | 2024-12-11 | 1,435.63 | ~$558 | ~$801,082 | `5ECEsYL82fbXx9KfTZy7G2KXSurnScciJyAVMHZjekc8jUbn` |
| 62 | AgenTao | 4,474,225 | 2024-12-13 | 2,061.28 | ~$558 | ~$1,150,194 | `5F1uxPLnv9uZqUCVHpwirnUNoybiEKuAAoJe5pv4rEHbJy1N` |
| **63** | **Quantum Simulation** | 4,885,578 | **2025-02-08** | **9,247.81** | ~$430 | **~$3,976,558** | `5CqTmNfgDchxULD1bfoz8jvj9rDYSoq76kiq98oBUUEDpWqX`† |
| 64 | Chutes | 4,531,295 | 2024-12-21 | 2,099.24 | ~$558 | ~$1,171,376 | `5FRYKhbmfXPDoHdUUDMx27E3HuMvAzwjzFMMq3rNurUhAyS9` |

> † SN63 注册者（`5Gmp...`）与当前链上 Owner（`5CqT...`）不同，已发生 ownership 转移

---

## 六、dTAO 后注册记录（SN65-SN128，全部为销毁制）

### SN65-SN100（2025年2月18日—4月29日）

| netuid | 区块号 | 注册日期 | 成本(TAO) | TAO/USD | 成本(USD) | 当前 Owner 地址 |
|--------|--------|---------|----------|---------|----------|--------------|
| 65 | 4,950,813 | 2025-02-18 | **37.83** | $387 | $14,641 | `5GxEEHxLWpvcAGghL8LG7xNjrxZk4SEPW1VT43hGPZ2TP9mZ` |
| 66 | 4,958,013 | 2025-02-19 | 65.23 | $387 | $25,245 | `5E9oJhMQd7qagGD4HNMbRQzaQVDvLjVr76U5wvg4Poxv5pvj` |
| 67 | 4,965,213 | 2025-02-20 | 114.16 | $387 | $44,178 | `5HEAv3TU1yNei4GwiTsxfmDCDW9pMCKLeDVky9iaVJfYiVeY` |
| 68 | 4,972,413 | 2025-02-21 | 199.77 | $387 | $77,312 | `5EcdJLAeYoxM3Tsf5VZ3NQPenPku218gqnjSoo3iJNy4V12V` |
| 69 | 4,979,613 | 2025-02-22 | 349.60 | $387 | $135,296 | `5EsorPyFCP7TaNz3QrNvDvr8ZDVtG9hfzNEfGeAVG9wbFi2B` |
| 70 | 5,008,428 | 2025-02-26 | 349.42 | $387 | $135,227 | `5DkyQv5rqhXSzzXmwX4pL8FDU4q8xHJdX2jAwjBD3FkLmKt6` |
| 71 | 5,048,438 | 2025-03-03 | 213.42 | $274 | $58,477 | `5DwHzMhBXPGPSSxnPzp3J8Y12UyYmU17nppQ8oHum6yrRjSk` |
| 72 | 5,064,327 | 2025-03-05 | 191.36 | $274 | $52,432 | `5HTYVBxrF2WbVN8RBtFxAkBGuHJxjgLd9Sze5gxH4KC6GLCv` |
| 73 | 5,076,911 | 2025-03-07 | 215.49 | $274 | $59,043 | `5EWdfGjSKJ9jP6GH427s6Nj4jjhUTxaenExHH433eFi8wJ3J` |
| 74 | 5,086,205 | 2025-03-08 | 291.89 | $274 | $79,978 | `5D1VXeeSdrfyrBdMe4SNwKnRsmzrjXES9dhx6kQkCHhJUPvS` |
| 75 | 5,102,795 | 2025-03-11 | 247.51 | $274 | $67,817 | `5DAQpczEK4vzBn1waHkC4BZGqGPZ1dwPxKVsj36JDofHAw3a` |
| 76 | 5,114,649 | 2025-03-12 | 291.26 | $274 | $79,805 | `5FFNhWd881QTWuuiDgkqW4vgiWFDW1QYqPwRB9MZUkH7cMUP` |
| 77 | 5,128,460 | 2025-03-14 | 303.17 | $274 | $83,070 | `5GxxsUeYRyJSJKCuPeG1jZZiCummHJttmTNsfgDRSfxVnhGi` |
| 78 | 5,143,608 | 2025-03-16 | 287.43 | $274 | $78,755 | `5FxyfeqQi5DL88jwyz3pPZFww3WUbKHJT6Vdhe3kx6ML8V6R` |
| 79 | 5,173,967 | 2025-03-21 | 254.95 | $274 | $69,857 | `5Fxp7QBG81X7PLdMkAe1RLCvqqfQSw9rJC5ppEQs9FP8qez9` |
| 80 | 5,188,340 | 2025-03-23 | 255.43 | $274 | $69,988 | `5ERJCUPWkgEmVDFCcdwMgaBbtEqGmzZnhdqNRcf3W29JsJJs` |
| 81 | 5,203,057 | 2025-03-25 | 249.81 | $274 | $68,447 | `5Ckv5w2PLg9yeWA62cS6XYNUtorKQAeJLmaUgZ1sKMttEadb` |
| 82 | 5,216,791 | 2025-03-27 | 261.36 | $274 | $71,613 | `5CQGGDxtZrtpMJGpjXqEP3pkwmqfwwYs1knmYnQGjGs8MMgS` |
| 83 | 5,231,190 | 2025-03-29 | 261.38 | $274 | $71,618 | `5DqEjRLyNN8k3WbEXhA36tyGG4YpWyPEcVSTa47XxspNHhc3` |
| 84 | 5,248,864 | 2025-03-31 | 201.96 | $274 | $55,336 | `5FBwsAvvKjhe7bGSdtVSAaxm7huJAcWFZRb9WRpJJmrVUvoB` |
| 85 | 5,258,781 | 2025-04-01 | 264.82 | $289 | $76,533 | `5GTPBjA4uXhuQ51SJB7Jd55JwY6dKEnbnjCrsSSEXy3MN63z` |
| 86 | 5,275,445 | 2025-04-04 | 223.19 | $289 | $64,502 | `5ERnAHRQjTrLwtTcBgKqDu7j5YSL23eetTtnFgqb5jaKLqrq` |
| 87 | 5,292,605 | 2025-04-06 | 180.41 | $289 | $52,139 | `5GquyFXCVX4dAB1GFNSfZemYZm43H8KWa1BSTjV9UKeSYt2x` |
| 88 | 5,299,805 | 2025-04-07 | 270.61 | $289 | $78,206 | `5FhMsGJS7WYdwBzcgsTWxEtY7UCYLZdmBVLcNPmCxr3ppiKS` |
| 89 | 5,313,364 | 2025-04-09 | 286.42 | $289 | $82,775 | `5Dc5NmEUptDeMLrxDSvg8kfCToxJkiF47apAYSVTycAVvDN4` |
| 90 | 5,328,705 | 2025-04-11 | 267.70 | $289 | $77,366 | `5CqrdkU4FuH8LdUjkq4YQFJbQiK1Bmf9q4fVpFuhrxGcGwbW` |
| 91 | 5,342,193 | 2025-04-13 | 284.66 | $289 | $82,266 | `5E7dez1zSF5L5NPSTYBrRRP8K5r7kKGNuwnrtzspHNP9n3EA` |
| 92 | 5,356,404 | 2025-04-15 | 288.39 | $289 | $83,346 | `5Ck9Wu6bQ923pPgb7KWfszAWo6uraNryxw88JLfmRx7xUBTT` |
| 93 | 5,370,681 | 2025-04-17 | 290.86 | $289 | $84,058 | `5FLfN276taTF6Ud62soChQhPNbtF2EPK4dr3pJB9oTsTpUvr` |
| 94 | 5,386,070 | 2025-04-19 | 270.88 | $289 | $78,285 | `5EZRCK9op9piMhQvHqrEL1SNQU8ENU8s9aqGnRKNsUxmPYP2` |
| 95 | 5,403,674 | 2025-04-22 | 210.61 | $289 | $60,867 | `5D5UhUuc6cC47CXUBHyBkpDBrdeyeL6bpWGAreZgNm5WTyrg` |
| 96 | 5,410,917 | 2025-04-23 | 315.28 | $289 | $91,115 | `5D7bAeb7ybS72vpxsH9Wrutein45ZDp7a5Vi4uogsZ5BZnzJ` |
| 97 | 5,432,489 | 2025-04-26 | 158.27 | $289 | $45,739 | `5EXSiTySWQiuzowhogXzfCr4Xn45CW3oMELWGTxFEfQCTy86` |
| 98 | 5,445,992 | 2025-04-27 | 168.11 | $289 | $48,585 | `5Dd9Q6yueRkH1fLTHa2xdEEPoMQiqenWKRMUtZKPTuvjRL3w` |
| 99 | 5,453,192 | 2025-04-28 | 252.17 | $289 | $72,876 | `5EADbTnNp5Wfs2G4G3LiR1nUVHgtCbkTAkHZqRgFpDUJMYMb` |
| **100** | 5,460,392 | 2025-04-29 | **378.25** | $289 | **$109,314** | `5FX6kmhYwTYRFaZjxEo7k9DaG8qRmqrJtLTMGRgnfjRcXiWU` |

### SN101-SN128（2025年5月2日—6月25日）

| netuid | 区块号 | 注册日期 | 成本(TAO) | TAO/USD | 成本(USD) | 当前 Owner 地址 |
|--------|--------|---------|----------|---------|----------|--------------|
| 101 | 5,481,350 | 2025-05-02 | 206.00 | $393 | $80,960 | `5H8dNvi1jZRe1dcYN2FdknWKxfGx6u1o9pYm5zRMCZyy2Ex3` |
| 102 | 5,499,703 | 2025-05-05 | 149.45 | $393 | $58,733 | `5DrE31CZ9bWLXu7ND5WpbV1ERqXf48vWaKKjvWda5JWTqfiW` |
| 103 | 5,515,448 | 2025-05-07 | 135.49 | $393 | $53,246 | `5CcRAHrH5CjNhAMDU6iE2UaaDUx7EyZskUeXfkgn1pTULbh7` |
| 104 | 5,528,520 | 2025-05-09 | 147.98 | $393 | $58,156 | `5HBb3F1bmDzdwQ5WTweXUvnKETTzu6aWNAH811vrLkvSdQAn` |
| 105 | 5,545,447 | 2025-05-11 | 122.01 | $393 | $47,951 | `5G3ic2pAzVu1gZmeUQfKGox3P8TetJw87asvyAdkb2o8aCCX` |
| 106 | 5,558,480 | 2025-05-13 | 133.59 | $393 | $52,502 | `5E5Ctr2D9SjvLwNn45UNhBpjuQ7QWuinMqpAXY1ueRfJr5PT` |
| 107 | 5,565,706 | 2025-05-14 | 200.15 | $393 | $78,658 | `5DA2vLrSXZxnT9G4Yrywx1Fpi4RXwMH1Ah7r8DTTWS7UZZBM` |
| 108 | 5,586,824 | 2025-05-17 | 106.78 | $393 | $41,965 | `5HDuqw9fkqG3xdm1yZA8dfKeLBnZhg138xiMwnYQdBeLfytT` |
| 109 | 5,598,862 | 2025-05-19 | 124.29 | $393 | $48,845 | `5GW6xj5wUpLBz7jCNp38FzkdS6DfeFdUTuvUjcn6uKH5krsn` |
| 110 | 5,606,062 | 2025-05-20 | 186.43 | $393 | $73,267 | `5HKuDWu8y69RhSKaKenrby8rmWjTupyf4rNKjxn44saxcjkd` |
| 111 | 5,615,562 | 2025-05-22 | 249.87 | $393 | $98,198 | `5HKeYGvjWXKfB6VVtG4SBpRa87TyKYzc6n8pJKacStFwWyfZ` |
| 112 | 5,633,022 | 2025-05-25 | 196.78 | $393 | $77,334 | `5D7Rf7HbeE7ti49fyLg3TM3F96uWFUwzYBo9SkzBpAUTQMhM` |
| 113 | 5,651,055 | 2025-05-27 | 147.13 | $393 | $57,824 | `5FZZ32NJHT1szHX1Y4X4L6uZ2iU4gFZQCoYSB65k8MDasvPU` |
| 114 | 5,671,631 | 2025-05-30 | 84.03 | $393 | $33,025 | `5FHrQMjzzAhmL5zS9ys87ZrGCwG3vsVT9hXAUWZQ8SNdRqig` |
| 115 | 5,683,635 | 2025-06-01 | 98.01 | $382 | $37,439 | `5EkNnrTjnMYaj4x1gNxAnJne9UvKgfU6NZNjhm6XFWMstbdG` |
| 116 | 5,699,219 | 2025-06-03 | 89.95 | $382 | $34,361 | `5GgjJXbcDyiGenKGfPrPhRxJ7p91EdC22fcAAF4ccbATgu6H` |
| 117 | 5,710,859 | 2025-06-05 | 107.19 | $382 | $40,947 | `5CY4LpcYpCbwT7KnLZS4fdHZzd8ixBC8jeqevt64gfyo6nZe` |
| 118 | 5,724,794 | 2025-06-06 | 110.65 | $382 | $42,269 | `5CdS9RLYMZzgHUCmQagpqzhVkJFoNxasLyaCMA72wY3GvGG5` |
| 119 | 5,740,660 | 2025-06-09 | 99.39 | $382 | $37,966 | `5GbLENPLG8Takn1puaz5HorPmrFtDT7i2PojiJsqutbaGwWu` |
| 120 | 5,749,344 | 2025-06-10 | 138.84 | $382 | $53,035 | `5Fc3ZZQAYB3SPXKcFnd1WJeyQvArSZZeB6LU1rb7zvQ6XvDh` |
| 121 | 5,766,528 | 2025-06-12 | 112.00 | $382 | $42,783 | `5CXGaDJsffVeBK4CDhBNMVK6MH7fHbL7AbnjzZ8XP6QzFLWm` |
| 122 | 5,778,578 | 2025-06-14 | 130.27 | $382 | $49,764 | `5H6fAdf7QsrZpLKyydA1pM9sxTK7qJx4S4jUgg6YMHr4Xzqs` |
| 123 | 5,794,330 | 2025-06-16 | 118.04 | $382 | $45,093 | `5HVuEdEGMYisecwjkWC7dKDPEzgs9cECdsdCQagfPRVf6FxZ` |
| 124 | 5,813,454 | 2025-06-19 | 79.32 | $382 | $30,301 | `5CB6igqihC83cq9jTujmgeGutQfzRrJjCQzcDizmYDYXvcVC` |
| 125 | 5,834,408 | 2025-06-22 | 43.22 | $382 | $16,510 | `5DTzv2rL6YGQjCDNiWQJz2nE23fK1mDccH9eQimgiieyL3C4` |
| 126 | 5,841,630 | 2025-06-23 | 64.76 | $382 | $24,738 | `5DqrUa2z6E9taJdY8FGiPCrtCswsEjHjPbVo5xcTw2GqvKZm` |
| 127 | 5,848,837 | 2025-06-24 | 97.11 | $382 | $37,095 | `5FU4uxAdrZsaWaezWwXEK93MwPX5gw2566BQK2WwrGUudfSH` |
| **128** | 5,856,038 | **2025-06-25** | 145.65 | $382 | $55,639 | `5GgMeLFN4YssT6f9i9pZpRmczt8GYDsCZ1nYPiGRcTPWn3AA` |

---

## 七、SN0-SN32 早期子网（当前链上 Owner 地址）

| netuid | 子网名称 | 当前 Owner 地址（链上实时）|
|--------|---------|----------------------|
| 0 | Root | `5C4hrfjw9DjXZTzV3MwzrrAr9P1MJhSrvWGWqi1eSuyUpnhM` |
| 1 | Apex | `5HCFWvRqzSHWRPecN7q8J6c7aKQnrCZTMHstPv39xL1wgDHh` |
| 2 | Omron | `5EcYQ3W77ndrmMWdvVQusoFqY8doxfP3U2zrh7xZQiaz7avY` |
| 3 | Templar | `5G26HqQg8M6hfw9q84gM3udYHHymThmswRKgSGtwdcduBSos` |
| 4 | Targon | `5CXGPMnq9RCCLUEvp9G2iUuabw69TSFM155UVS1S4Zmusaxv` |
| 5 | Open Kaito | `5GurNtB3yQFCh6CSmfH7LrYJDsvzup4diHZiaYtKe274nrMX` |
| 6 | Infinite Games | `5CfSg4e23Z3aTXvc2XZie8ZE1xkqRPoyVRFdWUuyyjGxJrMA` |
| 7 | Subvortex | `5GER8KoYArh9hgcbqqEHmifGfisoobHnmNfr4d22DptgbXLn` |
| 8 | Proprietary Trading | `5F6tnxzAAxbhaWRmeUmB63JEM3VXBNSmqb3AwYJVDStQjw8y` |
| 9 | Pretraining | `5FsbubeciqtB5Nik3umL2iD4fG8FcC9GbT9nHJfXMj4mJJZ9` |
| 10 | Sturdy | `5GbcimKjp17QPUoS568DBSMNqV2pmDetBf3xyC15vh4bTFE1` |
| 11 | Dippy Roleplay | `5D2Jhtbnm7iAdKfjRk6DisXBnr1MEsYat8kXqaPNrVqJP3uE` |
| 12 | Horde | `5ELzhHvgUqmnAYs74vFWjMMehXNeHkRtkreAa3g8QQS96PCp` |
| 13 | Data Universe | `5HBswBt1A9Ahx6U76abXXGd7VmabmCNBGhSK2vrP71GSxtgZ` |
| 14 | VectorStore | `5CKhH8nKAhXLmqxwaXzFtVFgxqwwnyckXG8qLpmGtzVJH9Ri` |
| 15 | De-Val | `5GE9r7GMtDyfbsp5RKr2V8M5PaYJ7pgF9KBu6oBcRiYjZPCc` |
| 16 | BitAds | `5CqRkhQUEgkQ4nBB4SCKnc9AzKPs9VLYv28erjeXPqQYVt9V` |
| 17 | Three Gen | `5E7a4a7QETrNjoZ2SbVSJMaavrQeyTEaHgjBPDUDxBKjUaMZ` |
| 18 | Cortex.t | `5DHwWLjtpwnZQUQKKXE2N5Gdy2N8PpqhgjLUuzgSB7yuGZkF` |
| 19 | Nineteen | `5FWh37LfVV5LE9dZA91STzbtebh6vxYa3MH71c621sYafo1L` |
| 20 | BitAgent | `5FuzgvtfbZWdKSRxyYVPAPYNaNnf9cMnpT7phL3s2T3Kkrzo` |
| 21 | Omega Any-to-any | `5GjbJe6Li9L1pwdhKBjSnB75MTDdUAKr57ShLaPqzcszVTE3` |
| 22 | Desearch | `5DFuaMasyQtPhXcsuoYEyJmCVSRtzKxsTKFTA4SrpcGXBxJn` |
| 23 | SocialTensor | `5D5abJCLFGapLepwBrao9mg92oFQZLUCRLumUfWCKnqNZEf2` |
| 24 | Omega | `5ERaDLWTyUciYPkP8oXadbnHtetyhEmHiLopK8K5HPU1NEKZ` |
| 25 | Protein Folding | `5F6aRdsBHajN2NhZHBTB6ibBFu7YuZZEWruWzB8x6B6GiZ4D` |
| 26 | — | `5GsfAD4a3KXYKx2TF9UcajcW6C85Bw5vZsCTmrFep7RgMjcm` |
| 27 | NI Compute | `5HWcFNDtZcpbrq8Qkd92EvgWp6q5dCycHkT1aBQtWsmLT8fB` |
| 28 | LOL | `5GKYVYof1CbEuNcnBSa2wXx3rs5StYYVBPdg8C5CQ8MifCBc` |
| 29 | Coldint | `5HHHHHzgLnYRvnKkHd45cRUDMHXTSwx7MjUzxBrKbY4JfZWn` |
| 30 | Bettensor | `5HDpyLSn4GzxGQJidqn3YHRQkrjUmpiRzXFjZfjLZpV6Auw2` |
| 31 | NAS Chain | `5FUKS95wgvtqXKMR6bmnB9pmX7NbFzK1cH1JqkXyoYWD2EmU` |
| 32 | It's AI | `5DWgkCSvq4brWSNLDU9FBgTk1ZpAQ2y6t3ky97CvEVuS9Qad` |

> ⚠️ 注意：约 50 个子网的链上当前 Owner 与最初注册者不同（已发生 ownership 转移），上表均为**链上实时数据**（2026-02-27查询）

---

## 八、统计摘要

| 指标 | SN33-SN64 | SN65-SN128 |
|------|-----------|-----------|
| 注册时间段 | 2024年5月—2025年2月 | 2025年2月18日—6月25日 |
| 机制 | 锁定（可退还） | **销毁（永久）** |
| 最低成本(TAO) | 100 TAO (SN40) | 37.83 TAO (SN65) |
| 最高成本(TAO) | 9,247.81 TAO (SN63) | 378.25 TAO (SN100) |
| 最高成本(USD) | ~$3,976,558 (SN63) | ~$135,296 (SN69/SN70) |
| 注册速度 | 不定期（1周—3个月） | 约**每 2 天 1 个** |

---

## 九、链上数据 API

```bash
# 演示端点（无需 API Key）
GET https://docsdemo.taostats.io/api/http/api/subnet/registration/v1?limit=200&page=1

# 返回字段示例
{
  "block_number": 4885578,
  "timestamp": "2025-02-08T...",
  "netuid": 63,
  "registration_cost": 9247810000000,  // RAO ÷ 1e9 = TAO
  "owner": { "ss58": "5Gmp..." }
}

# 查询当前注册成本
btcli subnet burn-cost --network finney
```

---

## 十、数据来源

| 来源 | URL |
|------|-----|
| Taostats 链上 API（演示） | https://docsdemo.taostats.io/api/http/api/subnet/registration/v1 |
| Taostats API 文档 | https://docs.taostats.io/reference |
| taostat/subnets-infos | https://github.com/taostat/subnets-infos/blob/main/subnets.json |
| CoinLore TAO 历史价格 | https://www.coinlore.com/coin/bittensor/historical-data |
| tao.bot 注册成本快照 | https://x.com/taodotbot/status/1859987116287254875 |
| DL News AI 热潮报道 | https://www.dlnews.com/articles/defi/ai-hype-in-crypto-pushes-bittensor-subnet-tao-fees/ |
| OTF 燃烧机制公告 | https://x.com/opentensor/status/1978637998913990935 |
| Dynamic TAO FAQ | https://docs.learnbittensor.org/dynamic-tao/dtao-faq |
| Omega Labs SN24 GitHub | https://github.com/omegalabsinc/omegalabs-bittensor-subnet |
