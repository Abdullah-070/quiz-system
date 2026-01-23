@echo off
REM Quick deployment script for Quiz System

echo.
echo ======================================
echo   Quiz System - Deployment Guide
echo ======================================
echo.

echo Step 1: Initialize Git (run once)
echo   git init
echo   git config user.email "your-email@example.com"
echo   git config user.name "Your Name"
echo   git add .
echo   git commit -m "Initial commit"
echo.

echo Step 2: Push to GitHub
echo   git remote add origin https://github.com/YOUR_USERNAME/interview-quiz.git
echo   git branch -M main
echo   git push -u origin main
echo.

echo Step 3: Deploy Backend to Render
echo   - Go to https://render.com
echo   - Sign up with GitHub
echo   - Click "New +" ^> "Web Service"
echo   - Connect your interview-quiz repository
echo   - Set Root Directory to: backend
echo   - Use settings from render.yaml
echo   - Click Deploy
echo   - Note your URL: https://quiz-system-backend-xxxx.onrender.com
echo.

echo Step 4: Update Frontend API URL
echo   - Edit frontend\.env.production
echo   - Change REACT_APP_API_URL to your Render URL
echo   - Example: https://quiz-system-backend-xxxx.onrender.com/api
echo.

echo Step 5: Rebuild and Deploy Frontend
cd /d "%~dp0frontend"
echo   npm run build
call npm run build
echo.
echo   npx firebase deploy
call npx firebase deploy
echo.

echo ======================================
echo   Deployment Complete!
echo ======================================
echo.
echo Access your app at: https://quiz-system-78263.web.app
echo.
pause
