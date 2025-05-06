# Complete Installation Script for Text-Based CRM Opportunity Extractor
# This script sets up everything, including downloading the Mistral model

# Set error action preference to stop on any error
$ErrorActionPreference = "Stop"

# Set console colors for better readability
$infoColor = "Cyan"
$successColor = "Green"
$warningColor = "Yellow"
$errorColor = "Red"
$highlightColor = "Magenta"

# Display welcome message
Write-Host "=================================================" -ForegroundColor $highlightColor
Write-Host "  Text-Based CRM Opportunity Extractor - Setup" -ForegroundColor $highlightColor
Write-Host "=================================================" -ForegroundColor $highlightColor
Write-Host "This script will set up everything needed to run the application," -ForegroundColor $infoColor
Write-Host "including downloading the Mistral 7B model for AI-based extraction." -ForegroundColor $infoColor
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version
    Write-Host "✓ Python detected: $pythonVersion" -ForegroundColor $successColor
} catch {
    Write-Host "✗ Python not found. Please install Python 3.8 or higher." -ForegroundColor $errorColor
    Write-Host "  Download from: https://www.python.org/downloads/" -ForegroundColor $warningColor
    Write-Host "  Press any key to exit..." -ForegroundColor $infoColor
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

# Create virtual environment
Write-Host "`nCreating virtual environment..." -ForegroundColor $infoColor
if (Test-Path -Path "venv") {
    Write-Host "  Virtual environment already exists." -ForegroundColor $warningColor
} else {
    try {
        python -m venv venv
        Write-Host "✓ Virtual environment created successfully." -ForegroundColor $successColor
    } catch {
        Write-Host "✗ Failed to create virtual environment: $_" -ForegroundColor $errorColor
        Write-Host "  Press any key to exit..." -ForegroundColor $infoColor
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        exit 1
    }
}

# Activate virtual environment
Write-Host "`nActivating virtual environment..." -ForegroundColor $infoColor
try {
    & .\venv\Scripts\Activate.ps1
    Write-Host "✓ Virtual environment activated." -ForegroundColor $successColor
} catch {
    Write-Host "✗ Failed to activate virtual environment: $_" -ForegroundColor $errorColor
    Write-Host "  Try running this script with administrator privileges or run:" -ForegroundColor $warningColor
    Write-Host "  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor $warningColor
    Write-Host "  Press any key to exit..." -ForegroundColor $infoColor
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

# Install dependencies
Write-Host "`nInstalling dependencies..." -ForegroundColor $infoColor
try {
    pip install -r requirements.txt
    Write-Host "✓ Dependencies installed successfully." -ForegroundColor $successColor
} catch {
    Write-Host "✗ Failed to install dependencies: $_" -ForegroundColor $errorColor
    Write-Host "  Press any key to exit..." -ForegroundColor $infoColor
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

# Create directories
Write-Host "`nCreating necessary directories..." -ForegroundColor $infoColor
if (-not (Test-Path -Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
}
if (-not (Test-Path -Path "extraction_results")) {
    New-Item -ItemType Directory -Path "extraction_results" | Out-Null
}
if (-not (Test-Path -Path "models")) {
    New-Item -ItemType Directory -Path "models" | Out-Null
}
Write-Host "✓ Directories created." -ForegroundColor $successColor

# Set up environment files
Write-Host "`nSetting up environment files..." -ForegroundColor $infoColor
if (-not (Test-Path -Path ".env") -and (Test-Path -Path ".env.example")) {
    try {
        Copy-Item -Path ".env.example" -Destination ".env"
        Write-Host "✓ Created .env file from template." -ForegroundColor $successColor
    } catch {
        Write-Host "✗ Failed to create .env file: $_" -ForegroundColor $errorColor
    }
} elseif (Test-Path -Path ".env") {
    Write-Host "  .env file already exists." -ForegroundColor $warningColor
} else {
    Write-Host "✗ .env.example not found. Environment setup skipped." -ForegroundColor $errorColor
}

# Download Mistral model
$modelPath = "models\mistral-7b-instruct-v0.2.Q4_K_M.gguf"
if (-not (Test-Path -Path $modelPath)) {
    Write-Host "`nDownloading Mistral 7B model..." -ForegroundColor $highlightColor
    Write-Host "This is a large file (about 4.1GB) and may take a while to download." -ForegroundColor $warningColor
    Write-Host "The download will continue in the background while we set up other components." -ForegroundColor $infoColor
    
    try {
        $modelUrl = "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
        
        # Start download in background
        $webClient = New-Object System.Net.WebClient
        $downloadJob = Start-Job -ScriptBlock {
            param($url, $path)
            $webClient = New-Object System.Net.WebClient
            $webClient.DownloadFile($url, $path)
        } -ArgumentList $modelUrl, $modelPath
        
        Write-Host "✓ Download started in background." -ForegroundColor $successColor
    } catch {
        Write-Host "✗ Failed to start model download: $_" -ForegroundColor $errorColor
        Write-Host "  You can manually download it later from:" -ForegroundColor $warningColor
        Write-Host "  $modelUrl" -ForegroundColor $warningColor
    }
} else {
    Write-Host "`nMistral 7B model already exists." -ForegroundColor $successColor
}

# Install ctransformers
Write-Host "`nInstalling ctransformers for model support..." -ForegroundColor $infoColor
try {
    pip install ctransformers
    Write-Host "✓ ctransformers installed successfully." -ForegroundColor $successColor
} catch {
    Write-Host "✗ Failed to install ctransformers: $_" -ForegroundColor $errorColor
    Write-Host "  You can manually install it later with:" -ForegroundColor $warningColor
    Write-Host "  pip install ctransformers" -ForegroundColor $warningColor
}

# Create start_app.bat
Write-Host "`nCreating startup batch file..." -ForegroundColor $infoColor
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
Write-Host "✓ Created start_app.bat" -ForegroundColor $successColor

# Check if model download is complete
if (Get-Variable -Name downloadJob -ErrorAction SilentlyContinue) {
    Write-Host "`nWaiting for Mistral model download to complete..." -ForegroundColor $infoColor
    Write-Host "This may take a while depending on your internet connection." -ForegroundColor $warningColor
    Write-Host "You can press Ctrl+C to skip waiting and complete the setup." -ForegroundColor $warningColor
    
    try {
        Wait-Job -Job $downloadJob -Timeout 60 | Out-Null
        if ($downloadJob.State -eq "Completed") {
            Receive-Job -Job $downloadJob | Out-Null
            Write-Host "✓ Mistral model downloaded successfully." -ForegroundColor $successColor
        } else {
            Write-Host "  Model download is still in progress." -ForegroundColor $warningColor
            Write-Host "  You can check the models directory later to see if it completed." -ForegroundColor $warningColor
        }
    } catch {
        Write-Host "  Stopped waiting for model download." -ForegroundColor $warningColor
        Write-Host "  Download will continue in the background." -ForegroundColor $warningColor
    }
}

# Installation complete
Write-Host "`n=================================================" -ForegroundColor $highlightColor
Write-Host "  Installation Complete!" -ForegroundColor $successColor
Write-Host "=================================================" -ForegroundColor $highlightColor
Write-Host "To start the application:" -ForegroundColor $infoColor
Write-Host "  1. Double-click on start_app.bat" -ForegroundColor $warningColor
Write-Host "  2. Your browser will open automatically to http://127.0.0.1:5000/" -ForegroundColor $warningColor
Write-Host "  3. Paste text from your opportunity document and click 'Extract Data'" -ForegroundColor $warningColor
Write-Host "`nPress any key to exit..." -ForegroundColor $infoColor
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
