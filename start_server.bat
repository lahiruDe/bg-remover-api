@echo off
echo Starting Background Remover API...
py -m uvicorn main:app --reload
pause
