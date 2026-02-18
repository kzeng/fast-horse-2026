#!/bin/bash

# Fast-Horse-2026 Run Script
# Launches the application with proper environment setup

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_NAME="Fast-Horse-2026"
VERSION="0.0.2"

echo "🚀 Launching ${APP_NAME} v${VERSION}..."

# Check if application exists in different possible locations
APP_PATH=""
if [ -f "${SCRIPT_DIR}/dist/${APP_NAME}" ]; then
    APP_PATH="${SCRIPT_DIR}/dist/${APP_NAME}"
elif [ -f "${SCRIPT_DIR}/${APP_NAME}" ]; then
    APP_PATH="${SCRIPT_DIR}/${APP_NAME}"
elif [ -f "${SCRIPT_DIR}/dist_package/${APP_NAME}" ]; then
    APP_PATH="${SCRIPT_DIR}/dist_package/${APP_NAME}"
fi

if [ -z "$APP_PATH" ]; then
    echo "❌ Error: ${APP_NAME} not found"
    echo "Please build the application first: ./build.sh"
    exit 1
fi

echo "Found app at: $APP_PATH"

# Get the directory where the app is located
APP_DIR="$(dirname "$APP_PATH")"

# Check if deno exists
if [ ! -f "${APP_DIR}/deno" ]; then
    echo "⚠️  Warning: deno not found in ${APP_DIR}"
    echo "YouTube JS challenges may not work properly."
fi

# Make sure deno is executable
if [ -f "${APP_DIR}/deno" ] && [ ! -x "${APP_DIR}/deno" ]; then
    echo "Making deno executable..."
    chmod +x "${APP_DIR}/deno"
fi

# Add app directory to PATH for deno detection
export PATH="${APP_DIR}:${PATH}"

# Pass proxy environment variables to the application
# This ensures yt-dlp can use system proxy settings
if [ -n "$HTTP_PROXY" ]; then
    export HTTP_PROXY="$HTTP_PROXY"
fi
if [ -n "$HTTPS_PROXY" ]; then
    export HTTPS_PROXY="$HTTPS_PROXY"
fi
if [ -n "$ALL_PROXY" ]; then
    export ALL_PROXY="$ALL_PROXY"
fi

echo "✅ Environment setup complete"
echo "📱 Starting ${APP_NAME}..."

# Launch the application
exec "${APP_PATH}" "$@"