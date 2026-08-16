@echo off
echo ========================================
echo  Market Basket Analysis System Startup
echo ========================================
echo.
echo Starting Backend Server...
start "MBA Backend" cmd /k "cd backend && uvicorn app:app --host 0.0.0.0 --port 8000 --reload"
echo.
echo Waiting 3 seconds for backend to start...
timeout /t 3 /nobreak >nul
echo.
echo Starting Frontend Server...
start "MBA Frontend" cmd /k "cd frontend && echo Frontend available at: http://127.0.0.1:5500 && python -m http.server 5500"
echo.
echo ========================================
echo  System Started Successfully!
echo ========================================
echo.
echo Backend:  http://127.0.0.1:8000
echo Frontend: http://127.0.0.1:5500
echo.
echo Press any key to close this window...
pause >nul