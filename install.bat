@echo off
echo Installing ArixStructure Dependencies...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Python found. Installing dependencies...
echo.

REM Upgrade pip first
python -m pip install --upgrade pip

REM Install requirements
pip install -r requirements.txt

echo.
echo Installation complete!
echo.
echo To run the application:
echo   1. Double-click run.bat
echo   2. Or run: python start.py
echo   3. Or run: streamlit run app.py
echo.
pause