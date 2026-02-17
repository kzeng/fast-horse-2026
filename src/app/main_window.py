from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, 
    QLabel, QComboBox, QProgressBar, QFileDialog, QMessageBox,
    QMenuBar, QMenu
)
from PySide6.QtCore import Qt, QSettings, QTimer
from PySide6.QtGui import QFont
import os
from .download_manager import FetchInfoThread, DownloadThread
from .translations import translator
from .settings_dialog import SettingsDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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
        
        self.setup_ui()
        
        # Clear any previous URL
        self.url_input.clear()
        
    def setup_menu_bar(self):
        """Setup the menu bar with language and theme options"""
        menu_bar = QMenuBar(self)
        
        # File menu
        file_menu = menu_bar.addMenu(translator.get('menu_file'))
        exit_action = file_menu.addAction(translator.get('menu_exit'))
        exit_action.triggered.connect(self.close)
        
        # Settings menu
        settings_menu = menu_bar.addMenu(translator.get('menu_settings'))
        
        # Proxy settings action
        proxy_action = settings_menu.addAction("Proxy Settings")
        proxy_action.triggered.connect(self.show_proxy_settings)
        
        settings_menu.addSeparator()
        
        # Language submenu
        language_menu = settings_menu.addMenu(translator.get('menu_language'))
        self.english_action = language_menu.addAction(translator.get('menu_english'))
        self.chinese_action = language_menu.addAction(translator.get('menu_chinese'))
        
        self.english_action.triggered.connect(lambda: self.change_language('en'))
        self.chinese_action.triggered.connect(lambda: self.change_language('zh'))
        
        # Theme submenu
        theme_menu = settings_menu.addMenu(translator.get('menu_theme'))
        self.dark_action = theme_menu.addAction(translator.get('menu_dark'))
        self.light_action = theme_menu.addAction(translator.get('menu_light'))
        
        # Make theme actions checkable
        self.dark_action.setCheckable(True)
        self.light_action.setCheckable(True)
        
        # Set initial check state based on saved theme
        saved_theme = self.settings.value("theme", "dark")
        self.dark_action.setChecked(saved_theme == 'dark')
        self.light_action.setChecked(saved_theme == 'light')
        
        self.dark_action.triggered.connect(lambda: self.change_theme('dark'))
        self.light_action.triggered.connect(lambda: self.change_theme('light'))
        
        # Help menu
        help_menu = menu_bar.addMenu(translator.get('menu_help'))
        about_action = help_menu.addAction(translator.get('menu_about'))
        about_action.triggered.connect(self.show_about)
        
        # Set menu bar
        self.setMenuBar(menu_bar)
        
    def change_language(self, lang_code):
        """Change application language"""
        if translator.set_language(lang_code):
            self.update_ui_text()
            # Update menu text
            self.update_menu_text()
            
    def update_menu_text(self):
        """Update menu text when language changes"""
        # This would need to be implemented if we store menu references
        pass
        
    def show_proxy_settings(self):
        """Show proxy settings dialog"""
        dialog = SettingsDialog(self)
        dialog.exec()
        
    def show_about(self):
        """Show about dialog"""
        QMessageBox.information(self, 
                              translator.get('about_title'),
                              f"{translator.get('about_description')}\n\n{translator.get('about_version')}")
        
    def setup_ui(self):
        # Create central widget for QMainWindow
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Menu Bar
        self.setup_menu_bar()
        
        # Content layout
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # Title
        title_label = QLabel(translator.get('title_label'))
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
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setStyleSheet("""
            QLabel {
                background-color: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-radius: 8px;
                padding: 20px;
                margin: 10px 0;
            }
        """)
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
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Spacer
        layout.addStretch()
        
        # Add content layout to main layout
        main_layout.addLayout(layout)
        
    def load_stylesheet(self, theme='dark'):
        """Load the application stylesheet"""
        if theme == 'dark':
            style_file = 'style.qss'
        else:
            style_file = 'style_light.qss'
            
        style_path = os.path.join(os.path.dirname(__file__), style_file)
        if os.path.exists(style_path):
            with open(style_path, 'r') as f:
                self.setStyleSheet(f.read())
        
        # Save theme preference
        self.settings.setValue("theme", theme)
    
    def change_theme(self, theme):
        """Change application theme"""
        self.load_stylesheet(theme)
        
        # Update theme menu check state
        if hasattr(self, 'dark_action') and hasattr(self, 'light_action'):
            # Uncheck both first
            self.dark_action.setChecked(False)
            self.light_action.setChecked(False)
            
            # Check the selected theme
            if theme == 'dark':
                self.dark_action.setChecked(True)
            else:
                self.light_action.setChecked(True)
        
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
        
        # Start timeout timer (show status update after 12 seconds)
        self.timeout_timer.start(12000)
        
        # Start the fetch thread
        self.fetch_thread = FetchInfoThread(url)
        self.fetch_thread.finished.connect(self.on_fetch_complete)
        self.fetch_thread.error.connect(self.on_fetch_error)
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
            self.status_label.setText("Still fetching... (using Firefox config)")
            # Optional: Show tooltip instead of message box
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
            duration_min = info.get('duration', 0) // 60
            duration_sec = info.get('duration', 0) % 60
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
                "YouTube is blocking requests. Please:\n\n"
                "1. Make sure you're logged into YouTube in Firefox\n"
                "2. Try again (the app will use Firefox cookies)\n\n"
                "If this doesn't work, YouTube may be blocking your IP/VPN.")
                
        elif "YouTube requires JavaScript challenge" in error or "Deno runtime" in error:
            # JS challenge error - needs Deno installation
            QMessageBox.critical(self, translator.get('error_deno'),
                "YouTube requires JavaScript challenge solving.\n\n" +
                error + "\n\n" +
                "After installing Deno, restart the app.")
            
        elif "Network connection failed" in error or "Connection timed out" in error:
            # Network-related error from download_manager
            QMessageBox.critical(self, "Network Error", error)
            
        elif "Network is unreachable" in error or "Errno 101" in error or "system proxy" in error.lower():
            # Direct network error or proxy issue
            QMessageBox.critical(self, "Network/Proxy Issue",
                "Cannot connect to YouTube. Since your Firefox uses system proxy settings:\n\n"
                "1. Your Clash VPN may be blocking YouTube API\n"
                "2. Try disabling Clash VPN temporarily\n"
                "3. Or configure Clash to allow YouTube API access\n"
                "4. Check if YouTube works in Firefox first\n"
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
        
        # Update progress stages
        self.fetch_progress_stages = [
            translator.get('progress_connecting'),
            translator.get('progress_fetching'),
            translator.get('progress_processing'),
            translator.get('progress_completing')
        ]
        
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
        
        # Update menu bar if it exists
        menu_bar = self.menuBar()
        if menu_bar:
            # Update File menu
            file_menu = menu_bar.actions()[0].menu()
            if file_menu:
                file_menu.setTitle(translator.get('menu_file'))
                file_menu.actions()[0].setText(translator.get('menu_exit'))
            
            # Update Settings menu
            settings_menu = menu_bar.actions()[1].menu()
            if settings_menu:
                settings_menu.setTitle(translator.get('menu_settings'))
                
                # Update Proxy Settings action
                settings_menu.actions()[0].setText("Proxy Settings")
                
                # Update Language submenu
                language_menu = settings_menu.actions()[2].menu()
                if language_menu:
                    language_menu.setTitle(translator.get('menu_language'))
                    language_menu.actions()[0].setText(translator.get('menu_english'))
                    language_menu.actions()[1].setText(translator.get('menu_chinese'))
                
                # Update Theme submenu
                theme_menu = settings_menu.actions()[3].menu()
                if theme_menu:
                    theme_menu.setTitle(translator.get('menu_theme'))
                    theme_menu.actions()[0].setText(translator.get('menu_dark'))
                    theme_menu.actions()[1].setText(translator.get('menu_light'))
            
            # Update Help menu
            help_menu = menu_bar.actions()[2].menu()
            if help_menu:
                help_menu.setTitle(translator.get('menu_help'))
                help_menu.actions()[0].setText(translator.get('menu_about'))