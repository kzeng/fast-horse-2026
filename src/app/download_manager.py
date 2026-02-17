import yt_dlp
from PySide6.QtCore import QThread, Signal, QSettings
from .translations import translator

def get_proxy_url():
    """Get proxy URL from application settings"""
    settings = QSettings("Fast-Horse-2026", "App")
    proxy_type = settings.value("proxy_type", translator.get('settings_proxy_socks5'))
    proxy_host = settings.value("proxy_host", "127.0.0.1")
    proxy_port = settings.value("proxy_port", "10808")
    
    if proxy_type == translator.get('settings_proxy_none'):
        return None
    elif proxy_type == translator.get('settings_proxy_socks5'):
        return f"socks5://{proxy_host}:{proxy_port}"
    elif proxy_type == translator.get('settings_proxy_http'):
        return f"http://{proxy_host}:{proxy_port}"
    else:
        return f"socks5://{proxy_host}:{proxy_port}"

def is_bilibili_url(url):
    """检测URL是否为B站URL"""
    if not url:
        return False
    
    # B站域名模式
    bilibili_domains = [
        'bilibili.com',
        'b23.tv',
        'biligame.com',
        'biligame.net',
        'bilibili.tv',
    ]
    
    import re
    url_lower = url.lower()
    
    # 检查是否包含B站域名
    for domain in bilibili_domains:
        if domain in url_lower:
            return True
    
    # 检查B站视频ID模式 (BV开头)
    bv_pattern = r'BV[a-zA-Z0-9]{10}'
    if re.search(bv_pattern, url_lower, re.IGNORECASE):
        return True
    
    # 检查B站av号模式
    av_pattern = r'av\d+'
    if re.search(av_pattern, url_lower, re.IGNORECASE):
        return True
    
    return False

def get_format_for_url(url, user_format_spec):
    """根据URL类型返回合适的格式选择"""
    if is_bilibili_url(url):
        # B站需要特殊的格式选择
        # 如果用户选择了音频格式，保持原样
        if user_format_spec == 'bestaudio/best':
            return user_format_spec
        # 否则使用B站兼容格式
        else:
            return 'bestvideo+bestaudio'
    else:
        # 其他网站使用用户选择的格式
        return user_format_spec

