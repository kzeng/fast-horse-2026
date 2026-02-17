from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, 
    QLabel, QComboBox, QProgressBar, QFileDialog, QMessageBox,
    QTabWidget, QGroupBox, QRadioButton, QFormLayout, QTextEdit
)
from PySide6.QtCore import Qt, QSettings, QTimer, Signal, QPoint
from PySide6.QtGui import QFont, QPixmap
import os
from .download_manager import FetchInfoThread, DownloadThread
from .translations import translator
from . import __version__


class TitleBar(QWidget):
    """Custom title bar for a frameless main window"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent = parent
        self.setObjectName("title_bar")
        self.setFixedHeight(40)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(8)

        # Title text
        self.title_label = QLabel(translator.get('window_title'))
        self.title_label.setObjectName("window_title_label")
        self.title_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        layout.addWidget(self.title_label)
        layout.addStretch()

        # Window control buttons
        self.min_btn = QPushButton("─")
        self.min_btn.setObjectName("btn_minimize")
        self.min_btn.setFixedSize(30, 24)
        self.min_btn.clicked.connect(self.on_minimize)

        self.max_btn = QPushButton("⬜")
        self.max_btn.setObjectName("btn_maximize")
        self.max_btn.setFixedSize(30, 24)
        self.max_btn.clicked.connect(self.on_maximize_restore)

        self.close_btn = QPushButton("✕")
        self.close_btn.setObjectName("btn_close")
        self.close_btn.setFixedSize(30, 24)
        self.close_btn.clicked.connect(self.on_close)

        layout.addWidget(self.min_btn)
        layout.addWidget(self.max_btn)
        layout.addWidget(self.close_btn)

        self._drag_pos: QPoint | None = None

    def on_minimize(self):
        if self._parent is not None:
            self._parent.showMinimized()

    def on_maximize_restore(self):
        if self._parent is None:
            return
        if self._parent.isMaximized():
            self._parent.showNormal()
        else:
            self._parent.showMaximized()

    def on_close(self):
        if self._parent is not None:
            self._parent.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self._parent is not None:
            # Prefer native system move (works best on Wayland/X11)
            window = self._parent.windowHandle()
            if window is not None:
                try:
                    # startSystemMove() doesn't take arguments in newer Qt versions
                    window.startSystemMove()
                    event.accept()
                    return
                except TypeError:
                    # Fallback for older Qt versions or if the above fails
                    pass

            # Fallback: manual move by tracking global cursor delta
            self._drag_pos = event.globalPosition().toPoint()
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._drag_pos is not None and event.buttons() & Qt.LeftButton and self._parent is not None:
            # Move window by the delta between current and previous global positions
            current_pos = event.globalPosition().toPoint()
            delta = current_pos - self._drag_pos
            self._parent.move(self._parent.pos() + delta)
            self._drag_pos = current_pos
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._drag_pos = None
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.on_maximize_restore()
            event.accept()
        else:
            super().mouseDoubleClickEvent(event)

    def update_text(self):
        """Update title text when language changes"""
        self.title_label.setText(translator.get('window_title'))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Frameless window so we can draw our own custom title bar
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setWindowTitle(translator.get('window_title'))
        self.setMinimumSize(800, 600)
        self.current_info = None
        self.is_playlist = False
        
        # Settings
        self.settings = QSettings("Fast-Horse-2026", "App")
        self.output_dir = self.settings.value("output_dir", ".")
        
        # Progress tracking - slower updates for proxy/VPN
        self.fetch_progress_stages = [
            translator.get('progress_connecting'),
            translator.get('progress_fetching'),
            translator.get('progress_processing'),
            translator.get('progress_completing')
        ]
        self.current_progress_stage = 0
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self.update_fetch_progress)
        
        # Timeout warning
        self.timeout_timer = QTimer()
        self.timeout_timer.setSingleShot(True)
        self.timeout_timer.timeout.connect(self.show_timeout_warning)
        
        # Load theme preference
        saved_theme = self.settings.value("theme", "dark")
        
        # Load stylesheet
        self.load_stylesheet(saved_theme)
        
        self.setup_tabs()
        
        # Clear any previous URL
        if hasattr(self, 'url_input'):
            self.url_input.clear()
        
    def setup_tabs(self):
        """Setup the tab widget with Main and Settings tabs"""
        self.tab_widget = QTabWidget()
        
        # Create tabs
        self.main_tab = self.create_main_tab()
        self.settings_tab = self.create_settings_tab()
        
        # Add tabs to tab widget
        self.tab_widget.addTab(self.main_tab, translator.get('tab_main'))
        self.tab_widget.addTab(self.settings_tab, translator.get('tab_settings'))
        
        # Wrap title bar + tabs in a container widget
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        # Custom title bar at the top
        self.title_bar = TitleBar(self)
        container_layout.addWidget(self.title_bar)
        container_layout.addWidget(self.tab_widget)

        # Set container as central widget
        self.setCentralWidget(container)
        
    def create_main_tab(self):
        """Create the main downloader tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel(translator.get('title_label'))
        title_label.setObjectName("title_label")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # URL Input Section
        url_layout = QHBoxLayout()
        url_layout.setSpacing(10)
        
        url_label = QLabel(translator.get('url_label'))
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText(translator.get('url_placeholder'))
        self.url_input.setMinimumHeight(35)
        
        self.fetch_btn = QPushButton(translator.get('fetch_btn'))
        self.fetch_btn.setMinimumHeight(35)
        self.fetch_btn.clicked.connect(self.fetch_video_info)
        
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input, 1)
        url_layout.addWidget(self.fetch_btn)
        layout.addLayout(url_layout)
        
        # Preview Section
        self.preview_label = QLabel(translator.get('preview_label'))
        self.preview_label.setObjectName("preview_label")
        self.preview_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.preview_label)
        
        # Format Selection
        format_layout = QHBoxLayout()
        format_layout.setSpacing(10)
        
        format_label = QLabel(translator.get('format_label'))
        self.format_combo = QComboBox()
        self.format_combo.addItems([
            translator.get('format_best'),
            translator.get('format_1080p'),
            translator.get('format_720p'),
            translator.get('format_480p'),
            translator.get('format_mp3')
        ])
        self.format_combo.setMinimumHeight(35)
        
        # Folder selection
        self.folder_btn = QPushButton("📁")
        self.folder_btn.setObjectName("folder_btn")
        self.folder_btn.setToolTip(translator.get('folder_btn'))
        self.folder_btn.setMinimumHeight(35)
        self.folder_btn.clicked.connect(self.select_folder)
        
        self.download_btn = QPushButton(translator.get('download_btn'))
        self.download_btn.setMinimumHeight(35)
        self.download_btn.clicked.connect(self.start_download)
        self.download_btn.setEnabled(False)
        
        format_layout.addWidget(format_label)
        format_layout.addWidget(self.format_combo, 1)
        format_layout.addWidget(self.folder_btn)
        format_layout.addWidget(self.download_btn)
        layout.addLayout(format_layout)
        
        # Progress Section
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimumHeight(25)
        layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel(translator.get('status_ready'))
        self.status_label.setObjectName("status_label")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Spacer
        layout.addStretch()
        
        return tab
        
        return tab
    
    def create_settings_tab(self):
        """Create the settings tab with language, theme, proxy, and about sections"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Language Section
        self.language_group = QGroupBox(translator.get('settings_language'))
        language_layout = QVBoxLayout()
        
        self.english_radio = QRadioButton(translator.get('language_english'))
        self.chinese_radio = QRadioButton(translator.get('language_chinese'))
        
        # Set current language
        current_lang = translator.current_lang
        self.english_radio.setChecked(current_lang == 'en')
        self.chinese_radio.setChecked(current_lang == 'zh')
        
        self.english_radio.clicked.connect(lambda: self.change_language('en'))
        self.chinese_radio.clicked.connect(lambda: self.change_language('zh'))
        
        language_layout.addWidget(self.english_radio)
        language_layout.addWidget(self.chinese_radio)
        self.language_group.setLayout(language_layout)
        layout.addWidget(self.language_group)
        
        # Theme Section
        self.theme_group = QGroupBox(translator.get('settings_theme'))
        theme_layout = QVBoxLayout()
        
        self.dark_radio = QRadioButton(translator.get('theme_dark'))
        self.light_radio = QRadioButton(translator.get('theme_light'))
        
        # Set current theme
        saved_theme = self.settings.value("theme", "dark")
        self.dark_radio.setChecked(saved_theme == 'dark')
        self.light_radio.setChecked(saved_theme == 'light')
        
        self.dark_radio.clicked.connect(lambda: self.change_theme('dark'))
        self.light_radio.clicked.connect(lambda: self.change_theme('light'))
        
        theme_layout.addWidget(self.dark_radio)
        theme_layout.addWidget(self.light_radio)
        self.theme_group.setLayout(theme_layout)
        layout.addWidget(self.theme_group)
        
        # Proxy Settings Section
        self.proxy_group = QGroupBox(translator.get('settings_proxy'))
        proxy_layout = QFormLayout()
        
        # Proxy type
        self.proxy_type_combo = QComboBox()
        self.proxy_type_combo.addItems([
            translator.get('settings_proxy_none'),
            translator.get('settings_proxy_socks5'),
            translator.get('settings_proxy_http')
        ])
        proxy_layout.addRow(translator.get('settings_proxy_type') + ":", self.proxy_type_combo)
        
        # Proxy host
        self.proxy_host_input = QLineEdit()
        self.proxy_host_input.setPlaceholderText("127.0.0.1")
        proxy_layout.addRow(translator.get('settings_proxy_host'), self.proxy_host_input)
        
        # Proxy port
        self.proxy_port_input = QLineEdit()
        self.proxy_port_input.setPlaceholderText("10808")
        proxy_layout.addRow(translator.get('settings_proxy_port'), self.proxy_port_input)
        
        # Save proxy button
        self.save_proxy_btn = QPushButton(translator.get('settings_save'))
        self.save_proxy_btn.clicked.connect(self.save_proxy_settings)
        proxy_layout.addRow("", self.save_proxy_btn)
        
        self.proxy_group.setLayout(proxy_layout)
        layout.addWidget(self.proxy_group)
        
        # About Section
        self.about_group = QGroupBox(translator.get('settings_about'))
        
        # Use horizontal layout for about section (text on left, image on right)
        about_main_layout = QHBoxLayout()
        
        # Text on left
        about_text_layout = QVBoxLayout()
        
        self.about_text = QTextEdit()
        self.about_text.setReadOnly(True)
        self.about_text.setPlainText(
            f"{translator.get('about_description')}\n\n"
            f"{translator.get('about_author')}\n"
            f"{translator.get('about_version')} v{__version__}"
        )
        self.about_text.setMaximumHeight(120)
        self.about_text.setMaximumWidth(400)
        
        about_text_layout.addWidget(self.about_text)
        about_main_layout.addLayout(about_text_layout)
        
        # Image on right
        self.horse_image_label = QLabel()
        self.horse_image_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.horse_image_label.setObjectName("horse_image_label")
        about_main_layout.addWidget(self.horse_image_label)
        
        # Load horse image
        self.load_horse_image()
        
        self.about_group.setLayout(about_main_layout)
        layout.addWidget(self.about_group)
        
        # Spacer
        layout.addStretch()
        
        # Load current proxy settings
        self.load_proxy_settings()
        
        return tab
    
    def change_language(self, lang_code):
        """Change application language"""
        if translator.set_language(lang_code):
            # Update tab titles
            self.tab_widget.setTabText(0, translator.get('tab_main'))
            self.tab_widget.setTabText(1, translator.get('tab_settings'))
            
            # Update UI text
            self.update_ui_text()
            
            # Update settings tab content
            self.update_settings_tab()
    
    def change_theme(self, theme):
        """Change application theme"""
        self.load_stylesheet(theme)
        
        # Update theme radio buttons
        if hasattr(self, 'dark_radio') and hasattr(self, 'light_radio'):
            self.dark_radio.setChecked(theme == 'dark')
            self.light_radio.setChecked(theme == 'light')
    
    def load_proxy_settings(self):
        """Load current proxy settings from QSettings"""
        proxy_type = self.settings.value("proxy_type", translator.get('settings_proxy_socks5'))
        proxy_host = self.settings.value("proxy_host", "127.0.0.1")
        proxy_port = self.settings.value("proxy_port", "10808")
        
        # Set proxy type
        if proxy_type == translator.get('settings_proxy_none'):
            self.proxy_type_combo.setCurrentIndex(0)
        elif proxy_type == translator.get('settings_proxy_socks5'):
            self.proxy_type_combo.setCurrentIndex(1)
        elif proxy_type == translator.get('settings_proxy_http'):
            self.proxy_type_combo.setCurrentIndex(2)
        
        self.proxy_host_input.setText(proxy_host)
        self.proxy_port_input.setText(proxy_port)
    
    def save_proxy_settings(self):
        """Save proxy settings to QSettings"""
        proxy_type = self.proxy_type_combo.currentText()
        proxy_host = self.proxy_host_input.text().strip()
        proxy_port = self.proxy_port_input.text().strip()
        
        # Validate port
        if proxy_type != translator.get('settings_proxy_none'):
            if not proxy_host:
                QMessageBox.warning(self, "Warning", "Please enter proxy host")
                return
            if not proxy_port:
                QMessageBox.warning(self, "Warning", "Please enter proxy port")
                return
            try:
                port = int(proxy_port)
                if port < 1 or port > 65535:
                    raise ValueError
            except ValueError:
                QMessageBox.warning(self, "Warning", "Please enter a valid port number (1-65535)")
                return
        
        # Save settings
        self.settings.setValue("proxy_type", proxy_type)
        self.settings.setValue("proxy_host", proxy_host)
        self.settings.setValue("proxy_port", proxy_port)
        
        QMessageBox.information(self, "Success", "Proxy settings saved successfully")
    
    def update_settings_tab(self):
        """Update settings tab content when language changes"""
        if hasattr(self, 'language_group'):
            self.language_group.setTitle(translator.get('settings_language'))
            self.english_radio.setText(translator.get('language_english'))
            self.chinese_radio.setText(translator.get('language_chinese'))
            
            self.theme_group.setTitle(translator.get('settings_theme'))
            self.dark_radio.setText(translator.get('theme_dark'))
            self.light_radio.setText(translator.get('theme_light'))
            
            self.proxy_group.setTitle(translator.get('settings_proxy'))
            self.save_proxy_btn.setText(translator.get('settings_save'))
            
            self.about_group.setTitle(translator.get('settings_about'))
            about_text = f"{translator.get('about_description')}\n\n{translator.get('about_author')}\n{translator.get('about_version')} v{__version__}"
            if hasattr(self, 'about_text'):
                self.about_text.setPlainText(about_text)
    
    def load_stylesheet(self, theme='dark'):
        """Load the application stylesheet"""
        if theme == 'dark':
            style_file = 'style.qss'
        else:
            style_file = 'style_light.qss'
            
        # Get the directory of this module
        current_dir = os.path.dirname(os.path.abspath(__file__))
        style_path = os.path.join(current_dir, style_file)
        
        if os.path.exists(style_path):
            with open(style_path, 'r') as f:
                self.setStyleSheet(f.read())
        
        # Save theme preference
        self.settings.setValue("theme", theme)
        
        # Update horse image for theme
        self.load_horse_image()
    
    def load_horse_image(self):
        """Load and display the horse image with appropriate scaling"""
        if not hasattr(self, 'horse_image_label'):
            return
            
        # Get project root directory (one level up from app directory)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        image_path = os.path.join(project_root, "horse2026.jpeg")
        
        if os.path.exists(image_path):
            # Load pixmap
            pixmap = QPixmap(image_path)
            
            # Scale to fit in About section - max 150px width, 120px height
            max_width = 150
            max_height = 120
            
            if pixmap.width() > max_width or pixmap.height() > max_height:
                pixmap = pixmap.scaled(
                    max_width, max_height,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            
            self.horse_image_label.setPixmap(pixmap)
            self.horse_image_label.setFixedSize(pixmap.size())
    
    def resizeEvent(self, event):
        """Handle window resize to update horse image scaling"""
        super().resizeEvent(event)
        self.load_horse_image()
        
    def fetch_video_info(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, translator.get('error_no_url'), translator.get('error_no_url'))
            return
            
        # Start progress updates
        self.current_progress_stage = 0
        self.status_label.setText(self.fetch_progress_stages[0])
        self.fetch_btn.setEnabled(False)
        
        # Start progress timer (update every 2.5 seconds - slower for proxy)
        self.progress_timer.start(2500)
        
        # B站URL需要更长的超时时间
        if 'bilibili.com' in url.lower() or 'b23.tv' in url.lower():
            timeout_duration = 25000  # 25秒 for B站
        else:
            timeout_duration = 12000  # 12秒 for 其他网站
        
        # Start timeout timer
        self.timeout_timer.start(timeout_duration)
        
        # Start the fetch thread
        self.fetch_thread = FetchInfoThread(url)
        self.fetch_thread.finished.connect(self.on_fetch_complete, Qt.QueuedConnection)
        self.fetch_thread.error.connect(self.on_fetch_error, Qt.QueuedConnection)
        self.fetch_thread.start()
        
    def update_fetch_progress(self):
        """Update progress text during fetch operation"""
        if self.current_progress_stage < len(self.fetch_progress_stages) - 1:
            self.current_progress_stage += 1
            self.status_label.setText(self.fetch_progress_stages[self.current_progress_stage])
        else:
            # If we've gone through all stages, show a waiting message
            self.status_label.setText("Still working...")
    
    def show_timeout_warning(self):
        """Update status if fetch is taking longer than expected"""
        if self.fetch_thread and self.fetch_thread.isRunning():
            # Just update status text, don't show intrusive message box
            url = self.url_input.text().lower()
            if 'bilibili.com' in url or 'b23.tv' in url:
                self.status_label.setText("B站视频较大，请耐心等待...")
                self.status_label.setToolTip(
                    "B站视频可能较大，需要更多时间下载元数据。\n"
                    "请耐心等待，如果超过30秒仍无响应，请检查网络连接。"
                )
            else:
                self.status_label.setText("Still fetching... (using Firefox config)")
                self.status_label.setToolTip(
                    "Fetching is taking longer than usual.\n"
                    "The app is using Firefox configuration.\n"
                    "This may be due to YouTube server response time."
                )
    
    def on_fetch_complete(self, info):
        # Stop timers
        self.progress_timer.stop()
        self.timeout_timer.stop()
        
        self.current_info = info
        self.fetch_btn.setEnabled(True)
        
        if 'entries' in info:
            # It's a playlist
            count = len(info['entries'])
            self.preview_label.setText(
                f"🎬 Playlist: {info['title']}\n"
                f"📊 Videos: {count}\n"
                f"👤 Uploader: {info.get('uploader', 'Unknown')}"
            )
            self.is_playlist = True
        else:
            # Single video
            duration = info.get('duration', 0)
            # 修复：duration可能是浮点数，需要转换为整数
            duration_sec_int = int(duration)
            duration_min = duration_sec_int // 60
            duration_sec = duration_sec_int % 60
            self.preview_label.setText(
                f"🎬 Title: {info['title']}\n"
                f"⏱️ Duration: {duration_min}:{duration_sec:02d}\n"
                f"👤 Uploader: {info.get('uploader', 'Unknown')}\n"
                f"👁️ Views: {info.get('view_count', 'N/A')}"
            )
            self.is_playlist = False
            
        self.status_label.setText(translator.get('status_ready'))
        self.download_btn.setEnabled(True)
        
    def on_fetch_error(self, error):
        # Stop timers
        self.progress_timer.stop()
        self.timeout_timer.stop()
        
        self.fetch_btn.setEnabled(True)
        
        # Show a shorter error in status
        short_error = error[:100] + "..." if len(error) > 100 else error
        self.status_label.setText(f"Error: {short_error}")
        
        # Show appropriate error message based on error type
        if "Sign in to confirm you're not a bot" in error:
            QMessageBox.warning(self, translator.get('error_network'), 
                "The video site is blocking requests. Please:\n\n"
                "1. Make sure you're logged into the site in Firefox\n"
                "2. Try again (the app will use Firefox cookies)\n\n"
                "If this doesn't work, the site may be blocking your IP/VPN.")
                
        elif "JavaScript challenge" in error or "Deno runtime" in error:
            # JS challenge error - needs Deno installation
            QMessageBox.critical(self, translator.get('error_deno'),
                "The video site requires JavaScript challenge solving.\n\n" +
                error + "\n\n"
                "After installing Deno, restart the app.")
            
        elif "Network connection failed" in error or "Connection timed out" in error:
            # Network-related error from download_manager
            QMessageBox.critical(self, "Network Error", error)
            
        elif "Network is unreachable" in error or "Errno 101" in error or "system proxy" in error.lower():
            # Direct network error or proxy issue
            QMessageBox.critical(self, "Network/Proxy Issue",
                "Cannot connect to the video site. Since your Firefox uses system proxy settings:\n\n"
                "1. Your Clash VPN may be blocking the site API\n"
                "2. Try disabling Clash VPN temporarily\n"
                "3. Or configure Clash to allow the site API access\n"
                "4. Check if the site works in Firefox first\n"
                "5. Try a different network without VPN\n\n"
                "Error: " + error[:200])
                
        else:
            # Other error
            QMessageBox.critical(self, "Error", f"Failed to fetch video:\n{error[:300]}")
        
    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, translator.get('folder_btn'))
        if folder:
            self.output_dir = folder
            self.settings.setValue("output_dir", folder)
            self.status_label.setText(f"Download folder: {folder}")
            
    def start_download(self):
        if not self.current_info:
            QMessageBox.warning(self, translator.get('error_fetch_first'), translator.get('error_fetch_first'))
            return
            
        url = self.url_input.text().strip()
        
        # Map format selection to yt-dlp format spec
        format_map = {
            "Best Available": "best",
            "MP4 1080p": "bestvideo[height<=1080]+bestaudio/best",
            "MP4 720p": "bestvideo[height<=720]+bestaudio/best", 
            "MP4 480p": "bestvideo[height<=480]+bestaudio/best",
            "MP3 Audio": "bestaudio/best"
        }
        format_spec = format_map[self.format_combo.currentText()]
        
        # Prepare output template
        if self.is_playlist:
            output_template = f'{self.output_dir}/%(playlist_title)s/%(title)s.%(ext)s'
        else:
            output_template = f'{self.output_dir}/%(title)s.%(ext)s'
            
        self.download_thread = DownloadThread(url, format_spec, output_template)
        self.download_thread.progress.connect(self.update_progress)
        self.download_thread.status.connect(self.status_label.setText)
        self.download_thread.finished.connect(self.on_download_complete)
        self.download_thread.error.connect(self.on_download_error)
        self.download_thread.start()
        
        self.download_btn.setEnabled(False)
        self.fetch_btn.setEnabled(False)
        
    def update_progress(self, value):
        self.progress_bar.setValue(int(value))
        
    def on_download_complete(self, message):
        self.download_btn.setEnabled(True)
        self.fetch_btn.setEnabled(True)
        self.status_label.setText(message)
        self.progress_bar.setValue(100)
        QMessageBox.information(self, translator.get('status_complete'), translator.get('status_complete'))
        
    def on_download_error(self, error):
        self.download_btn.setEnabled(True)
        self.fetch_btn.setEnabled(True)
        self.status_label.setText(f"{translator.get('status_error')}{error}")
        QMessageBox.critical(self, translator.get('status_error'), f"Download failed:\n{error}")
    
    def update_ui_text(self):
        """Update all UI text when language changes"""
        self.setWindowTitle(translator.get('window_title'))
        # Update custom title bar text if present
        if hasattr(self, 'title_bar'):
            self.title_bar.update_text()
        
        # Update progress stages
        self.fetch_progress_stages = [
            translator.get('progress_connecting'),
            translator.get('progress_fetching'),
            translator.get('progress_processing'),
            translator.get('progress_completing')
        ]
        
        # Update tab titles
        if hasattr(self, 'tab_widget'):
            self.tab_widget.setTabText(0, translator.get('tab_main'))
            self.tab_widget.setTabText(1, translator.get('tab_settings'))
        
        # Find and update all widgets
        for widget in self.findChildren(QLabel):
            if widget.text() in ["YouTube Video Downloader", "YouTube URL:", "Format:", "Ready"]:
                if widget.text() == "YouTube Video Downloader":
                    widget.setText(translator.get('title_label'))
                elif widget.text() == "YouTube URL:":
                    widget.setText(translator.get('url_label'))
                elif widget.text() == "Format:":
                    widget.setText(translator.get('format_label'))
                elif widget.text() == "Ready":
                    widget.setText(translator.get('status_ready'))
        
        # Update buttons
        self.fetch_btn.setText(translator.get('fetch_btn'))
        self.download_btn.setText(translator.get('download_btn'))
        self.folder_btn.setToolTip(translator.get('folder_btn'))
        
        # Update combo box
        current_index = self.format_combo.currentIndex()
        self.format_combo.clear()
        self.format_combo.addItems([
            translator.get('format_best'),
            translator.get('format_1080p'),
            translator.get('format_720p'),
            translator.get('format_480p'),
            translator.get('format_mp3')
        ])
        self.format_combo.setCurrentIndex(current_index)
        
        # Update preview label if it's the default text
        if self.preview_label.text() == "No video loaded":
            self.preview_label.setText(translator.get('preview_label'))
        
        # Update settings tab
        self.update_settings_tab()