#!/bin/bash

# Fast-Horse-2026 Installation Script
# Installs the application to system directories

set -e

# Configuration
APP_NAME="Fast-Horse-2026"
VERSION="0.0.2"
INSTALL_DIR="/opt/${APP_NAME}"
BIN_DIR="/usr/local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_root() {
    if [ "$EUID" -eq 0 ]; then
        print_warning "Running as root. User installation recommended."
        read -p "Continue as root? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

check_dependencies() {
    print_info "Checking dependencies..."
    
    # Check for tar
    if ! command -v tar &> /dev/null; then
        print_error "tar is required but not installed"
        exit 1
    fi
    
    print_info "Dependencies check passed"
}

extract_package() {
    local package_file="${APP_NAME}-v${VERSION}-linux-x64.tar.gz"
    
    if [ ! -f "$package_file" ]; then
        print_error "Package file not found: $package_file"
        print_info "Please make sure you're in the directory containing the package"
        exit 1
    fi
    
    print_info "Extracting package: $package_file"
    
    # Create temporary directory
    TEMP_DIR=$(mktemp -d)
    tar -xzf "$package_file" -C "$TEMP_DIR"
    
    echo "$TEMP_DIR"
}

install_files() {
    local temp_dir="$1"
    
    print_info "Installing to: $INSTALL_DIR"
    
    # Create installation directory
    sudo mkdir -p "$INSTALL_DIR"
    
    # Copy files
    sudo cp -r "$temp_dir"/* "$INSTALL_DIR"/
    
    # Set permissions
    sudo chmod -R 755 "$INSTALL_DIR"
    sudo chmod +x "$INSTALL_DIR/$APP_NAME"
    sudo chmod +x "$INSTALL_DIR/deno" 2>/dev/null || true
    
    print_info "Files installed successfully"
}

create_symlinks() {
    print_info "Creating symlinks..."
    
    # Create symlink in bin directory
    sudo ln -sf "$INSTALL_DIR/$APP_NAME" "$BIN_DIR/$APP_NAME"
    
    # Create symlink for run script if it exists
    if [ -f "$INSTALL_DIR/run.sh" ]; then
        sudo ln -sf "$INSTALL_DIR/run.sh" "$BIN_DIR/${APP_NAME}-run"
        sudo chmod +x "$INSTALL_DIR/run.sh"
    fi
    
    print_info "Symlinks created:"
    print_info "  $BIN_DIR/$APP_NAME → $INSTALL_DIR/$APP_NAME"
    if [ -f "$INSTALL_DIR/run.sh" ]; then
        print_info "  $BIN_DIR/${APP_NAME}-run → $INSTALL_DIR/run.sh"
    fi
}

create_desktop_entry() {
    print_info "Creating desktop entry..."
    
    # Create desktop directory if it doesn't exist
    mkdir -p "$DESKTOP_DIR"
    mkdir -p "$ICON_DIR"
    
    # Create desktop entry
    cat > "$DESKTOP_DIR/${APP_NAME}.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=${APP_NAME}
Comment=YouTube Video Downloader
Exec=${BIN_DIR}/${APP_NAME}
Icon=${ICON_DIR}/${APP_NAME}.png
Terminal=false
Categories=Network;Video;
Keywords=youtube;download;video;
EOF
    
    # Copy icon if it exists
    if [ -f "horse2026.jpeg" ]; then
        cp horse2026.jpeg "$ICON_DIR/${APP_NAME}.png" 2>/dev/null || true
    fi
    
    print_info "Desktop entry created: $DESKTOP_DIR/${APP_NAME}.desktop"
}

cleanup() {
    local temp_dir="$1"
    
    if [ -d "$temp_dir" ]; then
        print_info "Cleaning up temporary files..."
        rm -rf "$temp_dir"
    fi
}

show_usage() {
    print_info "Installation complete!"
    echo ""
    echo "📱 Usage:"
    echo "  Run from terminal: $APP_NAME"
    echo "  Or use run script: ${APP_NAME}-run"
    echo ""
    echo "📁 Installation location: $INSTALL_DIR"
    echo "🔗 Binary location: $BIN_DIR/$APP_NAME"
    echo ""
    echo "🎉 ${APP_NAME} v${VERSION} has been successfully installed!"
}

# Main installation process
main() {
    echo "========================================="
    echo "    ${APP_NAME} v${VERSION} Installer"
    echo "========================================="
    echo ""
    
    check_root
    check_dependencies
    
    # Extract package
    TEMP_DIR=$(extract_package)
    
    # Install files
    install_files "$TEMP_DIR"
    
    # Create symlinks
    create_symlinks
    
    # Create desktop entry (user level)
    create_desktop_entry
    
    # Cleanup
    cleanup "$TEMP_DIR"
    
    # Show usage
    show_usage
}

# Run main function
main "$@"