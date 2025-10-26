@echo off
echo Starting ArixStructure Application...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if virtual environment exists
if exist "Scripts\activate.bat" (
    echo Activating virtual environment...
    call Scripts\activate.bat
) else (
    echo No virtual environment found, using system Python...
)

REM Install dependencies if needed
echo Checking dependencies...
pip install -r requirements.txt --quiet

REM Run the application
echo.
echo Starting Streamlit application...
echo The application will open in your default web browser
echo Press Ctrl+C to stop the application
echo.

streamlit run app.py

pause