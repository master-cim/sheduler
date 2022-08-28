@echo off

call %~dp0sheduler\venv\Scripts\activate

cd %~dp0sheduler

set TOKEN=5509395855:AAGU2ztLCPAh9KOUpSiqp0By3SgCjS-ITJU

python bot_telegram.py

pause