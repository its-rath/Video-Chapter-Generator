@echo off
setlocal

REM Check if venv exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 exit /b %errorlevel%
)

REM Activate venv
call venv\Scripts\activate
if %errorlevel% neq 0 exit /b %errorlevel%

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 exit /b %errorlevel%

REM Run the application
echo Starting application...
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
