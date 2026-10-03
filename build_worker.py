#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cloudflare Worker Generator & Deployer
Builds and deploys the all-in-one Cloudflare Worker containing:
- Personalized User Subscriptions (/sub/u/:userId)
- Telegram WebApp Mini App (/app) with Incy & Happ 1-click install
- Telegram Bot Webhook (@hustler_vpn_robot) with menu button & inline keyboards
- 100% clean server naming (Flag + Country + Tag + Latency), zero "бесплатный", zero fake CDN
"""

import os
import sys
import json
import urllib.request
import base64
from typing import List, Dict, Any

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
ALIVE_FILE = os.path.join(DATA_DIR, "alive_servers.json")

# Load environment variables from .env if present
_env_path = os.path.join(BASE_DIR, ".env")
if os.path.exists(_env_path):
    with open(_env_path, "r", encoding="utf-8") as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                os.environ.setdefault(_k.strip(), _v.strip())

CLOUDFLARE_ACCOUNT_ID = os.getenv("CF_ACCOUNT_ID", "0cce12c9f195e5f0bfe609e85d1a810e")
CLOUDFLARE_API_TOKEN = os.getenv("CF_API_TOKEN", "")
WORKER_NAME = os.getenv("CF_WORKER_NAME", "vless-hub")
TELEGRAM_BOT_TOKEN = os.getenv("TG_BOT_TOKEN", "8869884346:AAGZ0zL0_znst6qZo27fdYMKBeZGleOZAEg")


def load_servers() -> List[Dict[str, Any]]:
    if not os.path.exists(ALIVE_FILE):
        print("[!] alive_servers.json не найден, запустите сначала сканирование серверов")
        return []
    with open(ALIVE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    raw_servers = data.get("servers", [])
    valid = [
        s for s in raw_servers
        if s.get("is_alive", True)
        and s.get("protocol") == "vless"
        and s.get("security") in ("reality", "tls")
    ]
    def s_key(x):
        if x.get("is_whitelist"):
            prio = 2
        elif x.get("country_code") == "RU":
            prio = 1
        else:
            prio = 0
        lat = x.get("latency_ms", 99999)
        if lat <= 0:
            lat = 99999
        return (prio, lat)

    valid.sort(key=s_key)
    return valid


def generate_worker_js(servers: List[Dict[str, Any]]) -> str:
    servers_json = json.dumps(servers, ensure_ascii=False)

    js_code = f"""/**
 * 🍄 HUSTLER VPN • Cloudflare Smart Hub & Telegram Bot
 * Features:
 * - Telegram WebApp Mini App (/app)
 * - Personalized User Subscriptions (/sub/u/:userId)
 * - 1-Click "Добавить в Incy" & "Добавить в Happ"
 * - 100% Clean Server Names (Flag + Country Name + Tag + Ping)
 * - Auto-Failover per country
 */

const BOT_TOKEN = "{TELEGRAM_BOT_TOKEN}";
const SYNC_SECRET = "hustler_secret_2026";

// Verified server pool with clean remarks
let CACHED_SERVERS = {servers_json};

addEventListener('fetch', event => {{
  event.respondWith(handleRequest(event.request));
}});

async function handleRequest(request) {{
  const url = new URL(request.url);
  const path = url.pathname.replace(/\\/+$/, '') || '/';
  const origin = url.origin;

  // 1. Telegram Webhook
  if (path === '/webhook/telegram' && request.method === 'POST') {{
    return handleTelegramWebhook(request, origin);
  }}

  // 2. Telegram WebApp Mini App (Opens directly inside Telegram)
  if (path === '/app') {{
    return serveMiniApp(request, origin);
  }}

  // 3. Dynamic Data Sync API (for automated background checker)
  if (path === '/api/sync' && request.method === 'POST') {{
    return handleSync(request);
  }}

  // 4. Setup Telegram Webhook & Menu Button
  if (path === '/setup-telegram') {{
    return setupTelegramWebhook(origin);
  }}

  // 5. API Stats
  if (path === '/api/stats') {{
    return new Response(JSON.stringify(getStats()), {{
      headers: {{ 'Content-Type': 'application/json; charset=utf-8', 'Access-Control-Allow-Origin': '*' }}
    }});
  }}

  // 6. Personal User Subscriptions (/sub/u/:userId)
  if (path.startsWith('/sub/u/')) {{
    const userId = path.replace('/sub/u/', '').split('/')[0] || 'default';
    return servePersonalSub(userId, 'Incy');
  }}

  // 7. General Subscriptions (Foreign first, RU middle, Whitelist at bottom)
  if (path === '/sub' || path === '/sub/all' || path === '/sub/incy') {{
    return serveBase64Sub(getOrderedServers(), 'Incy-Universal');
  }}
  if (path === '/sub/happ') {{
    return serveBase64Sub(getOrderedServers(), 'Happ-Universal');
  }}
  if (path === '/sub/whitelist') {{
    const wl = CACHED_SERVERS.filter(s => s.is_whitelist);
    return serveBase64Sub(wl.length > 0 ? wl : CACHED_SERVERS, 'Whitelist-Обход');
  }}
  if (path === '/sub/gaming') {{
    const gaming = CACHED_SERVERS.filter(s => !s.is_whitelist && s.country_code !== 'RU' && s.latency_ms > 0 && s.latency_ms <= 85);
    return serveBase64Sub(gaming.length > 0 ? gaming : CACHED_SERVERS.slice(0, 30), 'Gaming-LowPing');
  }}
  if (path === '/sub/top3') {{
    const top3 = getTop3PerCountry();
    return serveBase64Sub(top3, 'Top3-Country');
  }}
  if (path.startsWith('/sub/country/')) {{
    const cc = path.replace('/sub/country/', '').toUpperCase();
    const cServers = CACHED_SERVERS.filter(s => s.country_code === cc);
    return serveBase64Sub(cServers, `Country-${{cc}}`);
  }}

  // 8. Direct 1-Click Keys
  // ⚡ Самый первый: Лучший зарубежный сервер (Обязательно НЕ Россия!)
  if (path === '/best') {{
    const best = getBestForeignServer();
    return new Response(best ? best.uri : 'No servers available', {{ headers: {{ 'Content-Type': 'text/plain; charset=utf-8' }} }});
  }}
  if (path === '/best-whitelist') {{
    const bestWl = getBestWhitelistServer();
    return new Response(bestWl ? bestWl.uri : 'No servers available', {{ headers: {{ 'Content-Type': 'text/plain; charset=utf-8' }} }});
  }}
  if (path === '/best-gaming') {{
    const bestGame = getBestGamingServer();
    return new Response(bestGame ? bestGame.uri : 'No servers available', {{ headers: {{ 'Content-Type': 'text/plain; charset=utf-8' }} }});
  }}

  // 9. Clash Meta & Singbox
  if (path === '/clash') {{
    return serveClashMeta();
  }}
  if (path === '/singbox') {{
    return serveSingbox();
  }}

  // 10. Default Dashboard
  return serveDashboard(origin);
}}

