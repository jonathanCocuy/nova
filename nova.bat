@echo off
title NOVA: SISTEMA ACTIVO
echo Iniciando protocolos NOVA...
cd /d %~dp0
.\venv\Scripts\python.exe nova.py
pause