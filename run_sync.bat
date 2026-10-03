@echo off
chcp 65001 >nul
title 🚀 Синхронизация серверов с Cloudflare Workers
echo =====================================================================
echo  🚀 Запуск проверки серверов и обновления Cloudflare Worker
echo =====================================================================
echo.
python sync_cloudflare.py 500
echo.
pause
