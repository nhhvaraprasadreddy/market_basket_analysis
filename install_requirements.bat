@echo off
echo 🔧 Installing Market Basket Analysis Project Requirements...
echo.

echo 📦 Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)
echo ✅ Python is installed
echo.

echo 📦 Upgrading pip...
python -m pip install --upgrade pip
echo.

echo 📦 Installing backend dependencies...
cd backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install backend dependencies
    pause
    exit /b 1
)
echo ✅ Backend dependencies installed successfully
echo.

cd ..
echo 🧪 Testing installation...
python -c "import fastapi, uvicorn, pandas, mlxtend, numpy, boto3, mangum, requests; print('✅ All dependencies installed successfully!')"
if %errorlevel% neq 0 (
    echo ❌ Some dependencies failed to import
    pause
    exit /b 1
)
echo.

echo 🎉 Installation completed successfully!
echo.
echo 📋 Next steps:
echo 1. Run 'start_backend.bat' to start the backend server
echo 2. Run 'start_frontend.bat' to start the frontend server
echo 3. Open http://127.0.0.1:5500 in your browser
echo.
pause