# Complete Installation Script for Text-Based CRM Opportunity Extractor
# This script sets up everything, including downloading the Mistral model

# Display welcome message
Write-Host "=================================================" -ForegroundColor Magenta
Write-Host "  Text-Based CRM Opportunity Extractor - Setup" -ForegroundColor Magenta
Write-Host "=================================================" -ForegroundColor Magenta
Write-Host "This script will set up everything needed to run the application," -ForegroundColor Cyan
Write-Host "including downloading the Mistral 7B model for AI-based extraction." -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version
    Write-Host "✓ Python detected: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "✗ Python not found. Please install Python 3.8 or higher." -ForegroundColor Red
    Write-Host "  Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "  Press any key to exit..." -ForegroundColor Cyan
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
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
        Write-Host "  Press any key to exit..." -ForegroundColor Cyan
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
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
    Write-Host "  Press any key to exit..." -ForegroundColor Cyan
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
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
    Write-Host "  Press any key to exit..." -ForegroundColor Cyan
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
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

# Set up environment files
Write-Host "`nSetting up environment files..." -ForegroundColor Cyan
if (-not (Test-Path -Path ".env") -and (Test-Path -Path ".env.example")) {
    try {
        Copy-Item -Path ".env.example" -Destination ".env"
        Write-Host "✓ Created .env file from template." -ForegroundColor Green
    }
    catch {
        Write-Host "✗ Failed to create .env file: $_" -ForegroundColor Red
    }
}
elseif (Test-Path -Path ".env") {
    Write-Host "  .env file already exists." -ForegroundColor Yellow
}
else {
    Write-Host "✗ .env.example not found. Environment setup skipped." -ForegroundColor Red
}

# Download Mistral model
$modelPath = "models\mistral-7b-instruct-v0.2.Q4_K_M.gguf"
if (-not (Test-Path -Path $modelPath)) {
    Write-Host "`nDownloading Mistral 7B model..." -ForegroundColor Magenta
    Write-Host "This is a large file (about 4.1GB) and may take a while to download." -ForegroundColor Yellow
    
    try {
        $modelUrl = "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
        $webClient = New-Object System.Net.WebClient
        
        # Show progress
        Write-Host "Download started. Please be patient..." -ForegroundColor Cyan
        $webClient.DownloadFile($modelUrl, $modelPath)
        Write-Host "✓ Mistral model downloaded successfully." -ForegroundColor Green
    }
    catch {
        Write-Host "✗ Failed to download model: $_" -ForegroundColor Red
        Write-Host "  You can manually download it later from:" -ForegroundColor Yellow
        Write-Host "  $modelUrl" -ForegroundColor Yellow
        Write-Host "  And place it in the 'models' directory." -ForegroundColor Yellow
    }
}
else {
    Write-Host "`nMistral 7B model already exists." -ForegroundColor Green
}

# Install ctransformers
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

# Create start_app.bat
Write-Host "`nCreating startup batch file..." -ForegroundColor Cyan
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

$startAppContent | Out-File -FilePath "start_app.bat" -Encoding ascii
Write-Host "✓ Created start_app.bat" -ForegroundColor Green

# Installation complete
Write-Host "`n=================================================" -ForegroundColor Magenta
Write-Host "  Installation Complete!" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Magenta
Write-Host "To start the application:" -ForegroundColor Cyan
Write-Host "  1. Double-click on start_app.bat" -ForegroundColor Yellow
Write-Host "  2. Your browser will open automatically to http://127.0.0.1:5000/" -ForegroundColor Yellow
Write-Host "  3. Paste text from your opportunity document and click 'Extract Data'" -ForegroundColor Yellow
Write-Host "`nPress any key to exit..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
