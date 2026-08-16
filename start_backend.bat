@echo off
echo Starting Market Basket Analysis Backend...
cd backend
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
pause