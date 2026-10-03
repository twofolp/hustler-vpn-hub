#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automated Checker & Cloudflare Sync Engine
Runs health checks on all proxy sources and uploads the alive verified pool
directly to your Cloudflare Worker: https://vless-hub.danilkaponda.workers.dev
"""

import os
import sys
import time
import json
import asyncio
import urllib.request

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from core.aggregator import ConfigAggregator
from core.checker import ProxyChecker
from core.subscription import SubscriptionGenerator
from build_worker import CLOUDFLARE_ACCOUNT_ID, CLOUDFLARE_API_TOKEN, WORKER_NAME, generate_worker_js, deploy_to_cloudflare

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
WORKER_SYNC_URL = "https://vless-hub.danilkaponda.workers.dev/api/sync"
SYNC_SECRET = "hustler_secret_2026"


def run_full_sync(limit: int = 500, concurrency: int = 100, timeout: float = 2.5):
    print("=" * 65)
    print(" 🚀 СКАНИРОВАНИЕ И СИНХРОНИЗАЦИЯ С CLOUDFLARE WORKERS")
    print("=" * 65)

    aggregator = ConfigAggregator(DATA_DIR)
    checker = ProxyChecker(concurrency=concurrency, timeout=timeout, data_dir=DATA_DIR)

    # 1. Aggregate from all sources
    print("[*] Сбор конфигураций со всех источников (VLESS-PO-GRIBI + впн.txt + отсортировать надо.txt)...")
    nodes = aggregator.aggregate(fetch_all_sources=True, max_servers=limit)
    print(f"[+] Всего отобрано для проверки: {len(nodes)} серверов")

    # 2. Check all concurrently
    print(f"[*] Сканирование в {concurrency} параллельных потоков...")
    start_t = time.time()
    last_print = 0

    def progress(completed, total, alive_count, latest_node):
        nonlocal last_print
        now = time.time()
        if now - last_print > 0.3 or completed == total:
            last_print = now
            pct = int((completed / total) * 100) if total > 0 else 0
            bar = "█" * (pct // 5) + "░" * (20 - (pct // 5))
            sys.stdout.write(f"\r  [{bar}] {pct}% ({completed}/{total}) | Живых: {alive_count}")
            sys.stdout.flush()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        alive_nodes = loop.run_until_complete(
            checker.check_all(nodes, progress_callback=progress)
        )
    finally:
        loop.close()

    elapsed = round(time.time() - start_t, 1)
    wl_nodes = [n for n in alive_nodes if n.is_whitelist]
    gaming_nodes = [n for n in alive_nodes if 0 < n.latency_ms <= 85]

    print(f"\n\n[+] Сканирование завершено за {elapsed} сек!")
    print(f"    • Живых узлов:           {len(alive_nodes)}")
    print(f"    • Белые списки (Обход): {len(wl_nodes)}")
    print(f"    • Игровые узлы (<85ms):  {len(gaming_nodes)}")

    if not alive_nodes:
        print("[!] Нет доступных серверов для синхронизации.")
        return

    # 3. Synchronize with Cloudflare Worker
    servers_dict = [n.to_dict() for n in alive_nodes]
    print("\n[*] Отправка свежей базы на Cloudflare Worker...")

    payload = json.dumps({
        "secret": SYNC_SECRET,
        "servers": servers_dict
    }).encode("utf-8")

    req = urllib.request.Request(
        WORKER_SYNC_URL,
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            res_data = json.loads(resp.read().decode("utf-8"))
            print(f"[+] Успешно синхронизировано с Cloudflare! База на воркере обновлена: {res_data}")
    except Exception as e:
        print(f"[*] Прямая синхронизация через API Worker ({e}), пересобираем и развертываем воркер напрямую через Cloudflare API...")
        script = generate_worker_js(servers_dict)
        deploy_to_cloudflare(script)

    print("\n" + "=" * 65)
    print(" ✅ ВСЕ СЕРВЕРА ОБНОВЛЕНЫ И ГОТОВЫ К РАБОТЕ!")
    print("=" * 65)
    print(" 🌐 Веб-панель:            https://vless-hub.danilkaponda.workers.dev")
    print(" 📱 Подписка для Incy:     https://vless-hub.danilkaponda.workers.dev/sub/incy")
    print(" 🚀 Подписка для Happ:     https://vless-hub.danilkaponda.workers.dev/sub/happ")
    print(" 🛡️ Белые списки:          https://vless-hub.danilkaponda.workers.dev/sub/whitelist")
    print(" 🎮 Игровые сервера:       https://vless-hub.danilkaponda.workers.dev/sub/gaming")
    print(" 🌍 Топ-3 по странам:      https://vless-hub.danilkaponda.workers.dev/sub/top3")
    print(" 🤖 Telegram Бот:          https://t.me/hustler_vpn_robot")
    print("=" * 65)


if __name__ == "__main__":
    limit = 400
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        limit = int(sys.argv[1])
    run_full_sync(limit=limit)
