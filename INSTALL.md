# Installation Guide for YTDownloader

## Quick Start

### For Linux Users
1. Download the `YTDownloader` executable
2. Make it executable: `chmod +x YTDownloader`
3. Run it: `./YTDownloader`

### For Windows Users
1. Download the `YTDownloader.exe` (if built for Windows)
2. Double-click to run

## System Requirements

### Minimum Requirements
- **OS**: Linux (x86_64), Windows 10+, or macOS 10.15+
- **RAM**: 2GB minimum, 4GB recommended
- **Storage**: 100MB free space

### Recommended
- **FFmpeg**: For best MP4 video quality (merges audio+video)
- **Browser**: Chrome or Firefox (for YouTube cookie access)

## FFmpeg Installation

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg
```

### Windows
1. Download from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract to a folder (e.g., `C:\ffmpeg`)
3. Add to PATH or place `ffmpeg.exe` in same folder as YTDownloader

### macOS
```bash
brew install ffmpeg
```

## First Run Setup

1. **Launch YTDownloader**
2. **Log into YouTube** in your browser (Chrome/Firefox recommended)
   - This helps bypass YouTube's bot detection
   - The app will automatically try to use browser cookies
3. **Test with a video**: Paste a YouTube URL and click "Fetch Info"

## Troubleshooting

### "Sign in to confirm you're not a bot" Error
1. Make sure you're logged into YouTube in Chrome/Firefox
2. Restart the app
3. Try a different video URL

### FFmpeg Not Found
1. Install FFmpeg (see above)
2. For MP3 downloads, FFmpeg is optional
3. For MP4 downloads, FFmpeg is required for audio+video merging

### App Won't Start
1. Check file permissions: `chmod +x YTDownloader`
2. Try running from terminal: `./YTDownloader`
3. Check system libraries (Linux): `ldd YTDownloader`

## Advanced Usage

### Command Line Options
Run from terminal to see debug output:
```bash
./YTDownloader --debug
```

### Settings Location
- **Linux**: `~/.config/YTDownloader/App.conf`
- **Windows**: `%APPDATA%\YTDownloader\App.conf`
- **macOS**: `~/Library/Preferences/YTDownloader/App.conf`

### Reset Settings
Delete the settings file above to reset all preferences.

## Building from Source

See `README.md` for development setup and building instructions.

## Support

For issues or feature requests:
1. Check the troubleshooting section above
2. Run with `--debug` flag for more information
3. Ensure all dependencies are installed