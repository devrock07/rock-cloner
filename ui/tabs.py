import sys
import discord
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QTextEdit, QProgressBar, QGroupBox, 
                            QCheckBox, QMessageBox, QPushButton, QFrame)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from utils.constants import DEFAULT_PREFERENCES, SUPPORT_LINK

class CloningTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # Input section
        input_group = QGroupBox("Server Information")
        input_group.setStyleSheet(self.get_groupbox_style())
        
        input_layout = QVBoxLayout(input_group)
        
        # Token input
        token_layout = QHBoxLayout()
        token_label = QLabel("User Token:")
        token_label.setStyleSheet("color: #ADAFB4; min-width: 120px;")
        self.main_window.token_input = QLineEdit()
        self.main_window.token_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.main_window.token_input.setPlaceholderText("Enter your Discord bot token...")
        self.setup_input_style(self.main_window.token_input)
        token_layout.addWidget(token_label)
        token_layout.addWidget(self.main_window.token_input)
        input_layout.addLayout(token_layout)
        
        # Server IDs
        server_layout = QHBoxLayout()
        
        source_layout = QVBoxLayout()
        source_label = QLabel("Source Server ID:")
        source_label.setStyleSheet("color: #ADAFB4;")
        self.main_window.source_input = QLineEdit()
        self.main_window.source_input.setPlaceholderText("Server ID to clone FROM...")
        self.setup_input_style(self.main_window.source_input)
        source_layout.addWidget(source_label)
        source_layout.addWidget(self.main_window.source_input)
        
        dest_layout = QVBoxLayout()
        dest_label = QLabel("Destination Server ID:")
        dest_label.setStyleSheet("color: #ADAFB4;")
        self.main_window.dest_input = QLineEdit()
        self.main_window.dest_input.setPlaceholderText("Server ID to clone TO...")
        self.setup_input_style(self.main_window.dest_input)
        dest_layout.addWidget(dest_label)
        dest_layout.addWidget(self.main_window.dest_input)
        
        server_layout.addLayout(source_layout)
        server_layout.addLayout(dest_layout)
        input_layout.addLayout(server_layout)
        
        layout.addWidget(input_group)
        
        # Progress section
        progress_group = QGroupBox("Cloning Progress")
        progress_group.setStyleSheet(self.get_groupbox_style())
        progress_layout = QVBoxLayout(progress_group)
        
        self.main_window.progress_bar = QProgressBar()
        self.main_window.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #1E1F22;
                border-radius: 5px;
                text-align: center;
                color: white;
                background-color: #2B2D31;
                height: 25px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5865F2, stop:1 #57F287);
                border-radius: 3px;
            }
        """)
        progress_layout.addWidget(self.main_window.progress_bar)
        
        self.main_window.status_display = QTextEdit()
        self.main_window.status_display.setMaximumHeight(150)
        self.main_window.status_display.setStyleSheet("""
            QTextEdit {
                background-color: #2B2D31;
                border: 1px solid #1E1F22;
                border-radius: 5px;
                color: #DCDFE4;
                padding: 10px;
                font-family: Consolas, monospace;
            }
        """)
        self.main_window.status_display.setReadOnly(True)
        progress_layout.addWidget(self.main_window.status_display)
        
        layout.addWidget(progress_group)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.main_window.start_btn = self.create_button("🚀 Start Cloning")
        self.main_window.start_btn.clicked.connect(self.main_window.start_cloning)
        button_layout.addWidget(self.main_window.start_btn)
        
        self.main_window.stop_btn = self.create_button("🛑 Stop")
        self.main_window.stop_btn.clicked.connect(self.main_window.stop_cloning)
        self.main_window.stop_btn.setEnabled(False)
        button_layout.addWidget(self.main_window.stop_btn)
        
        clear_btn = self.create_button("🗑️ Clear Log")
        clear_btn.clicked.connect(lambda: self.main_window.status_display.clear())
        button_layout.addWidget(clear_btn)
        
        layout.addLayout(button_layout)
        layout.addStretch()
    
    def get_groupbox_style(self):
        return """
            QGroupBox {
                color: #ffffff;
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #1E1F22;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """
    
    def setup_input_style(self, widget):
        widget.setStyleSheet("""
            QLineEdit {
                background-color: #383A40;
                border: 2px solid #1E1F22;
                border-radius: 5px;
                padding: 8px 12px;
                color: #ffffff;
                font-size: 13px;
                selection-background-color: #5865F2;
            }
            QLineEdit:focus {
                border-color: #5865F2;
            }
            QLineEdit::placeholder {
                color: #6D6F78;
            }
        """)
    
    def create_button(self, text):
        btn = QPushButton(text)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #5865F2;
                color: white;
                border: none;
                padding: 10px 15px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
                margin: 2px;
            }
            QPushButton:hover {
                background-color: #4752C4;
            }
            QPushButton:pressed {
                background-color: #3C45A5;
            }
            QPushButton:disabled {
                background-color: #4E5058;
                color: #6D6F78;
            }
        """)
        return btn

class SettingsTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        settings_group = QGroupBox("Cloning Options")
        settings_group.setStyleSheet("""
            QGroupBox {
                color: #ffffff;
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #1E1F22;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        settings_layout = QVBoxLayout(settings_group)
        
        # Clone options
        self.main_window.settings_checks = {
            'guild_edit': QCheckBox("Clone server icon and name"),
            'channels_delete': QCheckBox("Delete existing channels"),
            'roles_delete': QCheckBox("Delete existing roles"),
            'roles_create': QCheckBox("Clone roles"),
            'categories_create': QCheckBox("Clone categories"),
            'channels_create': QCheckBox("Clone channels"),
            'emojis_create': QCheckBox("Clone emojis")
        }
        
        for key, check in self.main_window.settings_checks.items():
            check.setChecked(DEFAULT_PREFERENCES.get(key, False))
            check.setStyleSheet("""
                QCheckBox {
                    color: #ADAFB4;
                    padding: 8px;
                    font-size: 13px;
                }
                QCheckBox::indicator {
                    width: 16px;
                    height: 16px;
                }
                QCheckBox::indicator:unchecked {
                    border: 2px solid #6D6F78;
                    border-radius: 3px;
                    background-color: #2B2D31;
                }
                QCheckBox::indicator:checked {
                    border: 2px solid #5865F2;
                    border-radius: 3px;
                    background-color: #5865F2;
                }
                QCheckBox::indicator:hover {
                    border: 2px solid #4752C4;
                }
            """)
            settings_layout.addWidget(check)
        
        layout.addWidget(settings_group)
        layout.addStretch()

class DocumentationTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        doc_text = QTextEdit()
        doc_text.setReadOnly(True)
        doc_text.setStyleSheet("""
            QTextEdit {
                background-color: #2B2D31;
                border: 1px solid #1E1F22;
                border-radius: 8px;
                color: #DCDFE4;
                padding: 15px;
                font-size: 13px;
                line-height: 1.5;
            }
        """)
        
        documentation = f"""
        <h2 style="color: #5865F2;">Rock V2 - Discord Server Cloner</h2>
        
        <h3 style="color: #57F287;">Features:</h3>
        <ul>
        <li>Clone server roles with permissions</li>
        <li>Clone categories and channel structure</li>
        <li>Clone text and voice channels</li>
        <li>Clone emojis (optional)</li>
        <li>Copy server icon and name</li>
        <li>Clean destination server before cloning</li>
        </ul>
        
        <h3 style="color: #57F287;">Instructions:</h3>
        <ol>
        <li>Get a Discord User token</a></li>
        <li>Join the User to both source and destination servers with necessary permissions</li>
        <li>Make sure to give proper role and permisson to the account</li>
        <li>Get the server IDs (right-click on server icon → Copy ID)</li>
        <li>Configure cloning options in Settings tab</li>
        <li>Start cloning!</li>
        </ol>
        
        <h3 style="color: #57F287;">Required Permissions:</h3>
        <ul>
        <li>Manage Roles</li>
        <li>Manage Channels</li>
        <li>Manage Server</li>
        <li>View Channels</li>
        <li>Read Message History</li>
        <li>Manage Emojis and Stickers</li>
        </ul>
        
        <p style="color: #FEE75C;">Need help? Join our support server: <a href="{SUPPORT_LINK}" style="color: #5865F2;">{SUPPORT_LINK}</a></p>
        """
        
        doc_text.setHtml(documentation)
        layout.addWidget(doc_text)

class TipsTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        tips_text = QTextEdit()
        tips_text.setReadOnly(True)
        tips_text.setStyleSheet("""
            QTextEdit {
                background-color: #2B2D31;
                border: 1px solid #1E1F22;
                border-radius: 8px;
                color: #DCDFE4;
                padding: 15px;
                font-size: 13px;
                line-height: 1.5;
            }
        """)
        
        tips = """
        <h2 style="color: #5865F2;">Tips & Shortcuts</h2>
        
        <h3 style="color: #57F287;">Best Practices:</h3>
        <ul>
        <li><strong>Backup First:</strong> Always backup your destination server before cloning</li>
        <li><strong>Test Server:</strong> Use a test server first to verify the cloning process</li>
        <li><strong>Bot Position:</strong> Make sure the bot role is higher than the roles it's trying to manage</li>
        <li><strong>Rate Limits:</strong> Large servers may take time due to Discord rate limits</li>
        </ul>
        
        <h3 style="color: #57F287;">Troubleshooting:</h3>
        <ul>
        <li><strong>Invalid Token:</strong> Ensure the token is correct and the bot is properly configured</li>
        <li><strong>Permission Errors:</strong> Check bot permissions in both servers</li>
        <li><strong>Server ID Issues:</strong> Verify you're using correct server IDs</li>
        <li><strong>Rate Limiting:</strong> If cloning fails, wait a few minutes and try again</li>
        </ul>
        
        <h3 style="color: #57F287;">Keyboard Shortcuts:</h3>
        <ul>
        <li><strong>Ctrl+Q:</strong> Quit application</li>
        <li><strong>Ctrl+R:</strong> Restart cloning process</li>
        <li><strong>Ctrl+L:</strong> Clear log</li>
        <li><strong>Ctrl+D:</strong> Show documentation</li>
        </ul>
        
        <p style="color: #FEE75C;">Remember: Use this tool responsibly and in accordance with Discord's Terms of Service.</p>
        """
        
        tips_text.setHtml(tips)
        layout.addWidget(tips_text)

class CreditsTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.network_manager = QNetworkAccessManager(self)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("ROCK V2")
        title.setStyleSheet("""
            QLabel {
                color: #5865F2;
                font-size: 36px;
                font-weight: 600;
                font-family: 'Arial', sans-serif;
            }
        """)
        layout.addWidget(title)
        
        subtitle = QLabel("Discord Server Cloner")
        subtitle.setStyleSheet("""
            QLabel {
                color: #57F287;
                font-size: 24px;
                font-weight: 500;
                font-family: 'Arial', sans-serif;
            }
        """)
        layout.addWidget(subtitle)
        
        # Creator (Dev Bhakat)
        creator_layout = QHBoxLayout()
        self.creator_image = QLabel()
        self.creator_image.setFixedSize(120, 120)
        self.creator_image.setStyleSheet("border-radius: 60px;")
        self.load_image("https://avatars.githubusercontent.com/u/114628634?v=4", self.creator_image)
        
        creator_info = QLabel("""
            <div>
                <strong>Creator:</strong> Dev Bhakat (devrock07)<br>
                <a href="https://github.com/devrock07" style="color: #5865F2; text-decoration: none;">github.com/devrock07</a>
            </div>
        """)
        creator_info.setStyleSheet("""
            QLabel {
                color: #DCDFE4;
                font-size: 14px;
            }
        """)
        creator_info.setOpenExternalLinks(True)
        
        creator_layout.addWidget(self.creator_image)
        creator_layout.addWidget(creator_info)
        creator_layout.addStretch()
        layout.addLayout(creator_layout)
        
        # Logo Designer (Asnehita Das)
        designer_layout = QHBoxLayout()
        self.designer_image = QLabel()
        self.designer_image.setFixedSize(120, 120)
        self.designer_image.setStyleSheet("border-radius: 60px;")
        self.load_image("https://avatars.githubusercontent.com/u/233407598?v=4", self.designer_image)
        
        designer_info = QLabel("""
            <div>
                <strong>Logo Designer:</strong> Asnehita Das (kiki Asnehita)<br>
                <a href="https://github.com/asnehitadas-71" style="color: #5865F2; text-decoration: none;">github.com/asnehitadas-71</a>
            </div>
        """)
        designer_info.setStyleSheet("""
            QLabel {
                color: #DCDFE4;
                font-size: 14px;
            }
        """)
        designer_info.setOpenExternalLinks(True)
        
        designer_layout.addWidget(self.designer_image)
        designer_layout.addWidget(designer_info)
        designer_layout.addStretch()
        layout.addLayout(designer_layout)
        
        # Support Server
        support_group = QFrame()
        support_group.setStyleSheet("""
            QFrame {
                background-color: #313338;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        support_layout = QVBoxLayout(support_group)
        
        support_label = QLabel("<strong>Support Server:</strong>")
        support_label.setStyleSheet("color: #DCDFE4; font-size: 14px;")
        support_layout.addWidget(support_label)
        
        support_link = QLabel(f'<a href="{SUPPORT_LINK}" style="color: #5865F2; text-decoration: none;">{SUPPORT_LINK}</a>')
        support_link.setStyleSheet("font-size: 14px;")
        support_link.setOpenExternalLinks(True)
        support_layout.addWidget(support_link)
        
        layout.addWidget(support_group)
        
        layout.addStretch()
    
    def load_image(self, url, label):
        """Load image from URL and set it to the given QLabel"""
        request = QNetworkRequest(QUrl(url))
        reply = self.network_manager.get(request)
        reply.finished.connect(lambda: self.set_image(reply, label))
    
    def set_image(self, reply, label):
        """Set the downloaded image to the QLabel"""
        if reply.error() == QNetworkReply.NetworkError.NoError:
            data = reply.readAll()
            image = QImage()
            if image.loadFromData(data):
                pixmap = QPixmap(image).scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                label.setPixmap(pixmap)
            else:
                label.setText("Load Failed")
        else:
            label.setText("Load Failed")