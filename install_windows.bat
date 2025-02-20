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

:: Check if pip is