class FetchInfoThread(QThread):
    finished = Signal(dict)
    error = Signal(str)
    
    def __init__(self, url):
        super().__init__()
        self.url = url
        
    def run(self):
        import sys
        import threading
        import subprocess
        import os
        print(f"DEBUG: FetchInfoThread.run() started for URL: {self.url}", flush=True)
        print(f"DEBUG: Python thread: {threading.current_thread().name}", flush=True)
        
        # Check if Deno is available (for YouTube JS challenges)
        deno_available = False
        deno_path = None
        try:
            # First check bundled deno in same directory as executable
            # When packaged with PyInstaller, sys._MEIPASS contains temp directory
            # The deno binary should be in the same directory as the executable
            import sys
            import os
            
            # Get directory of current executable
            if getattr(sys, 'frozen', False):
                # Running as PyInstaller bundle
                exe_dir = os.path.dirname(sys.executable)
                bundled_deno = os.path.join(exe_dir, 'deno')
            else:
                # Running as script
                exe_dir = os.path.dirname(os.path.abspath(__file__))
                project_root = os.path.dirname(exe_dir)
                bundled_deno = os.path.join(project_root, 'deno')
            
            # Check common Deno installation paths (including bundled)
            common_paths = [
                bundled_deno,  # Bundled deno first
                os.path.expanduser('~/.deno/bin/deno'),  # Current user's Deno
                '/usr/local/bin/deno',
                '/usr/bin/deno',
                'deno'  # Check PATH as fallback
            ]
            
            for deno_candidate in common_paths:
                try:
                    result = subprocess.run(['which', deno_candidate] if deno_candidate == 'deno' else ['test', '-f', deno_candidate], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        deno_available = True
                        deno_path = deno_candidate if deno_candidate != 'deno' else 'deno'
                        print(f"DEBUG: Deno found at: {deno_path}", flush=True)
                        break
                except Exception:
                    continue
            
            if not deno_available:
                print(f"DEBUG: Deno not found in common locations", flush=True)
        except Exception:
            print(f"DEBUG: Could not check for Deno", flush=True)
        
        try:
            # METHOD 1: Try with JS challenge solving (if Deno available)
            # 为B站URL使用智能格式选择
            # B站需要bestvideo+bestaudio格式，其他网站使用best[height<=1080]
            if is_bilibili_url(self.url):
                format_for_url = 'bestvideo+bestaudio'
                # B站需要更长的超时时间
                socket_timeout = 30
            else:
                format_for_url = 'best[height<=1080]'
                socket_timeout = 20
            
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'socket_timeout': socket_timeout,
                'proxy': get_proxy_url(),
                'cookiesfrombrowser': ('firefox',),
                'user_agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
                'format': format_for_url,
            }
            
            # 为B站URL添加referer头
            if is_bilibili_url(self.url):
                ydl_opts['referer'] = 'https://www.bilibili.com'
                print(f"DEBUG: B站URL检测成功，使用B站专用配置", flush=True)
            
            # If Deno is available, set environment to include it
            if deno_available and deno_path and deno_path != 'deno':
                # Extract directory from deno_path
                deno_dir = os.path.dirname(deno_path)
                # Add to PATH for this process
                os.environ['PATH'] = deno_dir + ':' + os.environ.get('PATH', '')
                print(f"DEBUG: Added {deno_dir} to PATH", flush=True)
            
            print(f"DEBUG: Method 1: With JS challenge solving...", flush=True)
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(self.url, download=False)
                    if info:
                        print(f"DEBUG: Method 1 SUCCESS!", flush=True)
                        self.finished.emit(info)
                        return
            except Exception as e1:
                error_str = str(e1)
                print(f"DEBUG: Method 1 failed: {error_str[:80]}", flush=True)
                
                # METHOD 2: Try without format selection (extract basic info only)
                if 'Requested format is not available' in error_str:
                    print(f"DEBUG: Method 2: Extract basic info without formats...", flush=True)
                    # B站需要更长的超时时间
                    timeout_2 = 30 if is_bilibili_url(self.url) else 15
                    try:
                        ydl_opts_basic = {
                            'quiet': True,
                            'socket_timeout': timeout_2,
                            'proxy': get_proxy_url(),
                            'cookiesfrombrowser': ('firefox',),
                            'skip_download': True,
                        }
                        
                        with yt_dlp.YoutubeDL(ydl_opts_basic) as ydl:
                            info = ydl.extract_info(self.url, download=False, process=False)
                            if info:
                                print(f"DEBUG: Method 2 SUCCESS! Got basic info", flush=True)
                                self.finished.emit(info)
                                return
                    except Exception as e2:
                        print(f"DEBUG: Method 2 failed: {str(e2)[:80]}", flush=True)
                
                # METHOD 3: Try without cookies (direct connection)
                print(f"DEBUG: Method 3: Try without cookies...", flush=True)
                # B站需要更长的超时时间
                timeout_3 = 30 if is_bilibili_url(self.url) else 15
                try:
                    ydl_opts_nocookies = {
                        'quiet': True,
                        'socket_timeout': timeout_3,
                        'proxy': get_proxy_url(),
                        'user_agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
                        'skip_download': True,
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts_nocookies) as ydl:
                        info = ydl.extract_info(self.url, download=False, process=False)
                        if info:
                            print(f"DEBUG: Method 3 SUCCESS! Got info without cookies", flush=True)
                            self.finished.emit(info)
                            return
                except Exception as e3:
                    print(f"DEBUG: Method 3 failed: {str(e3)[:80]}", flush=True)
                    last_error = e3
            
            print(f"DEBUG: Fetching video info (Deno available: {deno_available})...", flush=True)
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=False)
                
                if info:
                    title = info.get('title', 'Unknown')
                    print(f"DEBUG: SUCCESS! Got video: {title[:50]}", flush=True)
                    formats = info.get('formats', [])
                    print(f"DEBUG: Formats available: {len(formats) if formats else 0}", flush=True)
                    self.finished.emit(info)
                else:
                    print(f"DEBUG: Failed - no info extracted", flush=True)
                    self.error.emit("Could not extract video information")
                return
                
        except Exception as e:
            error_str = str(e)
            print(f"DEBUG: Error: {error_str[:100]}", flush=True)
            
            # Check for JS challenge errors
            if 'challenge solving failed' in error_str or 'n challenge' in error_str:
                if not deno_available:
                    error_msg = (
                        "The video site requires JavaScript challenge solving.\n\n"
                        "Deno runtime is not available in PATH.\n"
                        "Solution:\n"
                        "1. Install Deno: curl -fsSL https://deno.land/install.sh | sh\n"
                        "2. Add to PATH: export PATH=\"$HOME/.deno/bin:$PATH\"\n"
                        "3. Restart the app"
                    )
                else:
                    error_msg = (
                        "JavaScript challenge solving failed.\n\n"
                        "Deno is installed but yt-dlp can't use it.\n"
                        "Try: pip install yt-dlp-ejs"
                    )
            elif 'Requested format is not available' in error_str:
                if not deno_available:
                    error_msg = (
                        "The video site served restricted content.\n\n"
                        "With Firefox cookies + Clash VPN, the site may only serve images.\n"
                        "Solution:\n"
                        "1. Install Deno: curl -fsSL https://deno.land/install.sh | sh\n"
                        "2. The app will automatically detect Deno in ~/.deno/bin/\n"
                        "3. Deno solves JavaScript challenges to get video formats"
                    )
                else:
                    error_msg = (
                        "The video site served restricted content (no video formats).\n\n"
                        "This usually means:\n"
                        "1. The site detected bot-like behavior\n"
                        "2. Try refreshing Firefox cookies\n"
                        "3. Wait a few minutes and try again"
                    )
            elif 'Sign in to confirm' in error_str:
                error_msg = (
                    "Bot detection detected.\n\n"
                    "Try:\n"
                    "1. Use the site in Firefox first (refresh cookies)\n"
                    "2. Wait 5-10 minutes\n"
                    "3. Try a different video"
                )
            elif 'Network is unreachable' in error_str:
                error_msg = (
                    "Cannot connect through proxy.\n\n"
                    "Check:\n"
                    "1. Proxy server is running\n"
                    "2. Firefox can access the video site\n"
                    "3. Check proxy settings in the app"
                )
            else:
                error_msg = f"Failed to fetch video: {error_str[:100]}"
            
            self.error.emit(error_msg)
        

        
        print(f"DEBUG: FetchInfoThread.run() ending", flush=True)

