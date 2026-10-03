#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smart Hub HTTP Server & Multi-Subscription API
Provides REST API, Web UI, and dynamic subscription endpoints.
Zero external dependencies required (Pure Python standard library).
"""

import os
import sys
import json
import time
import urllib.parse
import threading
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from typing import List, Dict, Any, Optional

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

from core.parser import ProxyNode
from core.aggregator import ConfigAggregator
from core.checker import ProxyChecker
from core.subscription import SubscriptionGenerator
from core.proxy_relay import SmartProxyManager

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
DATA_DIR = os.path.join(BASE_DIR, "data")


class AppState:
    def __init__(self):
        self.aggregator = ConfigAggregator(DATA_DIR)
        self.checker = ProxyChecker(concurrency=80, timeout=2.5, data_dir=DATA_DIR)
        self.generator = SubscriptionGenerator()
        self.proxy_manager = SmartProxyManager(self.checker)

        self.all_nodes: List[ProxyNode] = []
        self.alive_nodes: List[ProxyNode] = []
        self.is_checking: bool = False
        self.check_progress = {
            "completed": 0,
            "total": 0,
            "alive_count": 0,
            "percent": 0,
            "is_running": False
        }
        self.lock = threading.Lock()

        # Load initial cached data
        self._load_initial_cache()

    def _load_initial_cache(self):
        cached_alive = self.checker.load_cached_alive()
        if cached_alive:
            self.alive_nodes = cached_alive
            self.proxy_manager.update_pools(self.alive_nodes)
            print(f"[+] Загружено {len(self.alive_nodes)} проверенных серверов из кэша")
        else:
            print("[*] Кэш пуст. Запустите первую проверку через веб-интерфейс или CLI")

    def trigger_check_async(self, max_servers: Optional[int] = None):
        with self.lock:
            if self.is_checking:
                return
            self.is_checking = True
            self.check_progress = {
                "completed": 0,
                "total": 0,
                "alive_count": 0,
                "percent": 0,
                "is_running": True
            }

        thread = threading.Thread(target=self._run_check_worker, args=(max_servers,), daemon=True)
        thread.start()

    def _run_check_worker(self, max_servers: Optional[int]):
        try:
            print("[*] Запуск сбора серверов из VLESS-PO-GRIBI...")
            nodes = self.aggregator.aggregate(fetch_all_sources=True, max_servers=max_servers)
            with self.lock:
                self.all_nodes = nodes
                self.check_progress["total"] = len(nodes)

            print(f"[*] Начало асинхронной проверки {len(nodes)} серверов...")

            def on_progress(completed, total, alive_count, latest_node):
                with self.lock:
                    percent = int((completed / total) * 100) if total > 0 else 0
                    self.check_progress.update({
                        "completed": completed,
                        "total": total,
                        "alive_count": alive_count,
                        "percent": percent,
                        "is_running": True
                    })

            # Run asyncio loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                alive = loop.run_until_complete(
                    self.checker.check_all(nodes, progress_callback=on_progress)
                )
            finally:
                loop.close()

            with self.lock:
                self.alive_nodes = alive
                self.proxy_manager.update_pools(self.alive_nodes)
                self.check_progress["is_running"] = False
                self.is_checking = False

            print(f"[+] Проверка завершена! Найдено живых: {len(alive)}")
        except Exception as e:
            print(f"[!] Ошибка во время проверки: {e}")
            with self.lock:
                self.is_checking = False
                self.check_progress["is_running"] = False


state = AppState()


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True


class RequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Clean logging
        pass

    def send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, User-Agent")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip("/")
        if not path:
            path = "/"

        # 1. Static Files & Root
        if path == "/" or path == "/index.html":
            self.serve_file(os.path.join(STATIC_DIR, "index.html"), "text/html; charset=utf-8")
            return
        elif path.startswith("/static/"):
            rel_path = path[8:]
            file_path = os.path.join(STATIC_DIR, rel_path)
            content_type = self.get_content_type(file_path)
            self.serve_file(file_path, content_type)
            return

        # 2. REST API Endpoints
        if path == "/api/stats":
            self.handle_api_stats()
            return
        elif path == "/api/check/progress":
            self.handle_api_progress()
            return
        elif path == "/api/failover/status":
            self.handle_api_failover()
            return

        # 3. Subscriptions
        # A. Plain / Base64 for Incy, Happ, v2rayNG, Throne, v2rayN
        if path in ["/sub", "/sub/all", "/sub/incy"]:
            self.serve_subscription(whitelist_only=False, is_base64=True)
            return
        elif path == "/sub/happ":
            self.serve_subscription(whitelist_only=False, is_base64=True)
            return
        elif path == "/sub/raw":
            self.serve_subscription(whitelist_only=False, is_base64=False)
            return
        elif path == "/sub/whitelist":
            self.serve_subscription(whitelist_only=True, is_base64=True)
            return
        elif path == "/sub/whitelist/raw":
            self.serve_subscription(whitelist_only=True, is_base64=False)
            return
        elif path == "/sub/gaming":
            self.serve_subscription(whitelist_only=False, gaming_only=True, is_base64=True)
            return
        elif path == "/sub/top3":
            self.serve_subscription(whitelist_only=False, top_per_country=3, is_base64=True)
            return
        elif path.startswith("/sub/country/"):
            cc = path.split("/sub/country/")[1].strip().upper()
            self.serve_subscription(whitelist_only=False, country_code=cc, is_base64=True)
            return

        # Direct Best Single Keys for Incy / Happ
        if path == "/best":
            self.serve_best_key(whitelist_only=False, gaming_only=False)
            return
        elif path == "/best-whitelist":
            self.serve_best_key(whitelist_only=True, gaming_only=False)
            return
        elif path == "/best-gaming":
            self.serve_best_key(whitelist_only=False, gaming_only=True)
            return

        # B. Clash Meta / Mihomo (YAML with Auto-Failover)
        if path in ["/clash", "/clash/meta"]:
            self.serve_clash()
            return

        # C. Sing-box / Hiddify (JSON with Auto-Failover)
        if path in ["/singbox", "/hiddify"]:
            self.serve_singbox()
            return

        # 404
        self.send_error(404, "Not Found")

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/api/check":
            state.trigger_check_async()
            self.send_response(200)
            self.send_cors_headers()
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "started"}).encode("utf-8"))
            return

        self.send_error(404, "Not Found")

    def handle_api_stats(self):
        with state.lock:
            alive = state.alive_nodes
            is_chk = state.is_checking
            total_scanned = len(state.all_nodes) if state.all_nodes else len(alive)
            wl_count = sum(1 for n in alive if n.is_whitelist)

            data = {
                "total_scanned": total_scanned,
                "alive_count": len(alive),
                "whitelist_count": wl_count,
                "is_checking": is_chk,
                "servers": [n.to_dict() for n in alive[:200]]
            }

        self.send_response(200)
        self.send_cors_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def handle_api_progress(self):
        with state.lock:
            data = dict(state.check_progress)

        self.send_response(200)
        self.send_cors_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def handle_api_failover(self):
        status = state.proxy_manager.get_status()
        self.send_response(200)
        self.send_cors_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(status, ensure_ascii=False).encode("utf-8"))

    def serve_subscription(
        self,
        whitelist_only: bool = False,
        country_code: Optional[str] = None,
        top_per_country: Optional[int] = None,
        gaming_only: bool = False,
        is_base64: bool = True
    ):
        with state.lock:
            nodes = list(state.alive_nodes)

        if is_base64:
            content = state.generator.generate_base64(
                nodes,
                whitelist_only=whitelist_only,
                country_code=country_code,
                top_per_country=top_per_country,
                gaming_only=gaming_only
            )
            c_type = "text/plain; charset=utf-8"
        else:
            content = state.generator.generate_plain(
                nodes,
                whitelist_only=whitelist_only,
                country_code=country_code,
                top_per_country=top_per_country,
                gaming_only=gaming_only
            )
            c_type = "text/plain; charset=utf-8"

        self.send_response(200)
        self.send_cors_headers()
        self.send_header("Content-Type", c_type)
        self.send_header("Subscription-Userinfo", f"upload=0; download=0; total=1073741824000; expire=0")
        self.send_header("profile-update-interval", "6")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))

    def serve_best_key(self, whitelist_only: bool = False, gaming_only: bool = False):
        with state.lock:
            nodes = list(state.alive_nodes)

        key = state.generator.get_best_server(nodes, whitelist_only=whitelist_only, gaming_only=gaming_only)
        if not key:
            key = "No servers available"

        self.send_response(200)
        self.send_cors_headers()
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(key.encode("utf-8"))

    def serve_clash(self):
        with state.lock:
            nodes = list(state.alive_nodes)

        yaml_content = state.generator.generate_clash_meta(nodes)
        self.send_response(200)
        self.send_cors_headers()
        self.send_header("Content-Type", "application/yaml; charset=utf-8")
        self.send_header("Content-Disposition", 'attachment; filename="clash_meta_failover.yaml"')
        self.send_header("profile-update-interval", "6")
        self.end_headers()
        self.wfile.write(yaml_content.encode("utf-8"))

    def serve_singbox(self):
        with state.lock:
            nodes = list(state.alive_nodes)

        json_content = state.generator.generate_singbox(nodes)
        self.send_response(200)
        self.send_cors_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Disposition", 'attachment; filename="singbox_failover.json"')
        self.end_headers()
        self.wfile.write(json_content.encode("utf-8"))

    def serve_file(self, filepath: str, content_type: str):
        if not os.path.exists(filepath):
            self.send_error(404, "File Not Found")
            return

        try:
            with open(filepath, "rb") as f:
                data = f.read()
            self.send_response(200)
            self.send_cors_headers()
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        except Exception as e:
            self.send_error(500, f"Error reading file: {e}")

    def get_content_type(self, filepath: str) -> str:
        ext = os.path.splitext(filepath)[1].lower()
        types = {
            ".html": "text/html; charset=utf-8",
            ".css": "text/css; charset=utf-8",
            ".js": "application/javascript; charset=utf-8",
            ".json": "application/json; charset=utf-8",
            ".png": "image/png",
            ".svg": "image/svg+xml",
            ".ico": "image/x-icon",
            ".txt": "text/plain; charset=utf-8"
        }
        return types.get(ext, "application/octet-stream")


def start_server(host: str = "0.0.0.0", port: int = 8088, auto_check_on_start: bool = False):
    server = ThreadedHTTPServer((host, port), RequestHandler)
    local_url = f"http://localhost:{port}"
    print("=" * 65)
    print(" 🍄 VLESS По Грибы • Smart Hub & Subscription Server")
    print("=" * 65)
    print(f" [✓] Веб-панель доступна по адресу:  {local_url}")
    print(f" [✓] Универсальная подписка:         {local_url}/sub")
    print(f" [✓] Только Белые списки (Обход):    {local_url}/sub/whitelist")
    print(f" [✓] Clash Meta (Auto-Failover):     {local_url}/clash")
    print(f" [✓] Sing-Box / Hiddify (Url-Test):  {local_url}/singbox")
    print("=" * 65)

    if auto_check_on_start or len(state.alive_nodes) == 0:
        print("[*] Запуск автоматической первой проверки серверов в фоне...")
        state.trigger_check_async()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Остановка сервера...")
        server.server_close()


if __name__ == "__main__":
    start_server()
