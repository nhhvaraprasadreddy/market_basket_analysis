@echo off
echo ========================================
echo  Starting Backend Server Only
echo ========================================
echo.

cd backend
echo Installing dependencies...
pip install -r requirements.txt
echo.

echo Starting FastAPI backend server...
echo Backend URL: http://127.0.0.1:8000
echo API Docs: http://127.0.0.1:8000/docs
echo Health Check: http://127.0.0.1:8000/health
echo.

uvicorn app:app --host 0.0.0.0 --port 8000 --reload