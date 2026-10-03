#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filters and categorizes the gathered 29,976 VLESS configurations:
- Strips CDN IPs
- Separates Reality & TLS
- Detects Whitelist SNIs
"""

import os
import re
import sys
import json
from core.parser import ProxyNode

from test_fetch_all import get_clean_urls, fetch_one
from concurrent.futures import ThreadPoolExecutor

WL_KEYWORDS = [
    "yandex.ru", "ya.ru", "dzen.ru", "passport.yandex.ru",
    "vk.com", "vk.me", "userapi.com", "vk-portal.net",
    "gosuslugi.ru", "esia.gosuslugi.ru", "gu-st.ru",
    "mail.ru", "sber.ru", "sberbank.ru", "tinkoff.ru", "t-bank.ru",
    "avito.ru", "ozon.ru", "wildberries.ru", "kinopoisk.ru",
    "api.dobro.ru", "ligastavok.ru", "utiltools.ru", "utiltools.site",
    "guardora.pro", "bobrkurva.shop", "dora-dura.shop", "soxy-boobs.shop"
]

def main():
    urls = get_clean_urls()
    print(f"[*] Сбор со всех источников ({len(urls)} URLs)...")
    all_raw = []
    with ThreadPoolExecutor(max_workers=30) as ex:
        for u, cfgs in ex.map(fetch_one, urls):
            all_raw.extend(cfgs)

    unique_raw = list(set(all_raw))
    print(f"[+] Собрано сырых VLESS: {len(unique_raw)}")

    reality_nodes = []
    tls_nodes = []
    whitelist_nodes = []
    seen = set()

    for line in unique_raw:
        node = ProxyNode(line)
        if not node or not node.is_valid:
            continue
        if node.is_cloudflare_cdn_ip():
            continue
        if node.security not in ("reality", "tls"):
            continue
        if node.security == "reality" and (not node.pbk or len(node.pbk) < 30 or not node.uuid or len(node.uuid) < 30):
            continue

        key = f"{node.host}:{node.port}"
        if key in seen:
            continue
        seen.add(key)

        sni_low = (node.sni or "").lower()
        rem_low = (node.remark or "").lower()
        is_wl = any(k in sni_low or k in rem_low for k in WL_KEYWORDS)

        if is_wl:
            node.is_whitelist = True
            whitelist_nodes.append(node)

        if node.security == "reality":
            reality_nodes.append(node)
        elif node.security == "tls":
            tls_nodes.append(node)

    print("\n" + "=" * 50)
    print(" 📊 РЕЗУЛЬТАТЫ ФИЛЬТРАЦИИ И АНАЛИЗА ВСЕХ ИСТОЧНИКОВ:")
    print("=" * 50)
    print(f" • Уникальных реальных хостов (без CDN): {len(seen)}")
    print(f" • Валидных VLESS Reality узлов:        {len(reality_nodes)}")
    print(f" • Валидных VLESS TLS узлов:            {len(tls_nodes)}")
    print(f" • Узлов с SNI Whitelist (Яндекс, VK...): {len(whitelist_nodes)}")

    # Save to data/all_candidates.txt
    with open("data/all_candidates.txt", "w", encoding="utf-8") as f:
        for n in reality_nodes + tls_nodes:
            f.write(n.raw_url + "\n")
    print("\n[+] Сохранено в data/all_candidates.txt для проверки!")

if __name__ == "__main__":
    main()
