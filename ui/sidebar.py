from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

# Use absolute imports
from utils.constants import DEFAULT_PREFERENCES


class Sidebar(QFrame):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
    
    def setup_ui(self):
        self.setFixedWidth(240)
        self.setObjectName("sidebar")
        
        sidebar_layout = QVBoxLayout(self)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_layout.setSpacing(10)
        
        # Logo
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo_pixmap = QPixmap("ROCK_CLONER.png")  # Path to your logo
        if logo_pixmap.isNull():
            logo_label.setText("ROCK CLONER V2")
            logo_label.setStyleSheet("""
                QLabel {
                    color: #ffffff;
                    font-size: 22px;
                    font-weight: bold;
                    margin: 10px;
                }
            """)
        else:
            # Make the logo big and smooth
            logo_label.setPixmap(
                logo_pixmap.scaled(
                    200, 80,  # Adjusted for horizontal logo
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            )
            logo_label.setStyleSheet("""
                QLabel {
                    background-color: transparent;
                    margin: 10px;
                }
            """)

        sidebar_layout.addWidget(logo_label)
        
        # Navigation buttons
        nav_buttons = [
            ("🚀 Start Cloning", self.main_window.show_cloning_tab),
            ("⚙️ Settings", self.main_window.show_settings_tab),
            ("📚 Documentation", self.main_window.show_documentation_tab),
            ("💡 Tips & Help", self.main_window.show_tips_tab),
            ("🔧 Credits", self.main_window.show_credits_tab)
        ]
        
        for text, slot in nav_buttons:
            btn = self.create_button(text)
            btn.clicked.connect(slot)
            sidebar_layout.addWidget(btn)
        
        sidebar_layout.addStretch()
        
        # Status
        status_frame = QFrame()
        status_frame.setStyleSheet("""
            QFrame {
                background-color: #2B2D31;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        status_layout = QVBoxLayout(status_frame)
        
        status_label = QLabel("System Status")
        status_label.setStyleSheet("color: #ADAFB4; font-weight: bold;")
        status_layout.addWidget(status_label)
        
        self.main_window.status_text = QLabel("Ready")
        self.main_window.status_text.setStyleSheet("color: #57F287;")
        status_layout.addWidget(self.main_window.status_text)
        
        sidebar_layout.addWidget(status_frame)
    
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
