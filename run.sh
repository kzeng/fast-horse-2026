#!/bin/bash

# Fast-Horse-2026 Run Script
# Launches the application with proper environment setup

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_NAME="Fast-Horse-2026"
VERSION="0.0.2"

echo "🚀 Launching ${APP_NAME} v${VERSION}..."

# Check if application exists
if [ ! -f "${SCRIPT_DIR}/${APP_NAME}" ]; then
    echo "❌ Error: ${APP_NAME} not found in ${SCRIPT_DIR}"
    echo "Please make sure you're in the correct directory."
    exit 1
fi

# Check if deno exists
if [ ! -f "${SCRIPT_DIR}/deno" ]; then
    echo "⚠️  Warning: deno not found in ${SCRIPT_DIR}"
    echo "YouTube JS challenges may not work properly."
fi

# Make sure deno is executable
if [ -f "${SCRIPT_DIR}/deno" ] && [ ! -x "${SCRIPT_DIR}/deno" ]; then
    echo "Making deno executable..."
    chmod +x "${SCRIPT_DIR}/deno"
fi

# Add current directory to PATH for deno detection
export PATH="${SCRIPT_DIR}:${PATH}"

echo "✅ Environment setup complete"
echo "📱 Starting ${APP_NAME}..."

# Launch the application
exec "${SCRIPT_DIR}/${APP_NAME}" "$@"