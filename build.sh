#!/bin/bash

# Fast-Horse-2026 Build Script
# Creates a standalone executable for Linux

set -e

echo "🚀 Building Fast-Horse-2026..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/upgrade dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build/ dist/ dist_package/ Fast-Horse-2026-linux-x64.tar.gz

# Build executable
echo "Building executable..."
pyinstaller --onefile \
    --windowed \
    --name "Fast-Horse-2026" \
    --add-data "src/app/style.qss:app" \
    --add-data "src/app/style_light.qss:app" \
    --hidden-import "PySide6" \
    --hidden-import "PySide6.QtCore" \
    --hidden-import "PySide6.QtGui" \
    --hidden-import "PySide6.QtWidgets" \
    --hidden-import "yt_dlp" \
    --hidden-import "secretstorage" \
    --hidden-import "cryptography" \
    --hidden-import "cffi" \
    --hidden-import "jeepney" \
    src/main.py

# Create distribution package
echo "Creating distribution package..."
mkdir -p dist_package
cp dist/Fast-Horse-2026 dist_package/
cp README.md INSTALL.md requirements.txt dist_package/
cp -r src/app/style.qss src/app/style_light.qss dist_package/ 2>/dev/null || true

# Create tarball
tar -czf Fast-Horse-2026-linux-x64.tar.gz -C dist_package .

echo ""
echo "✅ Build complete!"
echo ""
echo "📦 Distribution package: Fast-Horse-2026-linux-x64.tar.gz"
echo "📁 Executable: dist/Fast-Horse-2026"
echo ""
echo "To run: ./dist/Fast-Horse-2026"
echo "To distribute: Share Fast-Horse-2026-linux-x64.tar.gz"
echo ""
echo "Package contents:"
tar -tzf Fast-Horse-2026-linux-x64.tar.gz | sed 's/^/  /'

# Test the executable
echo ""
echo "🧪 Testing executable..."
timeout 3 ./dist/Fast-Horse-2026 &
PID=$!
sleep 1
if ps -p $PID > /dev/null; then
    echo "✅ Executable launches successfully"
    kill $PID 2>/dev/null
    wait $PID 2>/dev/null
else
    echo "❌ Executable failed to launch"
    exit 1
fi

echo ""
echo "🎉 Build successful! The application is ready to use."