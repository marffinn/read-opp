# Simple installation script for Text-Based CRM Opportunity Extractor

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Cyan
python -m venv venv

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& .\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt

# Create directories
Write-Host "Creating necessary directories..." -ForegroundColor Cyan
if (-not (Test-Path -Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
}
if (-not (Test-Path -Path "extraction_results")) {
    New-Item -ItemType Directory -Path "extraction_results" | Out-Null
}
if (-not (Test-Path -Path "models")) {
    New-Item -ItemType Directory -Path "models" | Out-Null
}

# Set up environment files
Write-Host "Setting up environment files..." -ForegroundColor Cyan
if (-not (Test-Path -Path ".env") -and (Test-Path -Path ".env.example")) {
    Copy-Item -Path ".env.example" -Destination ".env"
}

# Create start_app.bat
Write-Host "Creating startup batch file..." -ForegroundColor Cyan
@"
@echo off
echo ===================================================
echo   Text-Based CRM Opportunity Extractor
echo ===================================================
echo.
echo Starting application...
echo.
echo The browser will open automatically when the server is ready.
echo If it doesn't, manually navigate to: http://127.0.0.1:5000/
echo.
echo Press Ctrl+C to stop the server when you're done.
echo ===================================================
echo.

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Start the application in the background
start /B python simple_app.py

:: Wait for the server to start
echo Waiting for server to start...
timeout /t 3 /nobreak > nul

:: Open the browser
echo Opening browser...
start http://127.0.0.1:5000/

:: Keep the window open to show logs
echo.
echo Server is running. Press Ctrl+C to stop.
echo.

:: Wait for user to press Ctrl+C
cmd /k
"@ | Out-File -FilePath "start_app.bat" -Encoding ascii

# Installation complete
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host "To start the application, run start_app.bat" -ForegroundColor Cyan