// =========================================================================
// Subscription Delivery & 3-Tier Ordering
// =========================================================================
function getOrderedServers() {{
  const foreign = CACHED_SERVERS.filter(s => !s.is_whitelist && s.country_code !== 'RU').sort((a,b) => (a.latency_ms||999) - (b.latency_ms||999));
  const foreignWl = CACHED_SERVERS.filter(s => s.is_whitelist && s.country_code !== 'RU').sort((a,b) => (a.latency_ms||999) - (b.latency_ms||999));
  const ru = CACHED_SERVERS.filter(s => !s.is_whitelist && s.country_code === 'RU').sort((a,b) => (a.latency_ms||999) - (b.latency_ms||999));
  const ruWl = CACHED_SERVERS.filter(s => s.is_whitelist && s.country_code === 'RU').sort((a,b) => (a.latency_ms||999) - (b.latency_ms||999));
  return [...foreign, ...foreignWl, ...ru, ...ruWl];
}}

function getBestForeignServer() {{
  return CACHED_SERVERS.find(s => !s.is_whitelist && s.country_code !== 'RU') || CACHED_SERVERS[0];
}}

function getBestGamingServer() {{
  return CACHED_SERVERS.find(s => !s.is_whitelist && s.country_code !== 'RU' && s.latency_ms > 0 && s.latency_ms <= 85) || getBestForeignServer();
}}

function getBestWhitelistServer() {{
  return CACHED_SERVERS.find(s => s.is_whitelist) || CACHED_SERVERS[0];
}}

function servePersonalSub(userId, clientName) {{
  const servers = getTop3PerCountry();
  const uris = servers.map((s, idx) => {{
    let cleanRemark = "";
    if (idx === 0 && !s.is_whitelist && s.country_code !== 'RU') {{
      cleanRemark = `⚡ Лучший зарубежный сервер (Мин. пинг) • ${{s.country_flag || '🌐'}} ${{s.country_name || ''}} • ${{s.latency_ms}}ms`;
    }} else {{
      const flag = s.country_flag || '🌐';
      const cName = s.country_name || s.country_code || 'VPN';
      let tag = "";
      if (s.is_whitelist) {{
        tag = s.country_code !== 'RU' ? ` [${{s.whitelist_label || '🛡️ Обход'}} • Зарубежный]` : ` [${{s.whitelist_label || '🛡️ Обход'}} • РФ]`;
      }} else if (s.latency_ms <= 85 && s.latency_ms > 0) {{
        tag = ' [🎮 Игровой]';
      }}
      const ping = s.latency_ms > 0 ? ` • ${{s.latency_ms}}ms` : '';
      cleanRemark = `${{flag}} ${{cName}}${{tag}} #${{idx+1}}${{ping}}`;
    }}
    const baseUri = s.uri.split('#')[0];
    return `${{baseUri}}#${{encodeURIComponent(cleanRemark)}}`;
  }}).filter(Boolean);

  const plainText = uris.join('\\n');
  const base64Text = btoa(unescape(encodeURIComponent(plainText)));

  return new Response(base64Text, {{
    headers: {{
      'Content-Type': 'text/plain; charset=utf-8',
      'Access-Control-Allow-Origin': '*',
      'Subscription-Userinfo': 'upload=0; download=0; total=1073741824000; expire=0',
      'profile-update-interval': '6',
      'Content-Disposition': `inline; filename="sub_user_${{userId}}.txt"`
    }}
  }});
}}

function serveBase64Sub(servers, label) {{
  const uris = servers.map((s, idx) => {{
    let cleanRemark = "";
    if (idx === 0 && !s.is_whitelist && s.country_code !== 'RU') {{
      cleanRemark = `⚡ Лучший зарубежный сервер (Мин. пинг) • ${{s.country_flag || '🌐'}} ${{s.country_name || ''}} • ${{s.latency_ms}}ms`;
    }} else {{
      const flag = s.country_flag || '🌐';
      const cName = s.country_name || s.country_code || 'VPN';
      let tag = "";
      if (s.is_whitelist) {{
        tag = s.country_code !== 'RU' ? ` [${{s.whitelist_label || '🛡️ Обход'}} • Зарубежный]` : ` [${{s.whitelist_label || '🛡️ Обход'}} • РФ]`;
      }} else if (s.latency_ms <= 85 && s.latency_ms > 0) {{
        tag = ' [🎮 Игровой]';
      }}
      const ping = s.latency_ms > 0 ? ` • ${{s.latency_ms}}ms` : '';
      cleanRemark = `${{flag}} ${{cName}}${{tag}} #${{idx+1}}${{ping}}`;
    }}
    const baseUri = s.uri.split('#')[0];
    return `${{baseUri}}#${{encodeURIComponent(cleanRemark)}}`;
  }}).filter(Boolean);

  const plainText = uris.join('\\n');
  const base64Text = btoa(unescape(encodeURIComponent(plainText)));

  return new Response(base64Text, {{
    headers: {{
      'Content-Type': 'text/plain; charset=utf-8',
      'Access-Control-Allow-Origin': '*',
      'Subscription-Userinfo': 'upload=0; download=0; total=1073741824000; expire=0',
      'profile-update-interval': '6',
      'Content-Disposition': `inline; filename="sub_${{encodeURIComponent(label)}}.txt"`
    }}
  }});
}}

function getTop3PerCountry() {{
  const ordered = getOrderedServers();
  const byCountry = {{}};
  const result = [];
  for (const s of ordered) {{
    const cc = s.country_code || 'OTHER';
    if (!byCountry[cc]) byCountry[cc] = 0;
    if (byCountry[cc] < 3) {{
      byCountry[cc]++;
      result.push(s);
    }}
  }}
  return result;
}}

