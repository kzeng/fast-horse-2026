# Proxy settings dialog for Fast-Horse-2026

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QComboBox, QLineEdit, QPushButton, QFormLayout,
    QMessageBox
)
from PySide6.QtCore import Qt, QSettings
from .translations import translator

class SettingsDialog(QDialog):
    """Dialog for configuring proxy settings"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(translator.get('settings_title'))
        self.setMinimumWidth(400)
        
        self.settings = QSettings("Fast-Horse-2026", "App")
        
        self.setup_ui()
        self.load_settings()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Proxy settings section
        proxy_label = QLabel(translator.get('settings_proxy'))
        proxy_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(proxy_label)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        # Proxy type
        self.proxy_type_combo = QComboBox()
        self.proxy_type_combo.addItems([
            translator.get('settings_proxy_none'),
            translator.get('settings_proxy_socks5'),
            translator.get('settings_proxy_http')
        ])
        form_layout.addRow(translator.get('settings_proxy_type') + ":", self.proxy_type_combo)
        
        # Proxy host
        self.proxy_host_input = QLineEdit()
        self.proxy_host_input.setPlaceholderText("127.0.0.1")
        form_layout.addRow(translator.get('settings_proxy_host'), self.proxy_host_input)
        
        # Proxy port
        self.proxy_port_input = QLineEdit()
        self.proxy_port_input.setPlaceholderText("10808")
        form_layout.addRow(translator.get('settings_proxy_port'), self.proxy_port_input)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.save_btn = QPushButton(translator.get('settings_save'))
        self.save_btn.clicked.connect(self.save_settings)
        
        self.cancel_btn = QPushButton(translator.get('settings_cancel'))
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
        
    def load_settings(self):
        """Load current settings from QSettings"""
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
        
    def save_settings(self):
        """Save settings to QSettings"""
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
        
        QMessageBox.information(self, "Success", "Settings saved successfully")
        self.accept()
        
    def get_proxy_url(self):
        """Get proxy URL from settings"""
        proxy_type = self.settings.value("proxy_type", translator.get('settings_proxy_socks5'))
        proxy_host = self.settings.value("proxy_host", "127.0.0.1")
        proxy_port = self.settings.value("proxy_port", "10808")
        
        if proxy_type == translator.get('settings_proxy_none'):
            return None
        elif proxy_type == translator.get('settings_proxy_socks5'):
            return f"socks5://{proxy_host}:{proxy_port}"
        elif proxy_type == translator.get('settings_proxy_http'):
            return f"http://{proxy_host}:{proxy_port}"
        else:
            return f"socks5://{proxy_host}:{proxy_port}"