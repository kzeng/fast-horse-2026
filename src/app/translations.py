# Translations for Fast-Horse-2026
# Supports Chinese and English

from PySide6.QtCore import QLocale, QTranslator
import os

class Translator:
    """Translation manager for Fast-Horse-2026"""
    
    def __init__(self):
        self.translations = {
            'en': self._english_translations(),
            'zh': self._chinese_translations()
        }
        self.current_lang = 'en'
        
    def _english_translations(self):
        """English translations"""
        return {
            # Window title
            'window_title': "Fast Horse 2026 - Resource Downloader",

            # Tabs
            'tab_main': "Main",
            'tab_settings': "Settings",

            # Settings tab sections
            'settings_language': "Language",
            'settings_theme': "Theme",
            'settings_proxy': "Proxy Settings",
            'settings_about': "About",
            'settings_show_thumbnail': "Show Thumbnail",

            # Language options
            'language_english': "English",
            'language_chinese': "中文",

            # Theme options
            'theme_dark': "Dark",
            'theme_light': "Light",

            # About section
            'about_author': "Author: Zengkai001@qq.com",
            'about_version': "Version: 0.0.2",
            'about_description': "A fast video downloader with proxy support for YouTube, Bilibili, and more",

            # Main UI
            'title_label': "Fast Horse 2026 - Resource Downloader",
            'url_label': "Resource URL:",
            'url_placeholder': "Paste YouTube or Bilibili URL here...",
            'fetch_btn': "Fetch Info",
            'preview_label': "No video loaded",
            'format_label': "Format:",
            'format_best': "Best Available",
            'format_1080p': "MP4 1080p",
            'format_720p': "MP4 720p", 
            'format_480p': "MP4 480p",
            'format_mp3': "MP3 Audio",
            
            # Folder selection
            'folder_btn': "Select Folder",
            'download_btn': "Download",
            
            # Status messages
            'status_ready': "Ready",
            'status_fetching': "Fetching video info...",
            'status_downloading': "Downloading...",
            'status_complete': "Download complete!",
            'status_error': "Error: ",
            
            # Progress stages
            'progress_connecting': "Connecting through proxy...",
            'progress_fetching': "Fetching video info...",
            'progress_processing': "Processing response...",
            'progress_completing': "Almost complete...",
            
            # Error messages
            'error_no_url': "Please enter a resource URL",
            'error_fetch_first': "Please fetch resource info first",
            'error_network': "Network error. Check proxy settings.",
            'error_deno': "Deno not found. Install Deno for JS challenges.",
            
            # Settings
            'settings_title': "Settings",
            'settings_proxy': "Proxy Settings",
            'settings_proxy_type': "Proxy Type",
            'settings_proxy_host': "Proxy Host:",
            'settings_proxy_port': "Proxy Port:",
            'settings_proxy_none': "No Proxy",
            'settings_proxy_socks5': "SOCKS5",
            'settings_proxy_http': "HTTP",
            'settings_save': "Save",
            'settings_cancel': "Cancel",
            
            # About (old - keeping for compatibility)
            'about_title': "About Fast Horse 2026",
            'about_github': "GitHub Repository",
            
            # Video info
            'video_title': "Title: ",
            'video_duration': "Duration: ",
            'video_uploader': "Uploader: ",
            'video_views': "Views: ",
        }
    
    def _chinese_translations(self):
        """Chinese translations"""
        return {
            # Window title
            'window_title': "快马2026 - 资源下载器",

            # Tabs
            'tab_main': "主界面",
            'tab_settings': "设置",

            # Settings tab sections
            'settings_language': "语言",
            'settings_theme': "主题",
            'settings_proxy': "代理设置",
            'settings_about': "关于",
            'settings_show_thumbnail': "显示封面",

            # Language options
            'language_english': "English",
            'language_chinese': "中文",

            # Theme options
            'theme_dark': "深色",
            'theme_light': "浅色",

            # About section
            'about_author': "作者: Zengkai001@qq.com",
            'about_version': "版本: 0.0.2",
            'about_description': "支持代理的快速视频下载器，支持YouTube、B站等",

            # Main UI
            'title_label': "快马2026 - 资源下载器",
            'url_label': "资源链接:",
            'url_placeholder': "粘贴YouTube或B站链接到这里...",
            'fetch_btn': "获取信息",
            'preview_label': "未加载视频",
            'format_label': "格式:",
            'format_best': "最佳可用",
            'format_1080p': "MP4 1080p",
            'format_720p': "MP4 720p",
            'format_480p': "MP4 480p",
            'format_mp3': "MP3音频",
            
            # Folder selection
            'folder_btn': "选择文件夹",
            'download_btn': "下载",
            
            # Status messages
            'status_ready': "就绪",
            'status_fetching': "正在获取视频信息...",
            'status_downloading': "正在下载...",
            'status_complete': "下载完成!",
            'status_error': "错误: ",
            
            # Progress stages
            'progress_connecting': "正在通过代理连接...",
            'progress_fetching': "正在获取视频信息...",
            'progress_processing': "正在处理响应...",
            'progress_completing': "即将完成...",
            
            # Error messages
            'error_no_url': "请输入资源链接",
            'error_fetch_first': "请先获取资源信息",
            'error_fetch_first': "请先获取视频信息",
            'error_network': "网络错误。请检查代理设置。",
            'error_deno': "未找到Deno。请安装Deno以解决JS挑战。",
            
            # Settings
            'settings_title': "设置",
            'settings_proxy': "代理设置",
            'settings_proxy_type': "代理类型",
            'settings_proxy_host': "代理主机:",
            'settings_proxy_port': "代理端口:",
            'settings_proxy_none': "无代理",
            'settings_proxy_socks5': "SOCKS5",
            'settings_proxy_http': "HTTP",
            'settings_save': "保存",
            'settings_cancel': "取消",
            
            # About (old - keeping for compatibility)
            'about_title': "关于快马2026",
            'about_github': "GitHub仓库",
            
            # Video info
            'video_title': "标题: ",
            'video_duration': "时长: ",
            'video_uploader': "上传者: ",
            'video_views': "观看次数: ",
        }
    
    def get(self, key, default=None):
        """Get translation for current language"""
        return self.translations.get(self.current_lang, {}).get(key, default or key)
    
    def set_language(self, lang_code):
        """Set current language"""
        if lang_code in self.translations:
            self.current_lang = lang_code
            return True
        return False
    
    def get_available_languages(self):
        """Get list of available language codes"""
        return list(self.translations.keys())
    
    def get_language_name(self, lang_code):
        """Get display name for language code"""
        names = {
            'en': 'English',
            'zh': '中文'
        }
        return names.get(lang_code, lang_code)

# Global translator instance
translator = Translator()