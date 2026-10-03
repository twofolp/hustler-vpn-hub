#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Proxy URI Parser & Normalizer
Supports VLESS, VMess, Shadowsocks, Trojan.
Detects whitelist targets (VK, Госуслуги, Яндекс, etc.) and security profiles.
"""

import re
import json
import base64
import urllib.parse
from typing import Dict, Any, Optional, List

WHITELIST_PATTERNS = [
    (r'(?:^|\.)(?:vk\.com|vk\.me|userapi\.com)', "VKontakte", "🛡️ VK"),
    (r'(?:^|\.)gosuslugi\.ru', "Gosuslugi", "🛡️ Госуслуги"),
    (r'(?:^|\.)(?:ya\.ru|dzen\.ru|yandex\.ru|yandex\.net)', "Yandex-Dzen", "🛡️ Яндекс/Дзен"),
    (r'(?:^|\.)mail\.ru', "Mail.ru", "🛡️ Mail.ru"),
    (r'(?:^|\.)(?:wildberries\.ru|ozon\.ru)', "Marketplace", "🛡️ Маркетплейс"),
    (r'(?:^|\.)(?:sberbank\.ru|sber\.ru|tbank\.ru|tinkoff\.ru|vtb\.ru)', "Banking", "🛡️ Банки"),
    (r'(?:^|\.)(?:rutube\.ru|max\.ru|ligastavok\.ru|fon\.bet|winline\.ru)', "Bypass-Media", "🛡️ Обход-СМИ"),
]

WHITELIST_KEYWORDS = [
    "whitelist", "белый список", "обход", "анти-ркн", "антиркн", "white", "cid-white", "bypass"
]


class ProxyNode:
    def __init__(self, raw_url: str):
        self.raw_url = raw_url.strip()
        self.protocol: str = ""
        self.uuid: str = ""
        self.host: str = ""
        self.port: int = 443
        self.params: Dict[str, str] = {}
        self.remark: str = ""
        self.security: str = ""
        self.sni: str = ""
        self.pbk: str = ""
        self.sid: str = ""
        self.net_type: str = "tcp"
        self.flow: str = ""
        self.fp: str = ""
        self.path: str = ""
        self.host_header: str = ""
        self.is_whitelist: bool = False
        self.whitelist_label: str = ""
        self.whitelist_category: str = ""
        self.country_code: str = "OTHER"
        self.country_flag: str = "🌐"
        self.country_name: str = "Неизвестно"
        self.latency_ms: int = -1
        self.is_alive: bool = False
        self.source_id: Optional[int] = None
        self.is_valid: bool = False
        self._parse()

    def _parse(self):
        if not self.raw_url:
            return

        try:
            if self.raw_url.startswith("vless://"):
                self._parse_vless()
            elif self.raw_url.startswith("vmess://"):
                self._parse_vmess()
            elif self.raw_url.startswith("ss://"):
                self._parse_ss()
            elif self.raw_url.startswith("trojan://"):
                self._parse_trojan()
            else:
                self.is_valid = False
                return

            if self.host and self.port > 0:
                self.is_valid = True
                self._check_whitelist()
        except Exception:
            self.is_valid = False

    def _parse_vless(self):
        self.protocol = "vless"
        # vless://uuid@host:port?param1=val&param2=val#remark
        body = self.raw_url[8:]
        remark = ""
        if "#" in body:
            body, remark = body.split("#", 1)
            self.remark = urllib.parse.unquote(remark).strip()

        query_str = ""
        if "?" in body:
            body, query_str = body.split("?", 1)
            for k, v in urllib.parse.parse_qsl(query_str, keep_blank_values=True):
                self.params[k] = v

        if "@" in body:
            self.uuid, host_port = body.split("@", 1)
        else:
            return

        if ":" in host_port:
            parts = host_port.split(":")
            self.host = parts[0].strip("[]")
            self.port = int(parts[1]) if parts[1].isdigit() else 443
        else:
            self.host = host_port.strip("[]")
            self.port = 443

        self.security = self.params.get("security", "").lower()
        self.sni = self.params.get("sni", "") or self.params.get("peer", "")
        self.pbk = self.params.get("pbk", "")
        self.sid = self.params.get("sid", "")
        self.net_type = self.params.get("type", "tcp").lower()
        self.flow = self.params.get("flow", "")
        self.fp = self.params.get("fp", "chrome")
        self.path = self.params.get("path", "")
        self.host_header = self.params.get("host", "")

    def _parse_vmess(self):
        self.protocol = "vmess"
        body = self.raw_url[8:]
        try:
            # Often base64 encoded JSON
            missing_padding = len(body) % 4
            if missing_padding:
                body += '=' * (4 - missing_padding)
            decoded = base64.b64decode(body).decode('utf-8', errors='ignore')
            data = json.loads(decoded)
            self.host = data.get("add", "")
            self.port = int(data.get("port", 443))
            self.uuid = data.get("id", "")
            self.net_type = data.get("net", "tcp")
            self.security = data.get("tls", "")
            self.sni = data.get("sni", "") or data.get("host", "")
            self.path = data.get("path", "")
            self.remark = data.get("ps", "")
        except Exception:
            pass

    def _parse_ss(self):
        self.protocol = "ss"
        body = self.raw_url[5:]
        if "#" in body:
            body, remark = body.split("#", 1)
            self.remark = urllib.parse.unquote(remark).strip()
        if "@" in body:
            cred, host_port = body.split("@", 1)
            if ":" in host_port:
                parts = host_port.split(":")
                self.host = parts[0].strip("[]")
                self.port = int(parts[1]) if parts[1].isdigit() else 8388
        else:
            # Maybe base64
            try:
                missing = len(body) % 4
                if missing:
                    body += '=' * (4 - missing)
                dec = base64.b64decode(body).decode('utf-8', errors='ignore')
                if "@" in dec:
                    cred, host_port = dec.split("@", 1)
                    if ":" in host_port:
                        parts = host_port.split(":")
                        self.host = parts[0].strip("[]")
                        self.port = int(parts[1]) if parts[1].isdigit() else 8388
            except Exception:
                pass

    def _parse_trojan(self):
        self.protocol = "trojan"
        body = self.raw_url[9:]
        if "#" in body:
            body, remark = body.split("#", 1)
            self.remark = urllib.parse.unquote(remark).strip()
        if "?" in body:
            body, query_str = body.split("?", 1)
            for k, v in urllib.parse.parse_qsl(query_str, keep_blank_values=True):
                self.params[k] = v
        if "@" in body:
            pwd, host_port = body.split("@", 1)
            self.uuid = pwd
            if ":" in host_port:
                parts = host_port.split(":")
                self.host = parts[0].strip("[]")
                self.port = int(parts[1]) if parts[1].isdigit() else 443
        self.sni = self.params.get("sni", "") or self.params.get("peer", "")
        self.security = self.params.get("security", "tls")

    def _check_whitelist(self):
        target_str = (self.sni + " " + self.host_header + " " + self.remark).lower()

        # Check SNI against whitelist domains
        for pattern, cat, label in WHITELIST_PATTERNS:
            if self.sni and re.search(pattern, self.sni.lower()):
                self.is_whitelist = True
                self.whitelist_category = cat
                self.whitelist_label = label
                return

        # Check keywords in remark
        for kw in WHITELIST_KEYWORDS:
            if kw in target_str:
                self.is_whitelist = True
                self.whitelist_category = "Keyword-Bypass"
                self.whitelist_label = "🛡️ Белый список"
                return

        # Check if source is dedicated whitelist source (4, 7, 9, 18, 24)
        if self.source_id in [4, 7, 9, 18, 24]:
            self.is_whitelist = True
            self.whitelist_category = f"Source-{self.source_id}"
            self.whitelist_label = "🛡️ Источник обхода"

    def is_cloudflare_cdn_ip(self) -> bool:
        """Detects if host IP is a Cloudflare Anycast CDN IP (common false positive in scrapers)."""
        cf_prefixes = [
            "104.16.", "104.17.", "104.18.", "104.19.", "104.20.", "104.21.", "104.22.", "104.23.", "104.24.", "104.25.", "104.26.", "104.27.",
            "172.64.", "172.65.", "172.66.", "172.67.", "172.68.", "172.69.", "172.70.", "172.71.",
            "188.114.96.", "188.114.97.", "188.114.98.", "188.114.99.", "198.41."
        ]
        return any(self.host.startswith(p) for p in cf_prefixes)

    def get_clean_remark(self, index: Optional[int] = None) -> str:
        """Constructs an informative, beautiful remark for clients (never uses raw scraped junk)."""
        flag = self.country_flag or "🌐"
        c_name = self.country_name if self.country_name and self.country_name != "Неизвестно" else (self.country_code or "VPN")
        
        wl = f" [{self.whitelist_label}]" if self.is_whitelist else ""
        gaming = " [🎮 Игровой]" if (not self.is_whitelist and 0 < self.latency_ms <= 85) else ""
        ping = f" • {self.latency_ms}ms" if self.latency_ms > 0 else ""
        num = f" #{index}" if index is not None else ""
        
        return f"{flag} {c_name}{wl}{gaming}{num}{ping}".strip()

    def to_vless_uri(self, custom_remark: Optional[str] = None) -> str:
        """Formats back to standard vless:// URI with guaranteed clean readable remark."""
        if self.protocol != "vless":
            return self.raw_url
        
        query = urllib.parse.urlencode(self.params)
        remark = custom_remark if custom_remark else self.get_clean_remark()
        encoded_remark = urllib.parse.quote(remark)
        return f"vless://{self.uuid}@{self.host}:{self.port}?{query}#{encoded_remark}"

    def to_dict(self) -> Dict[str, Any]:
        clean_rem = self.get_clean_remark()
        return {
            "protocol": self.protocol,
            "host": self.host,
            "port": self.port,
            "uuid": self.uuid,
            "security": self.security,
            "sni": self.sni,
            "pbk": self.pbk,
            "sid": self.sid,
            "flow": self.flow,
            "type": self.net_type,
            "remark": clean_rem,
            "is_whitelist": self.is_whitelist,
            "whitelist_label": self.whitelist_label,
            "whitelist_category": self.whitelist_category,
            "country_code": self.country_code,
            "country_flag": self.country_flag,
            "country_name": self.country_name,
            "latency_ms": self.latency_ms,
            "is_alive": self.is_alive,
            "source_id": self.source_id,
            "uri": self.to_vless_uri(clean_rem)
        }


def parse_configs_from_text(text: str, default_source_id: Optional[int] = None) -> List[ProxyNode]:
    """Extracts all valid proxy URIs from text."""
    nodes: List[ProxyNode] = []
    seen = set()

    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("//"):
            continue
        
        # Regex find URIs
        matches = re.findall(r'(vless://[^\s]+|vmess://[^\s]+|ss://[^\s]+|trojan://[^\s]+)', line)
        for m in matches:
            node = ProxyNode(m)
            if default_source_id:
                node.source_id = default_source_id
                node._check_whitelist()
            if node.is_valid:
                # Deduplication key: protocol + host + port + uuid
                key = f"{node.protocol}://{node.uuid}@{node.host}:{node.port}"
                if key not in seen:
                    seen.add(key)
                    nodes.append(node)
    return nodes
