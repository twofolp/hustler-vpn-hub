#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GeoIP & Country Resolution Module
Detects country from server remarks (flag emojis, country names) or IP batch lookup.
"""

import os
import re
import json
import urllib.request
import urllib.parse
from typing import Dict, List, Optional, Tuple

COUNTRY_MAP = {
    "RU": {"flag": "🇷🇺", "name_ru": "Россия", "name_en": "Russia"},
    "DE": {"flag": "🇩🇪", "name_ru": "Германия", "name_en": "Germany"},
    "NL": {"flag": "🇳🇱", "name_ru": "Нидерланды", "name_en": "Netherlands"},
    "FI": {"flag": "🇫🇮", "name_ru": "Финляндия", "name_en": "Finland"},
    "SE": {"flag": "🇸🇪", "name_ru": "Швеция", "name_en": "Sweden"},
    "US": {"flag": "🇺🇸", "name_ru": "США", "name_en": "United States"},
    "GB": {"flag": "🇬🇧", "name_ru": "Великобритания", "name_en": "United Kingdom"},
    "UK": {"flag": "🇬🇧", "name_ru": "Великобритания", "name_en": "United Kingdom"},
    "FR": {"flag": "🇫🇷", "name_ru": "Франция", "name_en": "France"},
    "TR": {"flag": "🇹🇷", "name_ru": "Турция", "name_en": "Turkey"},
    "PL": {"flag": "🇵🇱", "name_ru": "Польша", "name_en": "Poland"},
    "KZ": {"flag": "🇰🇿", "name_ru": "Казахстан", "name_en": "Kazakhstan"},
    "UA": {"flag": "🇺🇦", "name_ru": "Украина", "name_en": "Ukraine"},
    "AM": {"flag": "🇦🇲", "name_ru": "Армения", "name_en": "Armenia"},
    "GE": {"flag": "🇬🇪", "name_ru": "Грузия", "name_en": "Georgia"},
    "BY": {"flag": "🇧🇾", "name_ru": "Беларусь", "name_en": "Belarus"},
    "AT": {"flag": "🇦🇹", "name_ru": "Австрия", "name_en": "Austria"},
    "CH": {"flag": "🇨🇭", "name_ru": "Швейцария", "name_en": "Switzerland"},
    "ES": {"flag": "🇪🇸", "name_ru": "Испания", "name_en": "Spain"},
    "IT": {"flag": "🇮🇹", "name_ru": "Италия", "name_en": "Italy"},
    "MD": {"flag": "🇲🇩", "name_ru": "Молдова", "name_en": "Moldova"},
    "RS": {"flag": "🇷🇸", "name_ru": "Сербия", "name_en": "Serbia"},
    "BG": {"flag": "🇧🇬", "name_ru": "Болгария", "name_en": "Bulgaria"},
    "RO": {"flag": "🇷🇴", "name_ru": "Румыния", "name_en": "Romania"},
    "CZ": {"flag": "🇨🇿", "name_ru": "Чехия", "name_en": "Czech Republic"},
    "JP": {"flag": "🇯🇵", "name_ru": "Япония", "name_en": "Japan"},
    "SG": {"flag": "🇸🇬", "name_ru": "Сингапур", "name_en": "Singapore"},
    "HK": {"flag": "🇭🇰", "name_ru": "Гонконг", "name_en": "Hong Kong"},
    "IN": {"flag": "🇮🇳", "name_ru": "Индия", "name_en": "India"},
    "CA": {"flag": "🇨🇦", "name_ru": "Канада", "name_en": "Canada"},
    "BR": {"flag": "🇧🇷", "name_ru": "Бразилия", "name_en": "Brazil"},
    "AE": {"flag": "🇦🇪", "name_ru": "ОАЭ", "name_en": "UAE"},
    "IL": {"flag": "🇮🇱", "name_ru": "Израиль", "name_en": "Israel"},
    "LV": {"flag": "🇱🇻", "name_ru": "Латвия", "name_en": "Latvia"},
    "LT": {"flag": "🇱🇹", "name_ru": "Литва", "name_en": "Lithuania"},
    "EE": {"flag": "🇪🇪", "name_ru": "Эстония", "name_en": "Estonia"},
    "NO": {"flag": "🇳🇴", "name_ru": "Норвегия", "name_en": "Norway"},
}

FLAG_TO_CODE = {v["flag"]: k for k, v in COUNTRY_MAP.items()}

KEYWORDS = {
    "russia": "RU", "россия": "RU", "rus": "RU",
    "germany": "DE", "германия": "DE", "deutschland": "DE",
    "netherlands": "NL", "нидерланды": "NL", "holland": "NL",
    "finland": "FI", "финляндия": "FI", "helsinki": "FI",
    "sweden": "SE", "швеция": "SE", "stockholm": "SE",
    "united states": "US", "usa": "US", "сша": "US", "america": "US",
    "united kingdom": "GB", "uk": "GB", "london": "GB", "англия": "GB",
    "france": "FR", "франция": "FR", "paris": "FR",
    "turkey": "TR", "турция": "TR", "istanbul": "TR",
    "poland": "PL", "польша": "PL", "warsaw": "PL",
    "kazakhstan": "KZ", "казахстан": "KZ", "almaty": "KZ", "astana": "KZ",
    "spain": "ES", "испания": "ES", "madrid": "ES",
    "italy": "IT", "италия": "IT", "rome": "IT", "milan": "IT",
    "austria": "AT", "австрия": "AT", "vienna": "AT",
    "switzerland": "CH", "швейцария": "CH", "zurich": "CH",
    "ukraine": "UA", "украина": "UA", "kyiv": "UA",
    "armenia": "AM", "армения": "AM", "yerevan": "AM",
    "georgia": "GE", "грузия": "GE", "tbilisi": "GE",
    "serbia": "RS", "сербия": "RS", "belgrade": "RS",
    "bulgaria": "BG", "болгария": "BG", "sofia": "BG",
    "singapore": "SG", "сингапур": "SG",
    "japan": "JP", "япония": "JP", "tokyo": "JP",
}

CACHE_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "geoip_cache.json")


class GeoIPResolver:
    def __init__(self, cache_file: str = CACHE_FILE):
        self.cache_file = cache_file
        self.cache: Dict[str, Dict[str, str]] = {}
        self._load_cache()

    def _load_cache(self):
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    self.cache = json.load(f)
        except Exception:
            self.cache = {}

    def _save_cache(self):
        try:
            os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def detect_from_remark(self, remark: str) -> Optional[Tuple[str, str, str]]:
        """Tries to extract (country_code, flag, name_ru) from remark."""
        if not remark:
            return None
        
        # 1. Look for unicode regional indicator pair (flag emoji)
        flags = re.findall(r'[\U0001F1E6-\U0001F1FF]{2}', remark)
        if flags:
            flag = flags[0]
            code = FLAG_TO_CODE.get(flag)
            if code and code in COUNTRY_MAP:
                return code, flag, COUNTRY_MAP[code]["name_ru"]
            # Construct code from regional indicators
            # '🇦' is 0x1F1E6 -> 'A' is 0x41
            chars = [chr(ord(c) - 0x1F1E6 + ord('A')) for c in flag]
            code = "".join(chars)
            info = COUNTRY_MAP.get(code, {"flag": flag, "name_ru": code})
            return code, info.get("flag", flag), info.get("name_ru", code)

        # 2. Check keywords in remark
        low = remark.lower()
        for kw, code in KEYWORDS.items():
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, low):
                info = COUNTRY_MAP.get(code, {"flag": "🌐", "name_ru": code})
                return code, info["flag"], info["name_ru"]

        return None

    def resolve_batch_ips(self, ips: List[str]) -> Dict[str, Dict[str, str]]:
        """
        Resolves a list of IPv4 addresses using local cache and http://ip-api.com/batch.
        Returns map of ip -> {"code": "RU", "flag": "🇷🇺", "name_ru": "Россия"}
        """
        results: Dict[str, Dict[str, str]] = {}
        missing_ips = []

        # Check cache first
        for ip in ips:
            if not ip or not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip):
                continue
            if ip in self.cache:
                results[ip] = self.cache[ip]
            else:
                missing_ips.append(ip)

        missing_ips = list(set(missing_ips))

        # Query missing in chunks of 100
        if missing_ips:
            for i in range(0, min(len(missing_ips), 500), 100):
                chunk = missing_ips[i:i+100]
                try:
                    req = urllib.request.Request(
                        "http://ip-api.com/batch?fields=query,country,countryCode",
                        data=json.dumps(chunk).encode("utf-8"),
                        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
                    )
                    with urllib.request.urlopen(req, timeout=8) as resp:
                        batch_res = json.loads(resp.read().decode("utf-8"))
                        for item in batch_res:
                            query_ip = item.get("query")
                            code = item.get("countryCode", "OTHER").upper()
                            info = COUNTRY_MAP.get(code, {
                                "flag": "🌐",
                                "name_ru": item.get("country", code)
                            })
                            res_entry = {
                                "code": code,
                                "flag": info.get("flag", "🌐"),
                                "name_ru": info.get("name_ru", code)
                            }
                            self.cache[query_ip] = res_entry
                            results[query_ip] = res_entry
                except Exception:
                    pass

            self._save_cache()

        return results

    def get_info(self, country_code: str) -> Dict[str, str]:
        code = country_code.upper()
        if code in COUNTRY_MAP:
            return COUNTRY_MAP[code]
        return {"flag": "🌐", "name_ru": code, "name_en": code}
