@echo off
echo Starting Market Basket Analysis Frontend...
cd frontend
echo Frontend will be available at: http://127.0.0.1:3000
python -m http.server 3000
pause