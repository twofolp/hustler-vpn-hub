#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smart Proxy Relay & Failover Controller
Maintains per-country healthy server pools and handles dynamic switching.
"""

import os
import sys
import time
import json
import asyncio
from typing import List, Dict, Optional, Any
from collections import defaultdict

from core.parser import ProxyNode
from core.checker import ProxyChecker


class CountryPool:
    def __init__(self, country_code: str):
        self.country_code = country_code
        self.servers: List[ProxyNode] = []
        self.active_index: int = 0
        self.failed_attempts: int = 0

    def update_servers(self, servers: List[ProxyNode]):
        self.servers = [s for s in servers if s.is_alive and s.country_code == self.country_code]
        self.servers.sort(key=lambda s: s.latency_ms if s.latency_ms > 0 else 99999)
        self.active_index = 0
        self.failed_attempts = 0

    def get_current(self) -> Optional[ProxyNode]:
        if not self.servers:
            return None
        return self.servers[self.active_index % len(self.servers)]

    def report_failure(self) -> Optional[ProxyNode]:
        """Switches to the next healthy server in the same country."""
        if not self.servers or len(self.servers) <= 1:
            return None
        self.active_index = (self.active_index + 1) % len(self.servers)
        self.failed_attempts += 1
        return self.get_current()


class SmartProxyManager:
    def __init__(self, checker: ProxyChecker):
        self.checker = checker
        self.pools: Dict[str, CountryPool] = defaultdict(lambda: CountryPool("OTHER"))
        self.whitelist_pool = CountryPool("WHITELIST")
        self.all_alive: List[ProxyNode] = []

    def update_pools(self, alive_nodes: List[ProxyNode]):
        self.all_alive = alive_nodes
        by_country = defaultdict(list)
        wl_nodes = []

        for node in alive_nodes:
            by_country[node.country_code].append(node)
            if node.is_whitelist:
                wl_nodes.append(node)

        for cc, nodes in by_country.items():
            pool = CountryPool(cc)
            pool.update_servers(nodes)
            self.pools[cc] = pool

        self.whitelist_pool.update_servers(wl_nodes)

    def get_server_for_country(self, country_code: str) -> Optional[ProxyNode]:
        cc = country_code.upper()
        if cc in self.pools:
            return self.pools[cc].get_current()
        return self.all_alive[0] if self.all_alive else None

    def failover_country(self, country_code: str) -> Optional[ProxyNode]:
        cc = country_code.upper()
        if cc in self.pools:
            return self.pools[cc].report_failure()
        return None

    def get_status(self) -> Dict[str, Any]:
        status = {
            "total_alive": len(self.all_alive),
            "countries": {}
        }
        for cc, pool in self.pools.items():
            curr = pool.get_current()
            status["countries"][cc] = {
                "server_count": len(pool.servers),
                "active_server": curr.get_clean_remark() if curr else None,
                "active_ping": curr.latency_ms if curr else -1
            }
        return status