function getStats() {{
  const total = CACHED_SERVERS.length;
  const wlCount = CACHED_SERVERS.filter(s => s.is_whitelist).length;
  const gamingCount = CACHED_SERVERS.filter(s => !s.is_whitelist && s.country_code !== 'RU' && s.latency_ms > 0 && s.latency_ms <= 85).length;
  const pings = CACHED_SERVERS.map(s => s.latency_ms).filter(p => p > 0);
  const avgPing = pings.length > 0 ? Math.round(pings.reduce((a, b) => a + b, 0) / pings.length) : 0;
  const countries = [...new Set(CACHED_SERVERS.map(s => s.country_code).filter(c => c && c !== 'OTHER'))];

  return {{
    total,
    alive_count: total,
    whitelist_count: wlCount,
    gaming_count: gamingCount,
    avg_ping: avgPing,
    countries_count: countries.length,
    countries,
    best_server: getBestForeignServer(),
    best_whitelist: getBestWhitelistServer(),
    best_gaming: getBestGamingServer()
  }};
}}

// =========================================================================
// Telegram Bot Webhook & Mini App
// =========================================================================
async function setupTelegramWebhook(origin) {{
  const hookUrl = `${{origin}}/webhook/telegram`;
  const tgRes = await fetch(`https://api.telegram.org/bot${{BOT_TOKEN}}/setWebhook?url=${{encodeURIComponent(hookUrl)}}&drop_pending_updates=true`);
  const tgData = await tgRes.json();

  // Set native menu button to open WebApp
  await fetch(`https://api.telegram.org/bot${{BOT_TOKEN}}/setChatMenuButton`, {{
    method: 'POST',
    headers: {{ 'Content-Type': 'application/json' }},
    body: JSON.stringify({{
      menu_button: {{
        type: 'web_app',
        text: '🍄 VPN Hub',
        web_app: {{ url: `${{origin}}/app` }}
      }}
    }})
  }});

  return new Response(JSON.stringify({{ status: 'ok', webhook: hookUrl, telegram: tgData }}), {{
    headers: {{ 'Content-Type': 'application/json; charset=utf-8' }}
  }});
}}

async function handleTelegramWebhook(request, origin) {{
  try {{
    const update = await request.json();
    if (update.message) {{
      await handleMessage(update.message, origin);
    }} else if (update.callback_query) {{
      await handleCallback(update.callback_query, origin);
    }}
  }} catch (e) {{
    console.error('Telegram webhook error:', e);
  }}
  return new Response('OK');
}}

async function sendTelegram(method, payload) {{
  const url = `https://api.telegram.org/bot${{BOT_TOKEN}}/${{method}}`;
  return fetch(url, {{
    method: 'POST',
    headers: {{ 'Content-Type': 'application/json' }},
    body: JSON.stringify(payload)
  }});
}}

async function handleMessage(msg, origin) {{
  const chatId = msg.chat.id;
  const userId = msg.from.id;
  const firstName = msg.from.first_name || 'Друг';
  const text = msg.text || '';

  if (text.startsWith('/start') || text.startsWith('/help')) {{
    const personalSubUrl = `${{origin}}/sub/u/${{userId}}`;
    const appUrl = `${{origin}}/app?u=${{userId}}`;

    const welcome = `🍄 <b>HUSTLER VPN • Персональный Hub</b>\\n\\n` +
      `Привет, <b>${{firstName}}</b>! Для вас сгенерирована <b>личная подписка</b> без нерабочих узлов и без рекламы.\\n\\n` +
      `⚡ <b>Поддержка клиентов:</b> Incy (в приоритете) и Happ\\n` +
      `🛡️ <b>Белые списки РФ:</b> VK, Госуслуги, Яндекс (обход глушений)\\n` +
      `🎮 <b>Игровые узлы:</b> с минимальным пингом (&lt;65ms)\\n\\n` +
      `Нажмите <b>«🚀 Открыть VPN Hub»</b> ниже для удобного управления:`;

    const keyboard = {{
      inline_keyboard: [
        [
          {{ text: '🚀 Открыть VPN Hub (Incy / Happ)', web_app: {{ url: appUrl }} }}
        ],
        [
          {{ text: '⚡ Лучший зарубежный сервер (Мин. пинг)', callback_data: 'best_server' }}
        ],
        [
          {{ text: '📱 Добавить в Incy (1 клик)', callback_data: `sub_incy_${{userId}}` }},
          {{ text: '🚀 Добавить в Happ', callback_data: `sub_happ_${{userId}}` }}
        ],
        [
          {{ text: '🎮 Игровой сервер (<65ms)', callback_data: 'best_game' }},
          {{ text: '🌍 Топ-3 по странам', callback_data: `sub_top3_${{userId}}` }}
        ],
        [
          {{ text: '🛡️ Лучший белый список (Мин. пинг)', callback_data: 'best_wl' }}
        ]
      ]
    }};

    await sendTelegram('sendMessage', {{
      chat_id: chatId,
      text: welcome,
      parse_mode: 'HTML',
      reply_markup: keyboard
    }});
  }}
}}