class DownloadThread(QThread):
    progress = Signal(float)
    status = Signal(str)
    finished = Signal(str)
    error = Signal(str)
    
    def __init__(self, url, format_spec, output_template):
        super().__init__()
        self.url = url
        self.format_spec = format_spec
        self.output_template = output_template
        
    def run(self):
        import os
        import subprocess
        
        # Check if Deno is available (same logic as FetchInfoThread)
        deno_available = False
        deno_path = None
        try:
            # First check bundled deno in same directory as executable
            # When packaged with PyInstaller, sys._MEIPASS contains temp directory
            # The deno binary should be in the same directory as the executable
            import sys
            import os
            
            # Get directory of current executable
            if getattr(sys, 'frozen', False):
                # Running as PyInstaller bundle
                exe_dir = os.path.dirname(sys.executable)
                bundled_deno = os.path.join(exe_dir, 'deno')
            else:
                # Running as script
                exe_dir = os.path.dirname(os.path.abspath(__file__))
                project_root = os.path.dirname(exe_dir)
                bundled_deno = os.path.join(project_root, 'deno')
            
            # Check common Deno installation paths (including bundled)
            common_paths = [
                bundled_deno,  # Bundled deno first
                os.path.expanduser('~/.deno/bin/deno'),  # Current user's Deno
                '/usr/local/bin/deno',
                '/usr/bin/deno',
                'deno'  # Check PATH as fallback
            ]
            
            for deno_candidate in common_paths:
                try:
                    result = subprocess.run(['which', deno_candidate] if deno_candidate == 'deno' else ['test', '-f', deno_candidate], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        deno_available = True
                        deno_path = deno_candidate if deno_candidate != 'deno' else 'deno'
                        print(f"DEBUG: DownloadThread - Deno found at: {deno_path}", flush=True)
                        break
                except Exception:
                    continue
            
            if not deno_available:
                print(f"DEBUG: DownloadThread - Deno not found in common locations", flush=True)
        except Exception:
            print(f"DEBUG: DownloadThread - Could not check for Deno", flush=True)
        
        def progress_hook(d):
            if d['status'] == 'downloading':
                # Extract percentage from progress string
                percent_str = d.get('_percent_str', '0%')
                try:
                    percent = float(percent_str.strip('%'))
                    self.progress.emit(percent)
                except ValueError:
                    pass
                    
                # Get speed and ETA
                speed = d.get('_speed_str', '')
                eta = d.get('_eta_str', '')
                status_text = f"Downloading... {speed} ETA: {eta}"
                self.status.emit(status_text)
                
            elif d['status'] == 'finished':
                self.status.emit("Processing...")
                
        # Try different cookie approaches
        approaches = [
            {'cookiesfrombrowser': ('firefox',)},  # Try Firefox first (user's setup)
            {'cookiesfrombrowser': ('chrome',)},
            {}
        ]
        
        for opts in approaches:
            try:
                # 使用智能格式选择
                actual_format = get_format_for_url(self.url, self.format_spec)
                
                ydl_opts = {
                    'format': actual_format,
                    'outtmpl': self.output_template,
                    'progress_hooks': [progress_hook],
                    'merge_output_format': 'mp4',
                    'quiet': True,
                    'no_warnings': True,
                    'proxy': get_proxy_url(),  # Add proxy
                    **opts
                }
                
                # 为B站URL添加referer头
                if is_bilibili_url(self.url):
                    ydl_opts['referer'] = 'https://www.bilibili.com'
                
                # If Deno is available, set environment to include it
                if deno_available and deno_path and deno_path != 'deno':
                    # Extract directory from deno_path
                    deno_dir = os.path.dirname(deno_path)
                    # Add to PATH for this process
                    os.environ['PATH'] = deno_dir + ':' + os.environ.get('PATH', '')
                    print(f"DEBUG: DownloadThread - Added {deno_dir} to PATH", flush=True)
                
                # Add audio format options for MP3
                if self.format_spec == 'bestaudio/best':
                    ydl_opts.update({
                        'extract_audio': True,
                        'audio_format': 'mp3',
                        'audio_quality': '0',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '0'
                        }]
                    })
                else:
                    ydl_opts.update({
                        'merge_output_format': 'mp4',
                        'postprocessors': [{
                            'key': 'FFmpegVideoConvertor',
                            'preferedformat': 'mp4'
                        }]
                    })
                    
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([self.url])
                self.finished.emit("Download complete!")
                return
            except Exception as e:
                error_str = str(e)
                print(f"DEBUG: DownloadThread - Attempt failed: {error_str[:100]}", flush=True)
                continue
        
        self.error.emit("Download failed. The video site may be blocking requests.")