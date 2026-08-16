@echo off
echo ========================================
echo  Starting Frontend Server Only
echo ========================================
echo.

cd frontend
echo Starting Python HTTP server...
echo Frontend URL: http://127.0.0.1:5500
echo Test Page: http://127.0.0.1:5500/test.html
echo Main App: http://127.0.0.1:5500/index.html
echo.

python -m http.server 5500