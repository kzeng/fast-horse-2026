@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

set VERSION=0.0.2
set APP_NAME=Fast-Horse-2026
set PACKAGE_NAME=%APP_NAME%-v%VERSION%-win-x64

echo.
echo ============================================
echo   Building %APP_NAME% v%VERSION% for Windows
echo ============================================
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.10 or higher.
    exit /b 1
)

:: Create virtual environment (if not exists)
if not exist venv (
    echo [1/6] Creating virtual environment...
    python -m venv venv
) else (
    echo [1/6] Using existing virtual environment...
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Install dependencies
echo [2/6] Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    exit /b 1
)

:: Check/Install Deno
where deno.exe >nul 2>&1
if %errorlevel% neq 0 (
    echo [3/6] Installing Deno...
    powershell -Command "irm https://deno.land/install.ps1 | iex"
    if %errorlevel% neq 0 (
        echo [WARNING] Failed to install Deno. JS challenges may not work.
    )
) else (
    echo [3/6] Deno already installed.
)

:: Download FFmpeg
echo [4/6] Setting up FFmpeg...
if not exist "ffmpeg.exe" (
    echo Downloading FFmpeg...
    powershell -Command "try { Invoke-WebRequest -Uri 'https://github.com/GyanD/codexffmpeg/releases/download/6.0/ffmpeg-6.0-essentials_build.zip' -OutFile 'ffmpeg.zip' -UseBasicParsing } catch { Write-Host 'Failed to download FFmpeg' }"
    if exist "ffmpeg.zip" (
        powershell -Command "Expand-Archive -Path 'ffmpeg.zip' -DestinationPath 'ffmpeg_temp' -Force"
        if exist "ffmpeg_temp\bin\ffmpeg.exe" (
            copy "ffmpeg_temp\bin\ffmpeg.exe" "ffmpeg.exe"
            echo FFmpeg downloaded successfully.
        ) else (
            echo [WARNING] FFmpeg not found in archive.
        )
        rmdir /s /q ffmpeg_temp 2>nul
        del ffmpeg.zip 2>nul
    ) else (
        echo [WARNING] Could not download FFmpeg. Install it manually for MP4 downloads.
    )
) else (
    echo FFmpeg already exists.
)

:: Clean previous builds
echo [5/6] Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist dist_package rmdir /s /q dist_package

:: Build executable using spec file
echo [6/6] Building executable...
pyinstaller Fast-Horse-2026.spec --noconfirm
if %errorlevel% neq 0 (
    echo [ERROR] Build failed.
    exit /b 1
)

:: Create distribution package
echo.
echo Creating distribution package...
mkdir dist_package
copy dist\%APP_NAME%.exe dist_package\
copy README.md INSTALL.md requirements.txt dist_package\
copy horse2026.jpeg dist_package\
copy ffmpeg.exe dist_package\ 2>nul
copy run.bat dist_package\ 2>nul

:: Copy style files
mkdir dist_package\app
copy src\app\style.qss dist_package\app\
copy src\app\style_light.qss dist_package\app\

:: Copy deno if exists
copy deno.exe dist_package\ 2>nul

:: Create ZIP package
echo Creating ZIP archive...
powershell -Command "Compress-Archive -Path 'dist_package\*' -DestinationPath '%PACKAGE_NAME%.zip' -Force"

echo.
echo ============================================
echo   Build Complete!
echo ============================================
echo.
echo Package: %PACKAGE_NAME%.zip
echo Executable: dist\%APP_NAME%.exe
echo.
echo To run: dist\%APP_NAME%.exe
echo.

:: Cleanup
deactivate
