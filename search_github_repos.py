#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import json
import time

queries = [
    "vless whitelist",
    "vless белые списки",
    "vless russia whitelist",
    "vless bypass rkn",
    "vless-configs-for-russia",
    "vk turn proxy",
    "vk turn vless"
]

headers = {"User-Agent": "Mozilla/5.0"}
found_repos = {}

for q in queries:
    url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(q)}&sort=updated&order=desc&per_page=20"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode("utf-8"))
            items = data.get("items", [])
            print(f"Query '{q}': found {len(items)} repos (total: {data.get('total_count', 0)})")
            for it in items:
                repo_name = it["full_name"]
                if repo_name not in found_repos:
                    found_repos[repo_name] = {
                        "name": repo_name,
                        "url": it["html_url"],
                        "desc": it.get("description", ""),
                        "stars": it.get("stargazers_count", 0),
                        "updated": it.get("updated_at", "")
                    }
        time.sleep(1.2)
    except Exception as e:
        print(f"Query '{q}' error: {e}")

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

with open("data/discovered_github_repos.json", "w", encoding="utf-8") as f:
    json.dump(found_repos, f, ensure_ascii=False, indent=2)

print(f"\nTotal unique repos found: {len(found_repos)}")
for k, v in sorted(found_repos.items(), key=lambda x: x[1]["stars"], reverse=True)[:35]:
    print(f"- {v['name']} ({v['stars']} stars) [Updated: {v['updated']}]: {v['url']}")
    if v['desc']:
        print(f"  {v['desc'][:90]}")
