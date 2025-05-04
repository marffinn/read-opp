# Cleanup Script for Text-Based CRM Opportunity Extractor
# This script removes unnecessary files and directories

$ErrorActionPreference = "Stop"

Write-Host "=== Cleaning up the project directory ===" -ForegroundColor Green

# List of directories to remove
$dirsToRemove = @(
    "examples",
    "test_pdfs",
    "uploads",
    "src\pdf_processor",
    "src\interface",
    "src\__pycache__",
    "src\crm_extractor\__pycache__",
    "src\pdf_processor\__pycache__",
    "src\interface\__pycache__"
)

# List of files to remove
$filesToRemove = @(
    "app.py",
    "download_model.py",
    "index.html",
    "setup.bat",
    "setup.sh",
    "setup_local_llm.py",
    "test_opportunity.pdf",
    "test_opportunity2.pdf",
    "src\main.py"
)

# Remove directories
foreach ($dir in $dirsToRemove) {
    if (Test-Path $dir) {
        Write-Host "Removing directory: $dir" -ForegroundColor Yellow
        Remove-Item -Path $dir -Recurse -Force -ErrorAction SilentlyContinue
    }
}

# Remove files
foreach ($file in $filesToRemove) {
    if (Test-Path $file) {
        Write-Host "Removing file: $file" -ForegroundColor Yellow
        Remove-Item -Path $file -Force -ErrorAction SilentlyContinue
    }
}

# Create clean directory structure
$dirsToCreate = @(
    "logs",
    "extraction_results",
    "models"
)

foreach ($dir in $dirsToCreate) {
    if (-not (Test-Path $dir)) {
        Write-Host "Creating directory: $dir" -ForegroundColor Cyan
        New-Item -ItemType Directory -Path $dir | Out-Null
    }
}

# Create .gitignore entries for the clean directories
$gitignoreEntries = @(
    "# Python bytecode",
    "__pycache__/",
    "*.py[cod]",
    "*$py.class",
    "",
    "# Virtual environment",
    "venv/",
    "env/",
    "",
    "# Application specific",
    "logs/",
    "extraction_results/",
    "models/",
    "",
    "# IDE files",
    ".vscode/",
    ".idea/"
)

Write-Host "Updating .gitignore file" -ForegroundColor Cyan
$gitignoreEntries | Out-File -FilePath ".gitignore" -Encoding utf8

Write-Host "`nCleanup complete!" -ForegroundColor Green
Write-Host "The project directory has been cleaned up and organized." -ForegroundColor Cyan
