@echo off
echo ===================================================
echo   Text-Based CRM Opportunity Extractor - Installer
echo ===================================================
echo.
echo This will install the application and download all necessary components.
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause > nul

powershell -ExecutionPolicy Bypass -File complete_install.ps1

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Installation encountered an error.
    echo Please check the output above for details.
    echo.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Installation completed successfully!
echo You can now run the application by double-clicking on start_app.bat
echo.
pause
