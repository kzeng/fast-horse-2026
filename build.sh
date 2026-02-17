#!/bin/bash

# Fast-Horse-2026 Build Script
# Creates a standalone executable for Linux

set -e

# Version configuration
VERSION="0.0.2"
APP_NAME="Fast-Horse-2026"
PACKAGE_NAME="${APP_NAME}-v${VERSION}-linux-x64"

echo "🚀 Building ${APP_NAME} v${VERSION}..."

# Function to clean build artifacts
clean_build() {
    echo "🧹 Cleaning build artifacts..."
    rm -rf build/ dist/ dist_package/ *.tar.gz
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    find . -name "*.pyc" -delete 2>/dev/null || true
    echo "✅ Cleanup complete"
}

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

# Install deno if not present
echo "Checking for deno..."
if ! command -v deno &> /dev/null; then
    echo "Installing deno..."
    # Install deno to user directory
    curl -fsSL https://deno.land/install.sh | sh -s -- /tmp/deno-install
    export DENO_INSTALL="/tmp/deno-install"
    export PATH="$DENO_INSTALL/bin:$PATH"
    
    # Also install to ~/.deno for user
    if [ ! -d "$HOME/.deno" ]; then
        mkdir -p "$HOME/.deno/bin"
        cp "/tmp/deno-install/bin/deno" "$HOME/.deno/bin/"
    fi
fi

# Clean previous builds
clean_build

# Build executable
echo "Building executable..."
pyinstaller --onefile \
    --windowed \
    --name "Fast-Horse-2026" \
    --add-data "src/app/style.qss:app" \
    --add-data "src/app/style_light.qss:app" \
    --add-data "horse2026.jpeg:." \
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
cp horse2026.jpeg dist_package/
cp run.sh dist_package/ 2>/dev/null || true
cp -r src/app/style.qss src/app/style_light.qss dist_package/ 2>/dev/null || true

# Copy or create deno binary
echo "Setting up deno binary..."
if [ -f "dist_package/deno" ]; then
    echo "✅ Using existing deno binary in dist_package/"
elif command -v deno &> /dev/null && [ -f "deno_runner.js" ]; then
    echo "Compiling minimal deno runtime..."
    deno compile --allow-net --allow-read --allow-write --allow-env --output dist_package/deno deno_runner.js
    echo "✅ Deno compiled: $(du -h dist_package/deno | cut -f1)"
else
    echo "⚠️  No deno binary available, YouTube downloads may fail for some videos"
    echo "   Users can install deno manually: curl -fsSL https://deno.land/install.sh | sh"
fi

# Create tarball with versioned name
echo "Creating distribution package..."
tar -czf "${PACKAGE_NAME}.tar.gz" -C dist_package .

# Function to verify build
verify_build() {
    echo "🔍 Verifying build..."
    
    # Check file sizes
    echo "File sizes:"
    du -h dist/Fast-Horse-2026 dist_package/deno 2>/dev/null || true
    
    # Check package contents
    echo -e "\nPackage contents:"
    tar -tzf "${PACKAGE_NAME}.tar.gz" | sed 's/^/  /'
    
    # Check total package size
    echo -e "\nTotal package size: $(du -h "${PACKAGE_NAME}.tar.gz" | cut -f1)"
    
    echo "✅ Verification complete"
}

echo ""
echo "✅ Build complete!"
echo ""
echo "📦 Distribution package: ${PACKAGE_NAME}.tar.gz"
echo "📁 Executable: dist/Fast-Horse-2026"
echo "🏷️  Version: ${VERSION}"
echo ""
echo "To run: ./dist/Fast-Horse-2026"
echo "To distribute: Share ${PACKAGE_NAME}.tar.gz"

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

# Verify build
verify_build

echo ""
echo "🎉 Build successful! ${APP_NAME} v${VERSION} is ready to use."
echo ""
echo "📊 Build Summary:"
echo "  - Application: ${APP_NAME} v${VERSION}"
echo "  - Package: ${PACKAGE_NAME}.tar.gz"
echo "  - Build time: $(date)"
echo "  - Status: ✅ Ready for distribution"