async function handleCallback(cb, origin) {{
  const chatId = cb.message.chat.id;
  const data = cb.data;

  if (data.startsWith('sub_incy')) {{
    const userId = data.replace('sub_incy_', '') || cb.from.id;
    const subUrl = `${{origin}}/sub/u/${{userId}}`;
    const text = `📱 <b>Ваша личная подписка для Incy:</b>\\n\\n` +
      `1. Скопируйте ссылку подписки (нажмите на неё):\\n` +
      `<code>${{subUrl}}</code>\\n\\n` +
      `2. Откройте приложение <b>Incy</b>\\n` +
      `3. Нажмите <b>«+»</b> в правом верхнем углу → <b>«Импорт из буфера обмена»</b>\\n` +
      `4. Нажмите большую кнопку подключения!\\n\\n` +
      `<i>Все сервера гарантированно рабочие (проверены TLS handshake), с названиями стран и флагами.</i>`;

    await sendTelegram('sendMessage', {{ chat_id: chatId, text, parse_mode: 'HTML' }});
  }} else if (data.startsWith('sub_happ')) {{
    const userId = data.replace('sub_happ_', '') || cb.from.id;
    const subUrl = `${{origin}}/sub/u/${{userId}}`;
    const text = `🚀 <b>Ваша личная подписка для Happ:</b>\\n\\n` +
      `Скопируйте ссылку и вставьте в Happ:\\n` +
      `<code>${{subUrl}}</code>`;
    await sendTelegram('sendMessage', {{ chat_id: chatId, text, parse_mode: 'HTML' }});
  }} else if (data === 'best_server') {{
    const best = getBestForeignServer();
    if (best) {{
      const text = `⚡ <b>Лучший зарубежный сервер (Минимальный пинг):</b>\\n\\n` +
        `<b>Локация:</b> ${{best.country_flag}} ${{best.country_name}} (${{best.country_code}})\\n` +
        `<b>Пинг:</b> <code>${{best.latency_ms}} ms</code>\\n` +
        `<i>(Зарубежный сервер для свободного доступа: YouTube, Instagram, ChatGPT)</i>\\n\\n` +
        `Нажмите на ключ ниже, чтобы скопировать в Incy:\\n` +
        `<code>${{best.uri}}</code>`;
      await sendTelegram('sendMessage', {{ chat_id: chatId, text, parse_mode: 'HTML' }});
    }}
  }} else if (data === 'best_game') {{
    const bestGame = getBestGamingServer();
    if (bestGame) {{
      const text = `🎮 <b>Игровой зарубежный сервер с ультранизкой задержкой:</b>\\n\\n` +
        `<b>Локация:</b> ${{bestGame.country_flag}} ${{bestGame.country_name}}\\n` +
        `<b>Пинг:</b> <code>${{bestGame.latency_ms}} ms</code> (Brawl Stars, Discord, Онлайн-игры)\\n\\n` +
        `Нажмите для копирования:\\n` +
        `<code>${{bestGame.uri}}</code>`;
      await sendTelegram('sendMessage', {{ chat_id: chatId, text, parse_mode: 'HTML' }});
    }}
  }} else if (data === 'best_wl') {{
    const bestWl = getBestWhitelistServer();
    const foreignWl = CACHED_SERVERS.find(s => s.is_whitelist && s.country_code !== 'RU');
    if (bestWl) {{
      let text = `🛡️ <b>Лучший белый список (Минимальный пинг):</b>\\n\\n` +
        `<b>Локация:</b> ${{bestWl.country_flag}} ${{bestWl.country_name}}\\n` +
        `<b>Сервис маскировки:</b> ${{bestWl.whitelist_label || 'Белый список'}} (<code>${{bestWl.sni || 'yandex.ru'}}</code>)\\n` +
        `<b>Пинг:</b> <code>${{bestWl.latency_ms}} ms</code>\\n` +
        `<i>(Работает на мобильном интернете при любых глушениях операторов)</i>\\n\\n` +
        `Нажмите на ключ ниже, чтобы скопировать в Incy:\\n` +
        `<code>${{bestWl.uri}}</code>`;

      if (foreignWl && foreignWl.host !== bestWl.host) {{
        text += `\\n\\n🌐 <b>Зарубежный Whitelist (Обход + весь мировой интернет):</b>\\n` +
          `${{foreignWl.country_flag}} ${{foreignWl.country_name}} • ${{foreignWl.whitelist_label}} • ${{foreignWl.latency_ms}}ms\\n` +
          `<code>${{foreignWl.uri}}</code>`;
      }}

      await sendTelegram('sendMessage', {{ chat_id: chatId, text, parse_mode: 'HTML' }});
    }}
  }} else if (data.startsWith('sub_top3')) {{
    const userId = data.replace('sub_top3_', '') || cb.from.id;
    const subUrl = `${{origin}}/sub/top3`;
    const text = `🌍 <b>Подписка «Топ-3 по каждой стране»:</b>\\n\\n` +
      `Включает по 3 лучших сервера на каждую локацию:\\n` +
      `<code>${{subUrl}}</code>`;
    await sendTelegram('sendMessage', {{ chat_id: chatId, text, parse_mode: 'HTML' }});
  }}

  await sendTelegram('answerCallbackQuery', {{ callback_query_id: cb.id }});
}}

