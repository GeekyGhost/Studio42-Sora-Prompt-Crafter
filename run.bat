@echo off
echo ========================================
echo SORA PROMPT MAKER - DON'T PANIC!
echo ========================================
echo.

REM Check for Python
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    where py >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Python not found. Please install Python 3.10+ from python.org
        pause
        exit /b 1
    )
    set PYTHON=py -3
) else (
    set PYTHON=python
)

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo [SETUP] Creating virtual environment...
    %PYTHON% -m venv .venv
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo [SETUP] Activating virtual environment...
call .venv\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install/upgrade requirements
if exist "requirements.txt" (
    echo [SETUP] Installing requirements...
    pip install -q --upgrade pip
    pip install -q -r requirements.txt
    if %ERRORLEVEL% NEQ 0 (
        echo [WARNING] Some packages may have failed to install
    )
)

REM Create folder structure
if not exist "templates" mkdir templates
if not exist "static" mkdir static

REM Check if files exist
if not exist "app.py" (
    echo [ERROR] app.py not found in current directory!
    pause
    exit /b 1
)

if not exist "templates\index.html" (
    echo [WARNING] templates\index.html not found!
    echo Make sure to create the HTML file in the templates folder.
    pause
)

echo.
echo ========================================
echo SERVER STARTING
echo ========================================
echo.
echo Opening browser to: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Wait a moment then open browser
start "" timeout /t 2 /nobreak >nul && start http://localhost:5000

REM Run Flask app
python app.py

REM Cleanup
call deactivate
pause