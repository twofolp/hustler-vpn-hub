#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
High-Performance Asynchronous Proxy Checker
Tests TCP connectivity, TLS handshake, latency (ms), and resolves Country / GeoIP.
"""

import os
import sys
import time
import json
import ssl
import socket
import asyncio
from typing import List, Dict, Any, Optional, Callable

from core.parser import ProxyNode
from core.geoip import GeoIPResolver

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


class ProxyChecker:
    def __init__(
        self,
        concurrency: int = 80,
        timeout: float = 2.5,
        data_dir: str = DATA_DIR
    ):
        self.concurrency = concurrency
        self.timeout = timeout
        self.data_dir = data_dir
        self.geoip = GeoIPResolver()
        os.makedirs(self.data_dir, exist_ok=True)
        self.alive_file = os.path.join(self.data_dir, "alive_servers.json")
        self.alive_txt = os.path.join(self.data_dir, "alive_servers.txt")

    async def check_single(self, node: ProxyNode, semaphore: asyncio.Semaphore) -> ProxyNode:
        """
        Checks a single proxy node for genuine TLS/Reality connectivity.
        Filters out fake CDN IPs, unencrypted/unsupported protocols, and nodes that fail TLS handshake.
        """
        async with semaphore:
            # 1. Reject fake Cloudflare CDN IPs (causes N/A in Incy)
            if node.is_cloudflare_cdn_ip():
                node.is_alive = False
                node.latency_ms = -1
                return node

            # 2. Incy & Happ strictly require VLESS Reality or TLS
            if node.protocol != "vless" or node.security not in ("reality", "tls"):
                node.is_alive = False
                node.latency_ms = -1
                return node

            # 3. Strict Reality validation (keys must be valid)
            if node.security == "reality":
                if not node.pbk or len(node.pbk) < 30 or not node.uuid or len(node.uuid) < 30:
                    node.is_alive = False
                    node.latency_ms = -1
                    return node

            # 4. Check country from remark first if not already set
            country_info = self.geoip.detect_from_remark(node.remark)
            if country_info:
                node.country_code, node.country_flag, node.country_name = country_info

            # 5. REAL TLS/Reality Handshake Test
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            ctx.set_alpn_protocols(["h2", "http/1.1"])

            sni = node.sni or node.host

            t0 = time.perf_counter()
            try:
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(node.host, node.port, ssl=ctx, server_hostname=sni),
                    timeout=self.timeout
                )
                latency = int((time.perf_counter() - t0) * 1000)

                # Close connection gracefully
                writer.close()
                try:
                    await writer.wait_closed()
                except Exception:
                    pass

                node.is_alive = True
                node.latency_ms = latency
            except (asyncio.TimeoutError, OSError, ssl.SSLError, Exception):
                node.is_alive = False
                node.latency_ms = -1

            return node

    async def check_all(
        self,
        nodes: List[ProxyNode],
        progress_callback: Optional[Callable[[int, int, int, ProxyNode], None]] = None
    ) -> List[ProxyNode]:
        """
        Runs concurrent checks on all provided proxy nodes.
        Filters out 100% of dead nodes (no more N/A in Incy).
        Sorts:
        1. Foreign servers (non-RU, non-whitelist) with lowest ping FIRST.
        2. Regular RU servers in the middle.
        3. Whitelist bypass servers (VK, Gosuslugi, etc.) strictly at the BOTTOM.
        """
        semaphore = asyncio.Semaphore(self.concurrency)
        total = len(nodes)
        completed = 0
        alive_nodes: List[ProxyNode] = []

        async def worker(node: ProxyNode):
            nonlocal completed
            res = await self.check_single(node, semaphore)
            completed += 1
            if res.is_alive:
                alive_nodes.append(res)
            if progress_callback:
                progress_callback(completed, total, len(alive_nodes), res)
            return res

        # Run all tasks concurrently
        tasks = [asyncio.create_task(worker(n)) for n in nodes]
        await asyncio.gather(*tasks, return_exceptions=True)

        # Batch resolve GeoIP for alive nodes missing country
        missing_country_ips = [
            n.host for n in alive_nodes
            if n.country_code in ["OTHER", "XX", "", None]
        ]
        if missing_country_ips:
            resolved_map = self.geoip.resolve_batch_ips(missing_country_ips)
            for n in alive_nodes:
                if n.host in resolved_map:
                    inf = resolved_map[n.host]
                    n.country_code = inf.get("code", "OTHER")
                    n.country_flag = inf.get("flag", "🌐")
                    n.country_name = inf.get("name_ru", n.country_code)

        # Fallback for any node that still has OTHER: never leave unknown
        for n in alive_nodes:
            if n.country_code in ["OTHER", "XX", "", None] or n.country_name in ["Неизвестно", "OTHER", ""]:
                if n.is_whitelist or ".ru" in (n.sni + n.host).lower():
                    n.country_code = "RU"
                    n.country_flag = "🇷🇺"
                    n.country_name = "Россия"
                elif ".de" in (n.sni + n.host).lower():
                    n.country_code = "DE"
                    n.country_flag = "🇩🇪"
                    n.country_name = "Германия"
                elif ".nl" in (n.sni + n.host).lower():
                    n.country_code = "NL"
                    n.country_flag = "🇳🇱"
                    n.country_name = "Нидерланды"
                else:
                    n.country_code = "EU"
                    n.country_flag = "🇪🇺"
                    n.country_name = "Европа"

        # STRICT ORDERING requested by user:
        # Priority 0: Foreign nodes (country_code != 'RU' and not is_whitelist) -> Top of list!
        # Priority 1: Regular RU nodes (country_code == 'RU' and not is_whitelist)
        # Priority 2: Whitelist bypass nodes (is_whitelist == True) -> Bottom of list!
        def sorting_key(x: ProxyNode):
            if x.is_whitelist:
                prio = 2
            elif x.country_code == "RU":
                prio = 1
            else:
                prio = 0
            lat = x.latency_ms if x.latency_ms > 0 else 99999
            return (prio, lat)

        alive_nodes.sort(key=sorting_key)

        # Save to disk
        self.save_results(alive_nodes, total)

        return alive_nodes

    def save_results(self, alive_nodes: List[ProxyNode], total_scanned: int):
        """Saves verified working nodes to disk."""
        try:
            # 1. JSON dump with full metadata
            data = {
                "total_scanned": total_scanned,
                "alive_count": len(alive_nodes),
                "timestamp": time.time(),
                "time_str": time.strftime("%Y-%m-%d %H:%M:%S"),
                "whitelist_count": sum(1 for n in alive_nodes if n.is_whitelist),
                "servers": [n.to_dict() for n in alive_nodes]
            }
            with open(self.alive_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            # 2. Text dump with clean vless:// URIs
            with open(self.alive_txt, "w", encoding="utf-8") as f:
                lines = [n.to_vless_uri(n.get_clean_remark(idx + 1)) for idx, n in enumerate(alive_nodes)]
                f.write("\n".join(lines))
        except Exception as e:
            print(f"[!] Ошибка сохранения результатов: {e}")

    def load_cached_alive(self) -> List[ProxyNode]:
        """Loads previously verified alive nodes from disk."""
        nodes: List[ProxyNode] = []
        if os.path.exists(self.alive_file):
            try:
                with open(self.alive_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for item in data.get("servers", []):
                    n = ProxyNode(item.get("uri", ""))
                    n.is_alive = True
                    n.latency_ms = item.get("latency_ms", -1)
                    n.country_code = item.get("country_code", "OTHER")
                    n.country_flag = item.get("country_flag", "🌐")
                    n.country_name = item.get("country_name", "Неизвестно")
                    n.is_whitelist = item.get("is_whitelist", False)
                    n.whitelist_label = item.get("whitelist_label", "")
                    n.whitelist_category = item.get("whitelist_category", "")
                    nodes.append(n)
            except Exception:
                pass
        return nodes
