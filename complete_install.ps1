# Simple installation script for Text-Based CRM Opportunity Extractor

Write-Host "=== Text-Based CRM Opportunity Extractor - Installation ===" -ForegroundColor Green
Write-Host "This script will set up everything needed to run the application." -ForegroundColor Cyan

# Check if Python is installed
try {
    $pythonVersion = python --version
    Write-Host "Python detected: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "Python not found. Please install Python 3.8 or higher." -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Cyan
if (Test-Path -Path "venv") {
    Write-Host "Virtual environment already exists." -ForegroundColor Yellow
}
else {
    python -m venv venv
}

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

# Download Mistral model
$modelPath = "models\mistral-7b-instruct-v0.2.Q4_K_M.gguf"
if (-not (Test-Path -Path $modelPath)) {
    Write-Host "Downloading Mistral 7B model (about 4.1GB)..." -ForegroundColor Cyan
    Write-Host "This may take a while depending on your internet connection." -ForegroundColor Yellow
    
    $modelUrl = "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
    
    try {
        $webClient = New-Object System.Net.WebClient
        $webClient.DownloadFile($modelUrl, $modelPath)
        Write-Host "Model downloaded successfully." -ForegroundColor Green
    }
    catch {
        Write-Host "Failed to download model: $_" -ForegroundColor Red
        Write-Host "You can manually download it later from:" -ForegroundColor Yellow
        Write-Host "$modelUrl" -ForegroundColor Yellow
    }
}
else {
    Write-Host "Mistral 7B model already exists." -ForegroundColor Green
}

# Install ctransformers
if (Test-Path -Path $modelPath) {
    Write-Host "Installing ctransformers for model support..." -ForegroundColor Cyan
    pip install ctransformers
}

# Create start_app.bat
Write-Host "Creating startup batch file..." -ForegroundColor Cyan
$startAppContent = @"
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
"@

Set-Content -Path "start_app.bat" -Value $startAppContent

# Installation complete
Write-Host "=== Installation Complete! ===" -ForegroundColor Green
Write-Host "To start the application, run start_app.bat" -ForegroundColor Cyan
Write-Host "Once started, open your browser and go to: http://127.0.0.1:5000/" -ForegroundColor Cyan
