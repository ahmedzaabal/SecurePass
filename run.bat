@echo off
REM Quick start script for Windows

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -q -r requirements.txt

echo Starting SecurePass...
python main.py

pause
