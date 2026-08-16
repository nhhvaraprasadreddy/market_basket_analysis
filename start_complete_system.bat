@echo off
echo ========================================
echo  Market Basket Analysis System Startup
echo ========================================
echo.

echo [1/3] Installing Python dependencies...
cd backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [2/3] Starting Backend Server...
echo Backend will be available at: http://127.0.0.1:8000
echo API endpoint: http://127.0.0.1:8000/api/analyze
echo.
start "Backend Server" cmd /k "uvicorn app:app --host 0.0.0.0 --port 8000 --reload"

echo Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo.
echo [3/3] Starting Frontend Server...
cd ..\frontend
echo Frontend will be available at: http://127.0.0.1:3000
echo.
start "Frontend Server" cmd /k "python -m http.server 3000"

echo.
echo ========================================
echo  System Started Successfully!
echo ========================================
echo.
echo Backend:  http://127.0.0.1:8000
echo Frontend: http://127.0.0.1:3000
echo.
echo Open your browser and go to: http://127.0.0.1:3000
echo.
echo Press any key to exit this window...
pause > nul