// =========================================================================
// Telegram WebApp Mini App (/app)
// =========================================================================
function serveMiniApp(request, origin) {{
  const url = new URL(request.url);
  const userId = url.searchParams.get('u') || 'user';
  const personalSubUrl = `${{origin}}/sub/u/${{userId}}`;
  const stats = getStats();

  const html = `<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>🍄 HUSTLER VPN Mini App</title>
  <script src="https://telegram.org/js/telegram-web-app.js"></script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #090d16;
      --card: rgba(18, 24, 38, 0.85);
      --border: rgba(255, 255, 255, 0.08);
      --cyan: #06b6d4;
      --emerald: #10b981;
      --purple: #8b5cf6;
      --text: #f8fafc;
      --text-sec: #94a3b8;
    }}
    * {{ margin:0; padding:0; box-sizing:border-box; -webkit-tap-highlight-color: transparent; }}
    body {{
      background: var(--bg);
      color: var(--text);
      font-family: 'Plus Jakarta Sans', sans-serif;
      padding: 16px;
      line-height: 1.4;
      min-height: 100vh;
    }}
    .header {{
      display: flex; align-items: center; justify-content: space-between;
      padding-bottom: 14px; border-bottom: 1px solid var(--border); margin-bottom: 16px;
    }}
    .user-pill {{
      font-size: 11px; background: rgba(255,255,255,0.06); padding: 4px 10px;
      border-radius: 99px; border: 1px solid var(--border); font-family: 'JetBrains Mono', monospace;
    }}
    .big-actions {{ display: flex; flex-direction: column; gap: 12px; margin-bottom: 18px; }}
    .btn-main {{
      display: flex; align-items: center; justify-content: center; gap: 10px;
      width: 100%; padding: 15px; border-radius: 14px; font-weight: 800; font-size: 15px;
      border: none; cursor: pointer; transition: all 0.2s; text-decoration: none;
    }}
    .btn-incy {{
      background: linear-gradient(135deg, var(--cyan), #0284c7); color: #fff;
      box-shadow: 0 4px 16px rgba(6,182,212,0.3);
    }}
    .btn-happ {{
      background: linear-gradient(135deg, var(--purple), #6366f1); color: #fff;
      box-shadow: 0 4px 16px rgba(139,92,246,0.3);
    }}
    .btn-main:active {{ transform: scale(0.98); }}

    .quick-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 18px; }}
    .btn-quick {{
      background: var(--card); border: 1px solid var(--border); border-radius: 12px;
      padding: 12px 10px; text-align: center; cursor: pointer; color: var(--text);
      font-size: 13px; font-weight: 700; display: flex; flex-direction: column; align-items: center; gap: 4px;
    }}
    .btn-quick:active {{ background: rgba(255,255,255,0.1); }}
    .btn-quick span {{ font-size: 11px; color: var(--text-sec); font-weight: 500; }}

    .sub-box {{
      background: var(--card); border: 1px solid var(--border); border-radius: 14px;
      padding: 14px; margin-bottom: 16px;
    }}
    .sub-input {{
      width: 100%; background: rgba(0,0,0,0.4); border: 1px solid var(--border);
      border-radius: 8px; padding: 10px; color: #fff; font-family: monospace; font-size: 12px;
      margin: 8px 0; outline: none;
    }}

    .modal-overlay {{
      position: fixed; inset: 0; background: rgba(0,0,0,0.8); backdrop-filter: blur(8px);
      display: none; align-items: center; justify-content: center; z-index: 100; padding: 20px;
    }}
    .modal-card {{
      background: #121826; border: 1px solid var(--cyan); border-radius: 18px;
      padding: 20px; width: 100%; max-width: 360px; text-align: center;
    }}
    .toast {{
      position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
      background: #1e293b; border: 1px solid var(--cyan); color: #fff; padding: 10px 18px;
      border-radius: 99px; font-weight: 700; font-size: 13px; display: none; z-index: 200;
    }}
  </style>
</head>
<body>
  <div class="header">
    <div>
      <h2 style="font-size:18px; font-weight:800;">🍄 HUSTLER VPN</h2>
      <p style="font-size:11px; color:var(--text-sec);">Сервера проверены • Без N/A</p>
    </div>
    <div class="user-pill" id="user-display">ID: ${{userId}}</div>
  </div>

  <!-- 1. Top Action: Best Foreign Server (Guaranteed Non-RU) -->
  <div style="background: linear-gradient(135deg, rgba(6,182,212,0.18), rgba(16,185,129,0.18)); border: 1.5px solid var(--cyan); border-radius: 16px; padding: 16px; margin-bottom: 12px; cursor: pointer;" onclick="copyDirectKey('${{origin}}/best', '⚡ Лучший зарубежный сервер скопирован!')">
    <div style="display:flex; justify-content:space-between; align-items:center;">
      <div>
        <div style="font-size:11px; color:var(--cyan); font-weight:800; text-transform:uppercase; letter-spacing:0.5px;">⚡ САМЫЙ БЫСТРЫЙ СЕРВЕР (НЕ РОССИЯ)</div>
        <div style="font-size:15px; font-weight:800; margin-top:2px;">${{stats.best_server ? `${{stats.best_server.country_flag}} ${{stats.best_server.country_name}} • ${{stats.best_server.latency_ms}}ms` : '⚡ Зарубежный узел'}}</div>
        <div style="font-size:11px; color:var(--text-sec); margin-top:2px;">YouTube, Instagram, ChatGPT без блокировок</div>
      </div>
      <button class="btn-main" style="width:auto; padding:10px 16px; font-size:12px; background:var(--cyan); color:#000; border-radius:10px;">Скопировать</button>
    </div>
  </div>

  <!-- 1b. Best Whitelist Server (Minimum Ping) -->
  <div style="background: linear-gradient(135deg, rgba(16,185,129,0.18), rgba(6,182,212,0.18)); border: 1.5px solid var(--emerald); border-radius: 16px; padding: 16px; margin-bottom: 16px; cursor: pointer;" onclick="copyDirectKey('${{origin}}/best-whitelist', '🛡️ Лучший белый список скопирован!')">
    <div style="display:flex; justify-content:space-between; align-items:center;">
      <div>
        <div style="font-size:11px; color:var(--emerald); font-weight:800; text-transform:uppercase; letter-spacing:0.5px;">🛡️ ЛУЧШИЙ БЕЛЫЙ СПИСОК (МИН. ПИНГ)</div>
        <div style="font-size:15px; font-weight:800; margin-top:2px;">${{stats.best_whitelist ? `${{stats.best_whitelist.country_flag}} ${{stats.best_whitelist.country_name}} • ${{stats.best_whitelist.whitelist_label || 'Обход'}} • ${{stats.best_whitelist.latency_ms}}ms` : '🛡️ Белый список'}}</div>
        <div style="font-size:11px; color:var(--text-sec); margin-top:2px;">Работает на мобильном интернете при любых глушениях операторов</div>
      </div>
      <button class="btn-main" style="width:auto; padding:10px 16px; font-size:12px; background:var(--emerald); color:#000; border-radius:10px;">Скопировать</button>
    </div>
  </div>

  <!-- 2. Primary Incy & Happ Buttons -->
  <div class="big-actions">
    <button class="btn-main btn-incy" onclick="installSub('Incy')">
      📱 Добавить подписку в Incy (1 клик)
    </button>
    <button class="btn-main btn-happ" onclick="installSub('Happ')">
      🚀 Добавить подписку в Happ
    </button>
  </div>

  <!-- 3. Quick foreign server picks -->
  <div style="font-size:12px; font-weight:700; color:var(--text-sec); text-transform:uppercase; margin-bottom:8px;">Быстрый выбор:</div>
  <div class="quick-grid">
    <div class="btn-quick" onclick="copyDirectKey('${{origin}}/best-gaming', '🎮 Игровой сервер скопирован!')">
      🎮 Игровой сервер
      <span>Низкий пинг (&lt;85ms)</span>
    </div>
    <div class="btn-quick" onclick="copyDirectKey('${{origin}}/sub/top3', '🌍 Топ-3 по странам скопировано!')">
      🌍 Топ-3 по странам
      <span>По 3 узла на страну</span>
    </div>
  </div>

  <!-- 4. Personal link box -->
  <div class="sub-box">
    <div style="display:flex; justify-content:space-between; font-size:12px; font-weight:700;">
      <span>🔗 Ваша персональная ссылка:</span>
      <span style="color:var(--emerald);">1 TB • Без лимитов</span>
    </div>
    <input type="text" readonly value="${{personalSubUrl}}" id="sub-url-input" class="sub-input">
    <button class="btn-main" style="background:rgba(255,255,255,0.08); padding:8px; font-size:12px;" onclick="copyInput()">
      Копировать ссылку подписки
    </button>
  </div>

  <!-- 5. Bottom Section: Russian Whitelist Bypass -->
  <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; padding: 14px; margin-top: 14px; margin-bottom: 16px;">
    <div style="display:flex; justify-content:space-between; align-items:center;">
      <div>
        <div style="font-size:11px; color:var(--emerald); font-weight:800; text-transform:uppercase;">🛡️ Сервера обхода белых списков РФ</div>
        <div style="font-size:13px; font-weight:700; margin-top:2px;">Маскировка: VK, Госуслуги, Яндекс, СМИ</div>
        <div style="font-size:11px; color:var(--text-sec);">Использовать при изолировании мобильной сети</div>
      </div>
      <button class="btn-main" style="width:auto; padding:8px 12px; font-size:11px; background:rgba(16,185,129,0.2); color:var(--emerald); border: 1px solid var(--emerald); border-radius:10px;" onclick="copyDirectKey('${{origin}}/best-whitelist', '🛡️ Whitelist сервер скопирован!')">Скопировать</button>
    </div>
  </div>

  <div id="toast" class="toast">Скопировано!</div>

  <!-- Instruction Modal -->
  <div class="modal-overlay" id="modal-inst">
    <div class="modal-card">
      <div style="font-size:36px; margin-bottom:10px;">✅</div>
      <h3 style="font-size:17px; margin-bottom:8px;">Подписка скопирована!</h3>
      <p style="font-size:13px; color:var(--text-sec); text-align:left; margin-bottom:16px;">
        1. Откройте приложение <b id="modal-app-name" style="color:var(--cyan);">Incy</b>.<br>
        2. Нажмите <b>«+»</b> в правом верхнем углу.<br>
        3. Выберите <b>«Импорт из буфера обмена»</b>.<br>
        4. Нажмите большую кнопку подключения!
      </p>
      <button class="btn-main btn-incy" onclick="closeModal()">Понятно, открыть Incy</button>
    </div>
  </div>

  <script>
    const tg = window.Telegram?.WebApp;
    if (tg) {{
      tg.ready();
      tg.expand();
      if (tg.initDataUnsafe?.user) {{
        document.getElementById('user-display').textContent = tg.initDataUnsafe.user.first_name || 'ID: ${{userId}}';
      }}
    }}

    const subUrl = "${{personalSubUrl}}";

    function installSub(appName) {{
      navigator.clipboard.writeText(subUrl);
      if (tg?.HapticFeedback) tg.HapticFeedback.notificationOccurred('success');
      showToast('Ссылка скопирована!');

      document.getElementById('modal-app-name').textContent = appName;
      document.getElementById('modal-inst').style.display = 'flex';

      // Deep link attempt
      if (appName === 'Incy') {{
        window.location.href = "incy://install-sub?url=" + encodeURIComponent(subUrl);
      }} else if (appName === 'Happ') {{
        window.location.href = "happ://install-sub?url=" + encodeURIComponent(subUrl);
      }}
    }}

    function copyInput() {{
      navigator.clipboard.writeText(subUrl);
      if (tg?.HapticFeedback) tg.HapticFeedback.notificationOccurred('success');
      showToast('Подписка скопирована!');
    }}

    async function copyDirectKey(url, msg) {{
      const res = await fetch(url);
      const text = await res.text();
      navigator.clipboard.writeText(text);
      if (tg?.HapticFeedback) tg.HapticFeedback.notificationOccurred('success');
      showToast(msg);
    }}

    function closeModal() {{
      document.getElementById('modal-inst').style.display = 'none';
      if (tg?.close) tg.close();
    }}

    function showToast(msg) {{
      const t = document.getElementById('toast');
      t.textContent = msg;
      t.style.display = 'block';
      setTimeout(() => t.style.display = 'none', 2200);
    }}
  </script>
</body>
</html>`;

  return new Response(html, {{
    headers: {{ 'Content-Type': 'text/html; charset=utf-8' }}
  }});
}}

