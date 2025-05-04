# Text-Based CRM Opportunity Extractor - Installation Script
# This script sets up the environment and installs all dependencies

# Set error action preference to stop on any error
$ErrorActionPreference = "Stop"

Write-Host "=== Text-Based CRM Opportunity Extractor - Installation ===" -ForegroundColor Green
Write-Host "This script will set up everything needed to run the application." -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version
    Write-Host "✓ Python detected: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "✗ Python not found. Please install Python 3.8 or higher." -ForegroundColor Red
    Write-Host "  Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Create virtual environment
Write-Host "`nCreating virtual environment..." -ForegroundColor Cyan
if (Test-Path -Path "venv") {
    Write-Host "  Virtual environment already exists." -ForegroundColor Yellow
}
else {
    try {
        python -m venv venv
        Write-Host "✓ Virtual environment created successfully." -ForegroundColor Green
    }
    catch {
        Write-Host "✗ Failed to create virtual environment: $_" -ForegroundColor Red
        exit 1
    }
}

# Activate virtual environment
Write-Host "`nActivating virtual environment..." -ForegroundColor Cyan
try {
    & .\venv\Scripts\Activate.ps1
    Write-Host "✓ Virtual environment activated." -ForegroundColor Green
}
catch {
    Write-Host "✗ Failed to activate virtual environment: $_" -ForegroundColor Red
    Write-Host "  Try running this script with administrator privileges or run:" -ForegroundColor Yellow
    Write-Host "  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
    exit 1
}

# Install dependencies
Write-Host "`nInstalling dependencies..." -ForegroundColor Cyan
try {
    pip install -r requirements.txt
    Write-Host "✓ Dependencies installed successfully." -ForegroundColor Green
}
catch {
    Write-Host "✗ Failed to install dependencies: $_" -ForegroundColor Red
    exit 1
}

# Create directories
Write-Host "`nCreating necessary directories..." -ForegroundColor Cyan
if (-not (Test-Path -Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
}
if (-not (Test-Path -Path "extraction_results")) {
    New-Item -ItemType Directory -Path "extraction_results" | Out-Null
}
if (-not (Test-Path -Path "models")) {
    New-Item -ItemType Directory -Path "models" | Out-Null
}
Write-Host "✓ Directories created." -ForegroundColor Green

# Check if model exists and offer to download
$modelPath = "models\mistral-7b-instruct-v0.2.Q4_K_M.gguf"
if (-not (Test-Path -Path $modelPath)) {
    Write-Host "`nModel file not found: $modelPath" -ForegroundColor Yellow
    Write-Host "The application will work without the model using rule-based extraction," -ForegroundColor Yellow
    Write-Host "but AI-based extraction will be more accurate." -ForegroundColor Yellow

    $downloadChoice = Read-Host "`nWould you like to download the model now? (y/n)"
    if ($downloadChoice -eq "y" -or $downloadChoice -eq "Y") {
        Write-Host "`nDownloading Mistral 7B model (about 4.1GB)..." -ForegroundColor Cyan
        Write-Host "This may take a while depending on your internet connection." -ForegroundColor Yellow

        try {
            $modelUrl = "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
            $webClient = New-Object System.Net.WebClient
            $webClient.DownloadFile($modelUrl, $modelPath)
            Write-Host "✓ Model downloaded successfully." -ForegroundColor Green
        }
        catch {
            Write-Host "✗ Failed to download model: $_" -ForegroundColor Red
            Write-Host "  You can manually download it later from:" -ForegroundColor Yellow
            Write-Host "  $modelUrl" -ForegroundColor Yellow
        }
    }
    else {
        Write-Host "`nSkipping model download." -ForegroundColor Yellow
        Write-Host "You can manually download it later from:" -ForegroundColor Yellow
        Write-Host "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf" -ForegroundColor Yellow
    }
}

# Install ctransformers if model exists
if (Test-Path -Path $modelPath) {
    Write-Host "`nInstalling ctransformers for model support..." -ForegroundColor Cyan
    try {
        pip install ctransformers
        Write-Host "✓ ctransformers installed successfully." -ForegroundColor Green
    }
    catch {
        Write-Host "✗ Failed to install ctransformers: $_" -ForegroundColor Red
        Write-Host "  You can manually install it later with:" -ForegroundColor Yellow
        Write-Host "  pip install ctransformers" -ForegroundColor Yellow
    }
}

# Create start_app.bat if it doesn't exist
if (-not (Test-Path -Path "start_app.bat")) {
    Write-Host "`nCreating startup batch file..." -ForegroundColor Cyan
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
    Write-Host "✓ Created start_app.bat" -ForegroundColor Green
}

# Installation complete
Write-Host "`n=== Installation Complete! ===" -ForegroundColor Green
Write-Host "To start the application, run start_app.bat or execute:" -ForegroundColor Cyan
Write-Host "  .\venv\Scripts\activate" -ForegroundColor Yellow
Write-Host "  python simple_app.py" -ForegroundColor Yellow
Write-Host "`nOnce started, open your browser and go to: http://127.0.0.1:5000/" -ForegroundColor Cyan
Write-Host "`nPress any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
