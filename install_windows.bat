@echo off
title Python Environment Setup for Windows
echo ========================================
echo    Python Environment Setup Script
echo ========================================

:: Check if Python is installed
echo Checking for Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not added to PATH.
    echo Please install Python from https://www.python.org/downloads/ and ensure it is added to PATH.
    pause
    exit /b
) else (
    echo Python is installed.
)

:: Check if pip is installed
echo Checking for pip installation...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo pip is not installed. Installing pip...
    python -m ensurepip --upgrade
    if %errorlevel% neq 0 (
        echo Failed to install pip. Please resolve this issue manually.
        pause
        exit /b
    )
    echo pip installed successfully.
) else (
    echo pip is installed.
)

:: Install required Python libraries
echo Installing required Python libraries...
pip install subprocess-tee argparse textwrap logging > install_log.txt 2>&1
if %errorlevel% neq 0 (
    echo Error installing Python libraries. Check install_log.txt for details.
    pause
    exit /b
) else (
    echo Python libraries installed successfully.
)

:: Check for Ollama CLI
echo Checking for Ollama CLI installation...
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Ollama CLI is not installed.
    echo Please download and install Ollama CLI from https://ollama.ai/docs.
    pause
    exit /b
) else (
    echo Ollama CLI is installed.
)

:: Confirm completion
echo ========================================
echo All setup steps completed successfully.
echo You can now run your Python script.
echo ========================================
pause
