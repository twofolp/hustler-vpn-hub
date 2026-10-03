#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deep Analyzer of Desktop Source Files:
- C:\\Users\\twofolp\\Desktop\\впн.txt
- C:\\Users\\twofolp\\Desktop\\отсортировать надо.txt
"""

import os
import re
import sys
import json
import urllib.request
from typing import List, Set

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def extract_urls(filepath: str) -> List[str]:
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    # Find all http/https links
    pattern = re.compile(r"https?://[^\s<>\"\'\n\r]+")
    urls = pattern.findall(text)
    # Clean trailing punctuation
    cleaned = []
    for u in urls:
        u = u.rstrip(".,;:)")
        if u and "translate.yandex" not in u:
            cleaned.append(u)
    return cleaned

def main():
    f1 = r"C:\Users\twofolp\Desktop\впн.txt"
    f2 = r"C:\Users\twofolp\Desktop\отсортировать надо.txt"

    urls1 = extract_urls(f1)
    urls2 = extract_urls(f2)

    all_urls = sorted(list(set(urls1 + urls2)))
    print(f"Всего уникальных ссылок в файлах: {len(all_urls)}")
    print(f"  • Из впн.txt: {len(set(urls1))}")
    print(f"  • Из отсортировать надо.txt: {len(set(urls2))}")

    direct_subs = []
    github_repos = []
    other_links = []

    for u in all_urls:
        if "raw.githubusercontent.com" in u or "gist.githubusercontent.com" in u or "gitverse.ru" in u or u.endswith(".txt"):
            direct_subs.append(u)
        elif "github.com/" in u and not u.endswith(".txt"):
            github_repos.append(u)
        else:
            other_links.append(u)

    print(f"\n1. Прямые ссылки на файлы/подписки: {len(direct_subs)}")
    for s in direct_subs[:10]:
        print(f"   - {s}")
    if len(direct_subs) > 10:
        print(f"   ... и ещё {len(direct_subs)-10} прямых подписок")

    print(f"\n2. Ссылки на репозитории GitHub (с подписками внутри): {len(github_repos)}")
    for r in github_repos[:10]:
        print(f"   - {r}")
    if len(github_repos) > 10:
        print(f"   ... и ещё {len(github_repos)-10} репозиториев")

    print(f"\n3. Прочие ссылки: {len(other_links)}")
    for o in other_links[:5]:
        print(f"   - {o}")

if __name__ == "__main__":
    main()
