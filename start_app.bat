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
