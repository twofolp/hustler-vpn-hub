#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-Subscription Generator
Supports:
1. Base64 & Plain URI list (Incy, Happ, v2rayNG, v2rayN, V2Box, Throne, NekoBox)
2. Clash Meta / Mihomo YAML with Auto-Failover & URL-test groups per country
3. Sing-box / Hiddify JSON with per-country urltest failover outbounds
"""

import re
import json
import base64
import urllib.parse
from typing import List, Dict, Any, Optional
from collections import defaultdict

from core.parser import ProxyNode
from core.geoip import COUNTRY_MAP


class SubscriptionGenerator:
    def __init__(self, app_name: str = "VLESS-PO-GRIBI-HUB"):
        self.app_name = app_name

    # =========================================================================
    # 1. Plain & Base64 Subscription (Incy / Happ / v2rayNG / Throne / v2rayN)
    # =========================================================================
    def generate_plain(
        self,
        nodes: List[ProxyNode],
        whitelist_only: bool = False,
        country_code: Optional[str] = None,
        top_per_country: Optional[int] = None,
        gaming_only: bool = False,
        max_nodes: int = 150
    ) -> str:
        """Generates plain newline-separated list of working URIs."""
        filtered = self._filter_nodes(
            nodes, whitelist_only, country_code, top_per_country, gaming_only, max_nodes
        )
        lines = []
        for idx, node in enumerate(filtered):
            remark = node.get_clean_remark(idx + 1)
            lines.append(node.to_vless_uri(remark))
        return "\n".join(lines)

    def generate_base64(
        self,
        nodes: List[ProxyNode],
        whitelist_only: bool = False,
        country_code: Optional[str] = None,
        top_per_country: Optional[int] = None,
        gaming_only: bool = False,
        max_nodes: int = 150
    ) -> str:
        """Generates Base64 encoded subscription."""
        plain = self.generate_plain(
            nodes, whitelist_only, country_code, top_per_country, gaming_only, max_nodes
        )
        return base64.b64encode(plain.encode("utf-8")).decode("ascii")

    def get_best_server(
        self,
        nodes: List[ProxyNode],
        whitelist_only: bool = False,
        gaming_only: bool = False
    ) -> Optional[str]:
        """Returns single best server URI (Guaranteed non-RU for general browsing)."""
        if whitelist_only:
            candidates = [n for n in nodes if n.is_alive and n.is_whitelist]
        else:
            # Must be non-RU and non-whitelist for general unblocked internet!
            candidates = [n for n in nodes if n.is_alive and not n.is_whitelist and n.country_code != "RU"]
            if gaming_only:
                candidates = [n for n in candidates if 0 < n.latency_ms <= 85]
            if not candidates:
                candidates = [n for n in nodes if n.is_alive]

        if candidates:
            candidates.sort(key=lambda x: x.latency_ms if x.latency_ms > 0 else 99999)
            best = candidates[0]
            tag = " [Лучший Обход]" if whitelist_only else (" [Игровой]" if gaming_only else " [Лучший Сервер]")
            remark = f"{best.country_flag}{tag} {best.country_name or best.country_code} • {best.latency_ms}ms"
            return best.to_vless_uri(remark)
        return None

    # =========================================================================
    # 2. Clash Meta / Mihomo YAML with Auto-Failover (Переключение по стране)
    # =========================================================================
    def generate_clash_meta(
        self,
        nodes: List[ProxyNode],
        whitelist_only: bool = False,
        country_code: Optional[str] = None,
        max_nodes: int = 100
    ) -> str:
        """
        Generates Mihomo / Clash Meta YAML with:
        - URL-Test (Lowest Ping)
        - Fallback per Country (🇷🇺, 🇩🇪, 🇳🇱, 🇫🇮, 🇺🇸...)
        - Whitelist Fallback group
        """
        filtered = self._filter_nodes(nodes, whitelist_only, country_code, max_nodes)
        clash_proxies = []
        proxy_names = []
        proxies_by_country = defaultdict(list)
        whitelist_proxies = []

        for idx, node in enumerate(filtered):
            # Only export nodes that have valid VLESS structure
            c_proxy = self._node_to_clash(node, idx + 1)
            if c_proxy:
                name = c_proxy["name"]
                clash_proxies.append(c_proxy)
                proxy_names.append(name)
                proxies_by_country[node.country_code].append(name)
                if node.is_whitelist:
                    whitelist_proxies.append(name)

        if not proxy_names:
            proxy_names = ["DIRECT"]

        # Build proxy groups
        proxy_groups = []

        # 1. Main Selector
        main_proxies = ["⚡ Авто-Выбор (Лучший пинг)"]
        if whitelist_proxies:
            main_proxies.append("🛡️ Белый список (Auto-Failover)")
        for cc, plist in proxies_by_country.items():
            if len(plist) >= 1:
                c_info = COUNTRY_MAP.get(cc, {"flag": "🌐", "name_ru": cc})
                main_proxies.append(f"{c_info['flag']} {c_info['name_ru']} (Auto-Failover)")
        main_proxies.extend(["DIRECT", "REJECT"] + proxy_names[:25])

        proxy_groups.append({
            "name": "🚀 PROXY",
            "type": "select",
            "proxies": main_proxies
        })

        # 2. Global URL-Test (Fastest ping among all)
        proxy_groups.append({
            "name": "⚡ Авто-Выбор (Лучший пинг)",
            "type": "url-test",
            "url": "http://cp.cloudflare.com/generate_204",
            "interval": 60,
            "tolerance": 50,
            "proxies": proxy_names
        })

        # 3. Whitelist Fallback group
        if whitelist_proxies:
            proxy_groups.append({
                "name": "🛡️ Белый список (Auto-Failover)",
                "type": "fallback",
                "url": "http://cp.cloudflare.com/generate_204",
                "interval": 45,
                "proxies": whitelist_proxies
            })

        # 4. Per-Country Auto-Failover groups
        for cc, plist in proxies_by_country.items():
            if len(plist) >= 1:
                c_info = COUNTRY_MAP.get(cc, {"flag": "🌐", "name_ru": cc})
                group_name = f"{c_info['flag']} {c_info['name_ru']} (Auto-Failover)"
                proxy_groups.append({
                    "name": group_name,
                    "type": "fallback" if len(plist) > 1 else "select",
                    "url": "http://cp.cloudflare.com/generate_204",
                    "interval": 60,
                    "proxies": plist
                })

        # Assemble YAML manually to avoid dependency issues with PyYAML
        lines = [
            f"# Generated by {self.app_name}",
            "port: 7890",
            "socks-port: 7891",
            "allow-lan: false",
            "mode: rule",
            "log-level: info",
            "external-controller: 127.0.0.1:9090",
            "",
            "proxies:"
        ]

        for p in clash_proxies:
            lines.extend(self._format_clash_proxy_yaml(p))

        lines.append("")
        lines.append("proxy-groups:")
        for g in proxy_groups:
            lines.extend(self._format_clash_group_yaml(g))

        lines.extend([
            "",
            "rules:",
            "  - GEOIP,RU,DIRECT",
            "  - MATCH,🚀 PROXY"
        ])

        return "\n".join(lines)

    # =========================================================================
    # 3. Sing-box / Hiddify JSON with Auto-Failover
    # =========================================================================
    def generate_singbox(
        self,
        nodes: List[ProxyNode],
        whitelist_only: bool = False,
        country_code: Optional[str] = None,
        max_nodes: int = 100
    ) -> str:
        """
        Generates Sing-box / Hiddify JSON configuration with native urltest groups per country.
        """
        filtered = self._filter_nodes(nodes, whitelist_only, country_code, max_nodes)
        outbounds = []
        tags = []
        by_country = defaultdict(list)
        whitelist_tags = []

        for idx, node in enumerate(filtered):
            outbound = self._node_to_singbox(node, idx + 1)
            if outbound:
                tag = outbound["tag"]
                outbounds.append(outbound)
                tags.append(tag)
                by_country[node.country_code].append(tag)
                if node.is_whitelist:
                    whitelist_tags.append(tag)

        if not tags:
            tags = ["direct"]

        # Selector and urltest outbounds
        selector_outbounds = ["⚡ Авто (Лучший пинг)"]
        if whitelist_tags:
            selector_outbounds.append("🛡️ Белый список (Auto-Failover)")
        for cc in by_country:
            c_info = COUNTRY_MAP.get(cc, {"flag": "🌐", "name_ru": cc})
            selector_outbounds.append(f"{c_info['flag']} {c_info['name_ru']} (Auto-Failover)")
        selector_outbounds.extend(["direct", "block"] + tags[:20])

        groups = [
            {
                "type": "selector",
                "tag": "🚀 Выбор прокси",
                "outbounds": selector_outbounds
            },
            {
                "type": "urltest",
                "tag": "⚡ Авто (Лучший пинг)",
                "outbounds": tags,
                "url": "https://www.gstatic.com/generate_204",
                "interval": "1m",
                "tolerance": 50
            }
        ]

        if whitelist_tags:
            groups.append({
                "type": "urltest",
                "tag": "🛡️ Белый список (Auto-Failover)",
                "outbounds": whitelist_tags,
                "url": "https://www.gstatic.com/generate_204",
                "interval": "1m"
            })

        for cc, ptags in by_country.items():
            if len(ptags) >= 1:
                c_info = COUNTRY_MAP.get(cc, {"flag": "🌐", "name_ru": cc})
                groups.append({
                    "type": "urltest",
                    "tag": f"{c_info['flag']} {c_info['name_ru']} (Auto-Failover)",
                    "outbounds": ptags,
                    "url": "https://www.gstatic.com/generate_204",
                    "interval": "1m",
                    "tolerance": 50
                })

        config = {
            "version": 1,
            "outbounds": groups + outbounds + [
                {"type": "direct", "tag": "direct"},
                {"type": "block", "tag": "block"}
            ]
        }
        return json.dumps(config, ensure_ascii=False, indent=2)

    # =========================================================================
    # Helpers
    # =========================================================================
    def _filter_nodes(
        self,
        nodes: List[ProxyNode],
        whitelist_only: bool = False,
        country_code: Optional[str] = None,
        top_per_country: Optional[int] = None,
        gaming_only: bool = False,
        max_nodes: int = 150
    ) -> List[ProxyNode]:
        result = [n for n in nodes if n.is_alive]
        if whitelist_only:
            result = [n for n in result if n.is_whitelist]
        if gaming_only:
            # Low latency for gaming (< 85 ms)
            result = [n for n in result if 0 < n.latency_ms <= 85]
        if country_code:
            code = country_code.upper()
            result = [n for n in result if n.country_code.upper() == code]

        if top_per_country and top_per_country > 0:
            by_cc = defaultdict(list)
            for n in result:
                if len(by_cc[n.country_code]) < top_per_country:
                    by_cc[n.country_code].append(n)
            flattened = []
            for plist in by_cc.values():
                flattened.extend(plist)
            result = flattened

        # Strict ordering: Foreign first, RU middle, Whitelist at bottom
        def sorting_key(x: ProxyNode):
            if x.is_whitelist:
                prio = 2
            elif x.country_code == "RU":
                prio = 1
            else:
                prio = 0
            lat = x.latency_ms if x.latency_ms > 0 else 99999
            return (prio, lat)

        result.sort(key=sorting_key)
        return result[:max_nodes]

    def _node_to_clash(self, node: ProxyNode, index: int) -> Optional[Dict[str, Any]]:
        name = node.get_clean_remark(index)
        # Escape quotes in name
        name = name.replace('"', '')

        if node.protocol == "vless":
            p = {
                "name": name,
                "type": "vless",
                "server": node.host,
                "port": node.port,
                "uuid": node.uuid,
                "network": node.net_type or "tcp",
                "udp": True,
                "tls": node.security in ["tls", "reality"],
                "flow": node.flow,
                "servername": node.sni or node.host,
                "client-fingerprint": node.fp or "chrome"
            }
            if node.security == "reality":
                p["reality-opts"] = {
                    "public-key": node.pbk,
                    "short-id": node.sid or ""
                }
            if node.net_type == "ws":
                p["ws-opts"] = {
                    "path": node.path or "/",
                    "headers": {"Host": node.host_header or node.sni or node.host}
                }
            elif node.net_type == "grpc":
                p["grpc-opts"] = {
                    "grpc-service-name": node.params.get("serviceName", "")
                }
            return p

        elif node.protocol == "ss":
            return {
                "name": name,
                "type": "ss",
                "server": node.host,
                "port": node.port,
                "cipher": "aes-128-gcm",
                "password": node.uuid,
                "udp": True
            }
        return None

    def _format_clash_proxy_yaml(self, p: Dict[str, Any]) -> List[str]:
        lines = [f"  - name: \"{p['name']}\"", f"    type: {p['type']}", f"    server: {p['server']}", f"    port: {p['port']}"]
        if "uuid" in p:
            lines.append(f"    uuid: {p['uuid']}")
        if "cipher" in p:
            lines.append(f"    cipher: {p['cipher']}")
            lines.append(f"    password: {p.get('password', '')}")
        if "network" in p:
            lines.append(f"    network: {p['network']}")
        if "tls" in p:
            lines.append(f"    tls: {'true' if p['tls'] else 'false'}")
        if p.get("flow"):
            lines.append(f"    flow: {p['flow']}")
        if p.get("servername"):
            lines.append(f"    servername: {p['servername']}")
        if p.get("client-fingerprint"):
            lines.append(f"    client-fingerprint: {p['client-fingerprint']}")
        if "reality-opts" in p:
            lines.append("    reality-opts:")
            lines.append(f"      public-key: {p['reality-opts']['public-key']}")
            lines.append(f"      short-id: \"{p['reality-opts']['short-id']}\"")
        if "ws-opts" in p:
            lines.append("    ws-opts:")
            lines.append(f"      path: {p['ws-opts']['path']}")
            if "headers" in p["ws-opts"]:
                lines.append("      headers:")
                for hk, hv in p["ws-opts"]["headers"].items():
                    lines.append(f"        {hk}: {hv}")
        if "grpc-opts" in p:
            lines.append("    grpc-opts:")
            lines.append(f"      grpc-service-name: {p['grpc-opts']['grpc-service-name']}")
        if p.get("udp"):
            lines.append("    udp: true")
        return lines

    def _format_clash_group_yaml(self, g: Dict[str, Any]) -> List[str]:
        lines = [f"  - name: \"{g['name']}\"", f"    type: {g['type']}"]
        if "url" in g:
            lines.append(f"    url: {g['url']}")
        if "interval" in g:
            lines.append(f"    interval: {g['interval']}")
        if "tolerance" in g:
            lines.append(f"    tolerance: {g['tolerance']}")
        lines.append("    proxies:")
        for px in g["proxies"]:
            lines.append(f"      - \"{px}\"")
        return lines

    def _node_to_singbox(self, node: ProxyNode, index: int) -> Optional[Dict[str, Any]]:
        name = node.get_clean_remark(index)
        if node.protocol == "vless":
            out = {
                "type": "vless",
                "tag": name,
                "server": node.host,
                "server_port": node.port,
                "uuid": node.uuid,
                "flow": node.flow or "",
                "network": node.net_type or "tcp",
                "tls": {
                    "enabled": node.security in ["tls", "reality"],
                    "server_name": node.sni or node.host,
                    "utls": {"enabled": True, "fingerprint": node.fp or "chrome"}
                }
            }
            if node.security == "reality":
                out["tls"]["reality"] = {
                    "enabled": True,
                    "public_key": node.pbk,
                    "short_id": node.sid or ""
                }
            if node.net_type == "ws":
                out["transport"] = {
                    "type": "ws",
                    "path": node.path or "/",
                    "headers": {"Host": node.host_header or node.sni or node.host}
                }
            elif node.net_type == "grpc":
                out["transport"] = {
                    "type": "grpc",
                    "service_name": node.params.get("serviceName", "")
                }
            return out
        return None