// =========================================================================
// Data Sync API
// =========================================================================
async function handleSync(request) {{
  try {{
    const body = await request.json();
    if (body.secret !== SYNC_SECRET) {{
      return new Response(JSON.stringify({{ error: 'Unauthorized' }}), {{ status: 401 }});
    }}
    if (Array.isArray(body.servers) && body.servers.length > 0) {{
      CACHED_SERVERS = body.servers;
      return new Response(JSON.stringify({{ status: 'synced', count: CACHED_SERVERS.length }}), {{
        headers: {{ 'Content-Type': 'application/json' }}
      }});
    }}
  }} catch (e) {{
    return new Response(JSON.stringify({{ error: e.message }}), {{ status: 400 }});
  }}
  return new Response(JSON.stringify({{ error: 'Invalid data' }}), {{ status: 400 }});
}}

// =========================================================================
// Clash Meta & Singbox
// =========================================================================
function serveClashMeta() {{
  const proxies = CACHED_SERVERS.slice(0, 80).map((s, idx) => {{
    const name = `${{s.country_flag}} ${{s.country_name || s.country_code}} #${{idx+1}} • ${{s.latency_ms}}ms`;
    return `  - name: "${{name}}"
    type: vless
    server: ${{s.host}}
    port: ${{s.port}}
    uuid: ${{s.uuid}}
    network: ${{s.type || 'tcp'}}
    tls: ${{s.security === 'reality' || s.security === 'tls'}}
    flow: ${{s.flow || ''}}
    servername: ${{s.sni || s.host}}
    client-fingerprint: chrome
    reality-opts:
      public-key: ${{s.pbk || ''}}
      short-id: "${{s.sid || ''}}"
    udp: true`;
  }}).join('\\n');

  const names = CACHED_SERVERS.slice(0, 80).map((s, idx) => `      - "${{s.country_flag}} ${{s.country_name || s.country_code}} #${{idx+1}} • ${{s.latency_ms}}ms"`).join('\\n');

  const yaml = `# Generated by HUSTLER VPN Hub
port: 7890
socks-port: 7891
mode: rule
proxies:
${{proxies}}

proxy-groups:
  - name: "⚡ Авто-выбор (Лучший пинг)"
    type: url-test
    url: http://cp.cloudflare.com/generate_204
    interval: 60
    proxies:
${{names}}
  - name: "🚀 PROXY"
    type: select
    proxies:
      - "⚡ Авто-выбор (Лучший пинг)"
${{names}}

rules:
  - GEOIP,RU,DIRECT
  - MATCH,🚀 PROXY
`;
  return new Response(yaml, {{
    headers: {{ 'Content-Type': 'application/yaml; charset=utf-8', 'Content-Disposition': 'inline; filename="clash.yaml"' }}
  }});
}}

