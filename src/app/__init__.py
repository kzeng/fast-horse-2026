"""
Fast-Horse-2026 YouTube Downloader Application
"""

__version__ = "0.0.2"
__author__ = "Zengkai001@qq.com"
__description__ = "Fast-Horse-2026 YouTube Downloader"
__license__ = "MIT"

# Application metadata
APP_NAME = "Fast-Horse-2026"
APP_VERSION = __version__
APP_AUTHOR = __author__
APP_DESCRIPTION = __description__

def get_version():
    """Get the application version"""
    return __version__

def get_app_info():
    """Get complete application information"""
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "author": APP_AUTHOR,
        "description": APP_DESCRIPTION,
        "license": __license__
    }