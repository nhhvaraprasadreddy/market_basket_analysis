@echo off
echo 🚀 Deploying Market Basket Analysis Application...

echo.
echo 📦 Building SAM application...
sam build

if %ERRORLEVEL% neq 0 (
    echo ❌ Build failed!
    pause
    exit /b 1
)

echo.
echo ☁️ Deploying to AWS...
sam deploy --guided

if %ERRORLEVEL% neq 0 (
    echo ❌ Deployment failed!
    pause
    exit /b 1
)

echo.
echo ✅ Deployment completed!
echo.
echo 📝 Next steps:
echo 1. Note the API Gateway URL from the outputs above
echo 2. Update frontend/script.js with the API endpoint
echo 3. Upload frontend files to S3:
echo    aws s3 sync frontend/ s3://YOUR-BUCKET-NAME --delete
echo.
pause