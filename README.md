# Fast-Horse-2026 - YouTube Video Downloader

![Fast-Horse-2026](https://img.shields.io/badge/Fast--Horse--2026-YouTube%20Downloader-blue)
![Python](https://img.shields.io/badge/Python-3.10%2B-green)
![PySide6](https://img.shields.io/badge/GUI-PySide6-orange)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey)

A powerful, feature-rich desktop application for downloading YouTube videos with a modern PySide6 interface, bilingual support, and advanced configuration options.

## ✨ **Features**

### **Core Features**
- **Modern GUI**: Clean, professional interface with dark/light theme support
- **Video Preview**: Fetch and display video information (title, duration, uploader, views)
- **Multiple Formats**: Download in various qualities (1080p, 720p, 480p, MP3 audio)
- **Playlist Support**: Download entire playlists with automatic folder organization
- **Progress Tracking**: Real-time download progress with speed and ETA
- **Folder Selection**: Choose custom download location

### **Advanced Features**
- **🌐 Bilingual UI**: Full Chinese/English language support with dynamic switching
- **🔧 Configurable Proxy**: SOCKS5/HTTP proxy support with settings dialog
- **🎨 Theme Switching**: Dark/Light theme toggle with preference saving
- **📱 Professional Menu**: File, Settings, Help menus with keyboard shortcuts
- **⚡ Performance**: Multi-threaded downloads with progress tracking

## 📸 **Screenshots**

*(Application screenshots would go here)*

## 🚀 **Quick Start**

### **Download Pre-built Executable**
1. Download `Fast-Horse-2026-linux-x64.tar.gz` from releases
2. Extract: `tar -xzf Fast-Horse-2026-linux-x64.tar.gz`
3. Run: `./Fast-Horse-2026`

### **From Source**
```bash
# Clone repository
git clone https://gitee.com/kzeng/fast-horse-2026.git
cd fast-horse-2026

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run application
cd src
python main.py
```

## 📦 **Installation**

### **Dependencies**
- Python 3.10+
- PySide6 (GUI framework)
- yt-dlp (YouTube download engine)
- PyYAML (configuration)
- secretstorage (browser cookies access)

### **FFmpeg (Recommended)**
For MP4 downloads with audio, install FFmpeg:
- **Linux**: `sudo apt install ffmpeg`
- **macOS**: `brew install ffmpeg`
- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/)

## 🎮 **Usage**

### **Basic Usage**
1. **Launch** the application
2. **Paste YouTube URL** in the input field
3. **Click "Fetch Info"** to load video details
4. **Select format** from dropdown
5. **Choose download folder** (optional)
6. **Click "Download"** to start

### **Advanced Features**
- **Language Switch**: Settings → Language → English/中文
- **Proxy Settings**: Settings → Proxy Settings
- **Theme Switch**: Settings → Theme → Dark/Light
- **Playlist Download**: Paste playlist URL, all videos download to playlist folder

## 🏗️ **Project Structure**

```
fast-horse-2026/
├── src/
│   ├── main.py                     # Application entry point
│   └── app/
│       ├── __init__.py
│       ├── main_window.py          # Main window UI (QMainWindow)
│       ├── download_manager.py     # yt-dlp integration with proxy support
│       ├── translations.py         # Bilingual translation system
│       ├── settings_dialog.py      # Proxy configuration dialog
│       ├── style.qss               # Dark theme stylesheet
│       └── style_light.qss         # Light theme stylesheet
├── requirements.txt                # Python dependencies
├── build.sh                        # Build script for Linux
├── Fast-Horse-2026.spec           # PyInstaller specification
├── INSTALL.md                      # Detailed installation guide
├── BUILD_SUMMARY.md               # Build and feature documentation
└── README.md                       # This file
```

## ⚙️ **Configuration**

### **Proxy Settings**
Configure proxy through Settings → Proxy Settings:
- **No Proxy**: Direct connection
- **SOCKS5**: SOCKS5 proxy support
- **HTTP**: HTTP proxy support
- Settings saved automatically

### **Language Settings**
- **English**: Complete English UI
- **中文**: Complete Chinese UI
- Dynamic switching without restart

### **Theme Settings**
- **Dark Theme**: Professional dark interface (default)
- **Light Theme**: Clean light interface
- Preference saved between sessions

## 🔧 **Development**

### **Building from Source**
```bash
# Install build dependencies
pip install pyinstaller

# Build executable
./build.sh

# Output: dist/Fast-Horse-2026
# Package: Fast-Horse-2026-linux-x64.tar.gz
```

### **Adding New Translations**
1. Edit `src/app/translations.py`
2. Add translation keys to both `_english_translations()` and `_chinese_translations()`
3. Use `translator.get('key')` in UI code

### **Adding New Themes**
1. Create new `.qss` file in `src/app/`
2. Update `load_stylesheet()` method in `main_window.py`
3. Add theme option to menu

## 🐛 **Troubleshooting**

### **Common Issues**
1. **"YouTube bot detection"**: Log into YouTube in browser first, app uses browser cookies
2. **"No video formats"**: Install Deno for JavaScript challenge solving
3. **"Network error"**: Check proxy settings or try without proxy
4. **"FFmpeg not found"**: Install FFmpeg for MP4 with audio

### **Deno Installation (for JS challenges)**
```bash
# Install Deno
curl -fsSL https://deno.land/install.sh | sh

# Add to PATH
export PATH="$HOME/.deno/bin:$PATH"
```

## 📄 **License**

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Powerful YouTube download engine
- [PySide6](https://www.qt.io/qt-for-python) - Qt Python bindings for GUI
- [FFmpeg](https://ffmpeg.org/) - Multimedia framework
- [Deno](https://deno.land/) - JavaScript/TypeScript runtime for JS challenges

## 🤝 **Contributing**

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## 📞 **Support**

- **Issues**: [GitHub Issues](https://gitee.com/kzeng/fast-horse-2026/issues)
- **Documentation**: See [INSTALL.md](INSTALL.md) for detailed instructions

---

**Fast-Horse-2026** - Fast, feature-rich YouTube video downloader for 2026 and beyond!