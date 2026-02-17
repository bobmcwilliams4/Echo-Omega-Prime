@echo off
REM P01 Heirship Determiner - Startup Script
REM Port: 8651

echo ============================================================
echo P01 HEIRSHIP DETERMINER ENGINE
echo Texas Intestate Succession Analysis
echo Port: 8651
echo ============================================================
echo.

cd /d "%~dp0"

echo Starting engine...
"H:\Tools\PyManager\pythons\py311\python.exe" engine.py

pause
