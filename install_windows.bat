# Windows Installation Script
@echo off

REM Ensure Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python is not installed. Please install Python from https://www.python.org/downloads/ and ensure it is added to PATH.
    exit /b
)

REM Install pip dependencies
pip install subprocess-tee argparse textwrap logging
if %ERRORLEVEL% neq 0 (
    echo Failed to install Python dependencies. Check your Python and pip installation.
    exit /b
)

REM Check for Ollama CLI
ollama --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Ollama CLI is not installed. Please download it from https://ollama.ai/docs and add it to PATH.
    exit /b
)

REM Confirm setup
echo Installation complete. Ready to run the Python script.
exit /b

