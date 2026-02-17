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
- **🔧 Configurable Proxy**: SOCKS5/HTTP proxy support with integrated settings
- **🎨 Theme Switching**: Dark/Light theme toggle with preference saving
- **📱 Tab Interface**: Modern tab layout (Main/Settings) for better user experience
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
- **Language Switch**: Settings tab → Language section → English/中文
- **Proxy Settings**: Settings tab → Proxy Settings section
- **Theme Switch**: Settings tab → Theme section → Dark/Light
- **About Info**: Settings tab → About section with author and version
- **Playlist Download**: Paste playlist URL, all videos download to playlist folder

## 🏗️ **Project Structure**

```
fast-horse-2026/
├── src/
│   ├── main.py                     # Application entry point
│   └── app/
│       ├── __init__.py
│       ├── main_window.py          # Main window UI with tab layout (QMainWindow)
│       ├── download_manager.py     # yt-dlp integration with proxy support
│       ├── translations.py         # Bilingual translation system
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

### **Tab Interface**
The application features a modern tab-based interface:
- **Main Tab**: Video downloader interface (URL input, format selection, progress)
- **Settings Tab**: All configuration options in one place:
  - **Language Section**: Switch between English/中文
  - **Theme Section**: Toggle between Dark/Light themes
  - **Proxy Settings**: Configure SOCKS5/HTTP/No proxy
  - **About Section**: Author info (Zengkai001@qq.com) and version (0.0.1)

### **Proxy Settings**
Configure proxy through Settings tab → Proxy Settings:
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

## 🇨🇳 **中文文档**

### **快速开始**
1. **下载预编译版本**: 从发布页面下载 `Fast-Horse-2026-linux-x64.tar.gz`
2. **解压**: `tar -xzf Fast-Horse-2026-linux-x64.tar.gz`
3. **运行**: `./Fast-Horse-2026`

### **从源码运行**
```bash
# 克隆仓库
git clone https://gitee.com/kzeng/fast-horse-2026.git
cd fast-horse-2026

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt

# 运行应用
cd src
python main.py
```

### **使用说明**
1. **主界面标签页**: 粘贴YouTube链接，获取视频信息，选择格式，下载视频
2. **设置标签页**: 
   - **语言设置**: 切换英文/中文界面
   - **主题设置**: 切换深色/浅色主题
   - **代理设置**: 配置SOCKS5/HTTP代理
   - **关于信息**: 作者Zengkai001@qq.com，版本0.0.1

### **功能特点**
- **现代化标签界面**: 主界面/设置标签页布局，操作更直观
- **双语支持**: 完整的中文/英文界面，实时切换
- **代理配置**: 支持SOCKS5/HTTP代理，解决网络限制
- **主题切换**: 深色/浅色主题，保护眼睛
- **播放列表支持**: 下载整个播放列表，自动创建文件夹

### **常见问题**
1. **"YouTube机器人检测"**: 先在浏览器登录YouTube，应用会使用浏览器cookies
2. **"没有视频格式"**: 安装Deno解决JavaScript挑战
3. **"网络错误"**: 检查代理设置或尝试不使用代理
4. **"FFmpeg未找到"**: 安装FFmpeg以支持带音频的MP4下载

### **Deno安装（解决JS挑战）**
```bash
# 安装Deno
curl -fsSL https://deno.land/install.sh | sh

# 添加到PATH
export PATH="$HOME/.deno/bin:$PATH"
```

---
**Fast-Horse-2026** - Fast, feature-rich YouTube video downloader for 2026 and beyond!
**快马2026** - 为2026及以后设计的快速、功能丰富的YouTube视频下载器！