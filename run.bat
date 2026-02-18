@echo off
chcp 65001 >nul
setlocal

set "SCRIPT_DIR=%~dp0"
set "APP_NAME=Fast-Horse-2026"

:: Remove trailing backslash
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

echo ============================================
echo   Fast-Horse-2026 Video Downloader
echo ============================================
echo.

:: Check if application exists
if not exist "%SCRIPT_DIR%\%APP_NAME%.exe" (
    echo [ERROR] %APP_NAME%.exe not found in %SCRIPT_DIR%
    echo Please make sure you're in the correct directory.
    pause
    exit /b 1
)

:: Check for FFmpeg
if not exist "%SCRIPT_DIR%\ffmpeg.exe" (
    echo [WARNING] ffmpeg.exe not found in %SCRIPT_DIR%
    echo MP4 video merging may not work properly.
    echo You can download FFmpeg from: https://ffmpeg.org/download.html
    echo.
)

:: Check for Deno
if not exist "%SCRIPT_DIR%\deno.exe" (
    echo [WARNING] deno.exe not found in %SCRIPT_DIR%
    echo YouTube JS challenges may not work properly.
    echo You can install Deno using: iwr https://deno.land/install.ps1 -UseBasicParsing ^| iex
    echo.
)

:: Add current directory to PATH for deno detection
set "PATH=%SCRIPT_DIR%;%PATH%"

echo Starting %APP_NAME%...
echo.

:: Launch the application
start "" "%SCRIPT_DIR%\%APP_NAME%.exe" %*

:: Exit script
exit /b 0
