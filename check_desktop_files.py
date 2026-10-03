import os
import re
import sys

for fpath in [r"C:\Users\twofolp\Desktop\впн.txt", r"C:\Users\twofolp\Desktop\отсортировать надо.txt"]:
    if not os.path.exists(fpath):
        print("Not found:", fpath)
        continue
    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    uris = re.findall(r"vless://[^\s<>\"\'\n]+", content)
    reality = [u for u in uris if "security=reality" in u]
    wl = [u for u in uris if any(k in u.lower() for k in ["yandex.ru", "vk.com", "gosuslugi", "dzen.ru", "mail.ru", "dobro.ru", "utiltools"])]
    print(f"{os.path.basename(fpath)}: Total={len(uris)}, Reality={len(reality)}, Whitelist={len(wl)}")
