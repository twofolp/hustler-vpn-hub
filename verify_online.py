import urllib.request
import base64
import urllib.parse
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

print("=== 1. BEST WHITELIST KEY (/best-whitelist) ===")
req = urllib.request.Request("https://vless-hub.danilkaponda.workers.dev/best-whitelist", headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
with urllib.request.urlopen(req) as r:
    key = r.read().decode("utf-8")
    rem = urllib.parse.unquote(key.split("#")[1]) if "#" in key else key[:60]
    print("STATUS:", r.status)
    print("KEY REMARK:", rem)

print("\n=== 2. WHITELIST MULTI-SUBSCRIPTION (/sub/whitelist) ===")
req = urllib.request.Request("https://vless-hub.danilkaponda.workers.dev/sub/whitelist", headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
with urllib.request.urlopen(req) as r:
    raw = r.read().strip()
    decoded = base64.b64decode(raw).decode("utf-8")
    lines = [l for l in decoded.splitlines() if l.strip()]
    print(f"TOTAL WHITELIST SERVERS: {len(lines)}")
    for i, l in enumerate(lines):
        rem = urllib.parse.unquote(l.split("#")[1]) if "#" in l else l[:50]
        print(f" {i+1}. {rem}")

print("\n=== 3. ALL SERVERS IN INCY SUB (/sub/incy) ===")
req = urllib.request.Request("https://vless-hub.danilkaponda.workers.dev/sub/incy", headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
with urllib.request.urlopen(req) as r:
    raw = r.read().strip()
    decoded = base64.b64decode(raw).decode("utf-8")
    lines = [l for l in decoded.splitlines() if l.strip()]
    print(f"TOTAL SERVERS IN INCY SUB: {len(lines)}")
    print("Top 3:")
    for l in lines[:3]:
        print("  ", urllib.parse.unquote(l.split("#")[1]))
    print("Whitelists section:")
    for l in lines:
        rem = urllib.parse.unquote(l.split("#")[1])
        if "обход" in rem.lower() or "whitelist" in rem.lower() or "яндекс" in rem.lower() or "список" in rem.lower():
            print("  ", rem)
