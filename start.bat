@echo off
chcp 65001 >nul
title 🍄 VLESS По Грибы • Smart Hub
echo =====================================================================
echo  🍄 VLESS По Грибы • Smart Hub & Auto-Failover Server
echo =====================================================================
echo.
echo Запуск веб-панели и мультиподписок...
echo Панель откроется в браузере по адресу: http://localhost:8088
echo.

start "" http://localhost:8088
python main.py serve --port 8088

pause
