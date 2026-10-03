#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VLESS По Грибы • CLI Controller
Commands: check, serve, export, update
"""

import os
import sys
import time
import argparse
import asyncio
from typing import Optional

# Ensure UTF-8 output on Windows terminal
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from core.aggregator import ConfigAggregator
from core.checker import ProxyChecker
from core.subscription import SubscriptionGenerator
from server import start_server, BASE_DIR, DATA_DIR


def run_check_cli(limit: Optional[int] = None, concurrency: int = 80, timeout: float = 2.5):
    print("\n" + "=" * 65)
    print(" 🍄 СКАНИРОВАНИЕ И ЧЕКЕР СЕРВЕРОВ VLESS ПО ГРИБЫ")
    print("=" * 65)

    aggregator = ConfigAggregator(DATA_DIR)
    checker = ProxyChecker(concurrency=concurrency, timeout=timeout, data_dir=DATA_DIR)
    generator = SubscriptionGenerator()

    # 1. Aggregate
    nodes = aggregator.aggregate(fetch_all_sources=True, max_servers=limit)
    print(f"\n[*] Найдено серверов для проверки: {len(nodes)}")

    # 2. Check
    start_t = time.time()
    last_print = 0

    def progress(completed, total, alive_count, latest_node):
        nonlocal last_print
        now = time.time()
        if now - last_print > 0.4 or completed == total:
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

    print(f"\n\n[+] Сканирование завершено за {elapsed} сек!")
    print(f"    • Всего проверено:        {len(nodes)}")
    print(f"    • Рабочих (Alive):         {len(alive_nodes)} ({round(len(alive_nodes)/len(nodes)*100, 1) if nodes else 0}%)")
    print(f"    • Белые списки (Обход):   {len(wl_nodes)}")

    if alive_nodes:
        fastest = alive_nodes[:5]
        print("\n  Топ-5 самых быстрых серверов:")
        for idx, n in enumerate(fastest):
            print(f"   {idx+1}. {n.get_clean_remark(idx+1)} -> {n.host}:{n.port} ({n.latency_ms} ms)")

    # 3. Export
    export_dir = os.path.join(BASE_DIR, "export")
    os.makedirs(export_dir, exist_ok=True)

    with open(os.path.join(export_dir, "sub_all_base64.txt"), "w", encoding="utf-8") as f:
        f.write(generator.generate_base64(alive_nodes))

    with open(os.path.join(export_dir, "sub_whitelist_base64.txt"), "w", encoding="utf-8") as f:
        f.write(generator.generate_base64(alive_nodes, whitelist_only=True))

    with open(os.path.join(export_dir, "clash_meta_failover.yaml"), "w", encoding="utf-8") as f:
        f.write(generator.generate_clash_meta(alive_nodes))

    with open(os.path.join(export_dir, "singbox_failover.json"), "w", encoding="utf-8") as f:
        f.write(generator.generate_singbox(alive_nodes))

    print(f"\n[+] Готовые файлы подписок экспортированы в: {export_dir}")
    print("    - sub_all_base64.txt        (Incy / Happ / v2rayNG)")
    print("    - sub_whitelist_base64.txt  (Только Белые списки)")
    print("    - clash_meta_failover.yaml  (Clash Meta Auto-Failover)")
    print("    - singbox_failover.json     (Sing-box / Hiddify Url-test)")


def run_continuous_update(interval_minutes: int = 45):
    print(f"[*] Запуск фонового обновления каждые {interval_minutes} минут...")
    while True:
        try:
            run_check_cli()
        except Exception as e:
            print(f"[!] Ошибка во время проверки: {e}")
        print(f"\n[*] Следующая проверка через {interval_minutes} мин. Нажмите Ctrl+C для выхода.")
        time.sleep(interval_minutes * 60)


def main():
    parser = argparse.ArgumentParser(description="🍄 VLESS По Грибы • Smart Hub & Auto-Failover Checker")
    subparsers = parser.add_subparsers(dest="command", help="Команда для запуска")

    # Command: serve
    serve_parser = subparsers.add_parser("serve", help="Запустить веб-панель и сервер подписок")
    serve_parser.add_argument("--host", default="0.0.0.0", help="Хост для привязки (по умолчанию 0.0.0.0)")
    serve_parser.add_argument("--port", type=int, default=8088, help="Порт сервера (по умолчанию 8088)")
    serve_parser.add_argument("--no-auto-check", action="store_true", help="Не запускать автопроверку на старте")

    # Command: check
    check_parser = subparsers.add_parser("check", help="Запустить сканирование и чекер серверов")
    check_parser.add_argument("--limit", type=int, default=None, help="Лимит количества серверов для теста")
    check_parser.add_argument("--concurrency", type=int, default=80, help="Параллельных потоков (по умолчанию 80)")
    check_parser.add_argument("--timeout", type=float, default=2.5, help="Таймаут проверки сокета в секундах")

    # Command: update
    update_parser = subparsers.add_parser("update", help="Запустить циклическое фоновое обновление")
    update_parser.add_argument("--interval", type=int, default=45, help="Интервал обновления в минутах")

    args = parser.parse_args()

    if args.command == "check":
        run_check_cli(limit=args.limit, concurrency=args.concurrency, timeout=args.timeout)
    elif args.command == "update":
        run_continuous_update(interval_minutes=args.interval)
    else:
        # Default: start server
        host = getattr(args, "host", "0.0.0.0")
        port = getattr(args, "port", 8088)
        no_check = getattr(args, "no_auto_check", False)
        start_server(host=host, port=port, auto_check_on_start=not no_check)


if __name__ == "__main__":
    main()