function serveSingbox() {{
  const outbounds = CACHED_SERVERS.slice(0, 50).map((s, idx) => ({{
    type: 'vless',
    tag: `${{s.country_flag}} ${{s.country_name || s.country_code}} #${{idx+1}} • ${{s.latency_ms}}ms`,
    server: s.host,
    server_port: s.port,
    uuid: s.uuid,
    tls: {{ enabled: true, server_name: s.sni || s.host }}
  }}));

  const tags = outbounds.map(o => o.tag);
  const config = {{
    version: 1,
    outbounds: [
      {{ type: 'selector', tag: 'select', outbounds: ['urltest', ...tags] }},
      {{ type: 'urltest', tag: 'urltest', outbounds: tags, url: 'https://www.gstatic.com/generate_204' }},
      ...outbounds
    ]
  }};
  return new Response(JSON.stringify(config, null, 2), {{
    headers: {{ 'Content-Type': 'application/json; charset=utf-8' }}
  }});
}}

// =========================================================================
// HTML Dashboard
// =========================================================================
function serveDashboard(origin) {{
  const stats = getStats();
  const html = `<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🍄 HUSTLER VPN • Cloudflare Hub</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #090d16;
      --card: rgba(18, 24, 38, 0.75);
      --border: rgba(255, 255, 255, 0.08);
      --cyan: #06b6d4;
      --emerald: #10b981;
      --purple: #8b5cf6;
      --amber: #f59e0b;
      --text: #f8fafc;
      --text-sec: #94a3b8;
    }}
    * {{ margin:0; padding:0; box-sizing:border-box; }}
    body {{
      background: var(--bg); color: var(--text); font-family: 'Plus Jakarta Sans', sans-serif;
      min-height: 100vh; padding: 24px; line-height: 1.5;
    }}
    .container {{ max-width: 1200px; margin: 0 auto; }}
    .header {{
      display: flex; justify-content: space-between; align-items: center; padding-bottom: 24px;
      border-bottom: 1px solid var(--border); margin-bottom: 24px; flex-wrap: wrap; gap: 16px;
    }}
    .brand {{ display: flex; align-items: center; gap: 14px; }}
    .brand h1 {{ font-size: 24px; font-weight: 800; }}
    .badge {{ font-size: 11px; background: linear-gradient(135deg, var(--cyan), var(--purple)); padding: 3px 8px; border-radius: 99px; }}
    .stats-row {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 14px; margin-bottom: 24px; }}
    .stat-card {{ background: var(--card); border: 1px solid var(--border); padding: 16px; border-radius: 14px; backdrop-filter: blur(10px); }}
    .stat-num {{ font-size: 24px; font-weight: 800; font-family: 'JetBrains Mono', monospace; color: var(--cyan); }}
    .stat-label {{ font-size: 12px; color: var(--text-sec); text-transform: uppercase; font-weight: 600; }}
    
    .quick-actions {{
      background: linear-gradient(135deg, rgba(6, 182, 212, 0.08), rgba(16, 185, 129, 0.08));
      border: 1px solid rgba(6, 182, 212, 0.3); padding: 20px; border-radius: 16px; margin-bottom: 24px;
    }}
    .actions-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 14px; margin-top: 14px; }}
    .btn {{
      display: inline-flex; align-items: center; justify-content: center; gap: 8px;
      padding: 12px 18px; border-radius: 10px; font-weight: 700; font-size: 14px;
      border: none; cursor: pointer; transition: all 0.2s; text-decoration: none;
    }}
    .btn-cyan {{ background: var(--cyan); color: #000; }}
    .btn-emerald {{ background: var(--emerald); color: #000; }}
    .btn-purple {{ background: var(--purple); color: #fff; }}
    .btn-outline {{ background: rgba(255,255,255,0.06); color: #fff; border: 1px solid var(--border); }}
    
    .cards-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px; margin-bottom: 24px; }}
    .card {{ background: var(--card); border: 1px solid var(--border); border-radius: 16px; padding: 20px; display: flex; flex-direction: column; }}
    .card h3 {{ font-size: 16px; margin-bottom: 8px; }}
    .card p {{ font-size: 13px; color: var(--text-sec); margin-bottom: 16px; flex-grow: 1; }}
    .input-box {{ display: flex; gap: 8px; }}
    .input-box input {{ flex: 1; background: rgba(0,0,0,0.4); border: 1px solid var(--border); border-radius: 8px; padding: 8px 12px; color: #fff; font-family: monospace; font-size: 12px; }}

    .toast {{
      position: fixed; bottom: 20px; right: 20px; background: #1e293b; border: 1px solid var(--cyan);
      color: #fff; padding: 12px 20px; border-radius: 10px; font-weight: 600; display: none; z-index: 1000;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="brand">
        <span style="font-size:32px;">🍄</span>
        <div>
          <h1>HUSTLER VPN • Cloudflare Hub <span class="badge">ONLINE</span></h1>
          <p style="color:var(--text-sec); font-size:13px;">Подписки для Incy &amp; Happ • Whitelist обходы • Telegram Bot @hustler_vpn_robot</p>
        </div>
      </div>
      <div>
        <a href="https://t.me/hustler_vpn_robot" target="_blank" class="btn btn-purple">🤖 Открыть Telegram Бота</a>
      </div>
    </div>

    <div class="stats-row">
      <div class="stat-card">
        <div class="stat-label">Рабочих серверов</div>
        <div class="stat-num">${{stats.total}}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Белые списки (Обход)</div>
        <div class="stat-num" style="color:var(--emerald);">${{stats.whitelist_count}}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Игровые узлы (&lt;85ms)</div>
        <div class="stat-num" style="color:var(--purple);">${{stats.gaming_count}}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Средний пинг</div>
        <div class="stat-num">${{stats.avg_ping}} ms</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Стран в базе</div>
        <div class="stat-num">${{stats.countries_count}}</div>
      </div>
    </div>

    <!-- Quick action buttons -->
    <div class="quick-actions">
      <h2 style="font-size:18px;">⚡ Быстрое подключение в 1 клик:</h2>
      <p style="font-size:13px; color:var(--text-sec);">Нажмите на кнопку — ключ скопируется в буфер для мгновенной вставки в Incy или Happ!</p>
      <div class="actions-grid">
        <button class="btn btn-cyan" onclick="copyUrl('${{origin}}/best', 'Лучший сервер скопирован!')">⚡ Скопировать лучший сервер (Мин. пинг)</button>
        <button class="btn btn-emerald" onclick="copyUrl('${{origin}}/best-whitelist', 'Лучший обход (Whitelist) скопирован!')">🛡️ Скопировать лучший обход (Whitelist)</button>
        <button class="btn btn-purple" onclick="copyUrl('${{origin}}/best-gaming', 'Игровой сервер скопирован!')">🎮 Скопировать игровой сервер</button>
      </div>
    </div>

    <!-- Subscriptions grid -->
    <div class="cards-grid">
      <div class="card" style="border-color:rgba(6,182,212,0.4);">
        <div style="font-size:11px; color:var(--cyan); font-weight:700; margin-bottom:4px;">ПРИОРИТЕТ ДЛЯ INCY</div>
        <h3>📱 Подписка для Incy</h3>
        <p>Все протестированные рабочие сервера. Нажмите «+» → «Импорт из буфера» в приложении Incy.</p>
        <div class="input-box">
          <input type="text" readonly value="${{origin}}/sub/incy" id="inp-incy">
          <button class="btn btn-cyan" style="padding:8px 14px;" onclick="copyInput('inp-incy')">Копировать</button>
        </div>
      </div>

      <div class="card" style="border-color:rgba(16,185,129,0.4);">
        <div style="font-size:11px; color:var(--emerald); font-weight:700; margin-bottom:4px;">ОБХОД ГЛУШЕНИЙ РФ</div>
        <h3>🛡️ Подписка Whitelist (Белые списки)</h3>
        <p>Сервера с маскировкой под VK, Госуслуги, Яндекс. Работают при жестких блокировках!</p>
        <div class="input-box">
          <input type="text" readonly value="${{origin}}/sub/whitelist" id="inp-wl">
          <button class="btn btn-emerald" style="padding:8px 14px;" onclick="copyInput('inp-wl')">Копировать</button>
        </div>
      </div>

      <div class="card">
        <div style="font-size:11px; color:var(--purple); font-weight:700; margin-bottom:4px;">ПО 3 НА СТРАНУ</div>
        <h3>🌍 Топ-3 по каждой стране</h3>
        <p>Компактная подписка, содержащая ровно по 3 лучших сервера на каждую страну с наименьшим пингом.</p>
        <div class="input-box">
          <input type="text" readonly value="${{origin}}/sub/top3" id="inp-top3">
          <button class="btn btn-purple" style="padding:8px 14px;" onclick="copyInput('inp-top3')">Копировать</button>
        </div>
      </div>

      <div class="card">
        <div style="font-size:11px; color:var(--amber); font-weight:700; margin-bottom:4px;">HAPP КЛИЕНТ</div>
        <h3>🚀 Подписка для Happ</h3>
        <p>Оптимизированная база проверенных серверов для клиента Happ.</p>
        <div class="input-box">
          <input type="text" readonly value="${{origin}}/sub/happ" id="inp-happ">
          <button class="btn btn-outline" style="padding:8px 14px;" onclick="copyInput('inp-happ')">Копировать</button>
        </div>
      </div>
    </div>
  </div>

  <div id="toast" class="toast">Ссылка скопирована!</div>

  <script>
    function copyInput(id) {{
      const el = document.getElementById(id);
      navigator.clipboard.writeText(el.value);
      showToast('Подписка скопирована в буфер обмена!');
    }}
    async function copyUrl(url, msg) {{
      const res = await fetch(url);
      const text = await res.text();
      navigator.clipboard.writeText(text);
      showToast(msg);
    }}
    function showToast(msg) {{
      const t = document.getElementById('toast');
      t.textContent = msg;
      t.style.display = 'block';
      setTimeout(() => t.style.display = 'none', 2500);
    }}
  </script>
</body>
</html>`;

  return new Response(html, {{
    headers: {{ 'Content-Type': 'text/html; charset=utf-8' }}
  }});
}}
"""
    return js_code


def deploy_to_cloudflare(script_content: str):
    print("\n[*] Загрузка обновленного Cloudflare Worker в аккаунт...")
    url = f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/workers/scripts/{WORKER_NAME}"
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/javascript"
    }

    req = urllib.request.Request(url, data=script_content.encode("utf-8"), headers=headers, method="PUT")
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("success"):
                print(f"[+] Worker успешно развернут на Cloudflare! (Размер: {len(script_content)} байт)")
            else:
                print(f"[!] Ошибка загрузки: {data}")
                return False
    except Exception as e:
        print(f"[!] Ошибка API Cloudflare: {e}")
        return False

    # Enable subdomain route
    sub_url = f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/workers/scripts/{WORKER_NAME}/subdomain"
    sub_data = json.dumps({"enabled": True}).encode("utf-8")
    sub_req = urllib.request.Request(sub_url, data=sub_data, headers={"Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}", "Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(sub_req) as resp:
            pass
    except Exception:
        pass

    worker_url = f"https://{WORKER_NAME}.danilkaponda.workers.dev"
    print(f"[+] Worker доступен онлайн: {worker_url}")

    # Configure Telegram Webhook and Menu Button
    print("[*] Настройка Telegram Webhook & Menu Button для @hustler_vpn_robot...")
    setup_url = f"{worker_url}/setup-telegram"
    try:
        req = urllib.request.Request(setup_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=10) as r:
            res_data = json.loads(r.read().decode("utf-8"))
            print(f"[+] Telegram Webhook & Menu Button настроены: {res_data.get('telegram')}")
    except Exception as e:
        print(f"[!] Ошибка настройки Webhook (попробуйте повторить): {e}")

    return True


def main():
    print("=" * 65)
    print(" 🍄 СБОРКА И ЗАГРУЗКА НА CLOUDFLARE WORKERS")
    print("=" * 65)

    servers = load_servers()
    print(f"[*] Проверенных серверов в пуле: {len(servers)}")

    script = generate_worker_js(servers)

    worker_file = os.path.join(BASE_DIR, "cloudflare", "worker.js")
    os.makedirs(os.path.dirname(worker_file), exist_ok=True)
    with open(worker_file, "w", encoding="utf-8") as f:
        f.write(script)
    print(f"[+] Локальный файл воркера сохранен: {worker_file}")

    deploy_to_cloudflare(script)


if __name__ == "__main__":
    main()
