import os
import time
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QTabWidget, QFrame, QMessageBox, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QUrl, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

# Use absolute imports
from ui.sidebar import Sidebar
from ui.tabs import CloningTab, SettingsTab, DocumentationTab, TipsTab, CreditsTab  # Updated import
from utils.constants import APP_NAME, ICON_PATH
from core.clone_worker import CloneWorker

class DiscordClonerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.clone_worker = None
        self.setup_players()
        self.setup_ui()
        self.apply_discord_theme()
        self.set_window_icon()
        if self.loading_player.source().isValid():
            self.loading_player.play()  # Play loading sound on app start
        else:
            print("Warning: Could not play loading.mp3 - file not found or invalid.")
        
    def setup_players(self):
        # Get absolute path to resource directory
        base_path = os.path.dirname(os.path.abspath(__file__))
        resource_path = os.path.join(base_path, "resource")

        # Initialize loading player
        self.loading_player = QMediaPlayer(self)
        self.loading_output = QAudioOutput(self)
        self.loading_player.setAudioOutput(self.loading_output)
        loading_file = os.path.join(resource_path, "loading.mp3")
        if os.path.exists(loading_file):
            self.loading_player.setSource(QUrl.fromLocalFile(loading_file))
            print(f"Loaded loading.mp3 from: {loading_file}")
        else:
            print(f"Error: loading.mp3 not found at {loading_file}")

        # Initialize cloning player with looping
        self.cloning_player = QMediaPlayer(self)
        self.cloning_output = QAudioOutput(self)
        self.cloning_player.setAudioOutput(self.cloning_output)
        cloning_file = os.path.join(resource_path, "cloning.mp3")
        if os.path.exists(cloning_file):
            self.cloning_player.setSource(QUrl.fromLocalFile(cloning_file))
            self.cloning_player.setLoops(QMediaPlayer.Loops.Infinite)  # Set to loop indefinitely
            print(f"Loaded cloning.mp3 from: {cloning_file}")
        else:
            print(f"Error: cloning.mp3 not found at {cloning_file}")

        # Initialize done player
        self.done_player = QMediaPlayer(self)
        self.done_output = QAudioOutput(self)
        self.done_player.setAudioOutput(self.done_output)
        done_file = os.path.join(resource_path, "done.mp3")
        if os.path.exists(done_file):
            self.done_player.setSource(QUrl.fromLocalFile(done_file))
            print(f"Loaded done.mp3 from: {done_file}")
        else:
            print(f"Error: done.mp3 not found at {done_file}")
        
    def setup_ui(self):
        self.setWindowTitle(APP_NAME)
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(1000, 700)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Left sidebar
        self.sidebar = Sidebar(self)
        main_layout.addWidget(self.sidebar)
        
        # Add shadow to sidebar
        sidebar_shadow = QGraphicsDropShadowEffect()
        sidebar_shadow.setBlurRadius(15)
        sidebar_shadow.setXOffset(2)
        sidebar_shadow.setYOffset(0)
        sidebar_shadow.setColor(QColor(0, 0, 0, 120))
        self.sidebar.setGraphicsEffect(sidebar_shadow)
        
        # Right content area
        self.setup_content_area(main_layout)
    
    def setup_content_area(self, main_layout):
        content_frame = QFrame()
        content_frame.setObjectName("content")
        
        # Add shadow to content
        content_shadow = QGraphicsDropShadowEffect()
        content_shadow.setBlurRadius(20)
        content_shadow.setXOffset(0)
        content_shadow.setYOffset(0)
        content_shadow.setColor(QColor(0, 0, 0, 80))
        content_frame.setGraphicsEffect(content_shadow)
        
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)
        
        # Title with animation
        self.title = QLabel("Discord Server Cloner")
        self.title.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 30px;
                font-weight: 600;
                padding: 12px 0;
                font-family: 'Arial', sans-serif;
            }
        """)
        # Add fade-in animation for title
        self.title_animation = QPropertyAnimation(self.title, b"windowOpacity")
        self.title_animation.setDuration(1000)
        self.title_animation.setStartValue(0.0)
        self.title_animation.setEndValue(1.0)
        self.title_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.title_animation.start()
        content_layout.addWidget(self.title)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #1E1F22;
                border-radius: 8px;
                background-color: #2B2D31;
            }
            QTabBar::tab {
                background-color: #313338;
                color: #ADAFB4;
                padding: 12px 24px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                margin-right: 4px;
                font-weight: 500;
            }
            QTabBar::tab:selected {
                background-color: #2B2D31;
                color: #ffffff;
                border-bottom: 3px solid #5865F2;
            }
            QTabBar::tab:hover:!selected {
                background-color: #383A40;
                color: #ffffff;
            }
        """)
        
        # Setup tabs
        self.cloning_tab = CloningTab(self)
        self.settings_tab = SettingsTab(self)
        self.documentation_tab = DocumentationTab(self)
        self.tips_tab = TipsTab(self)
        self.credits_tab = CreditsTab(self)  # Updated from about_tab
        
        self.tab_widget.addTab(self.cloning_tab, "🚀 Cloning")
        self.tab_widget.addTab(self.settings_tab, "⚙️ Settings")
        self.tab_widget.addTab(self.documentation_tab, "📚 Documentation")
        self.tab_widget.addTab(self.tips_tab, "💡 Tips & Help")
        self.tab_widget.addTab(self.credits_tab, "🔧 Credits")  # Updated from About
        
        content_layout.addWidget(self.tab_widget)
        main_layout.addWidget(content_frame)
    
    def set_window_icon(self):
        """Set window icon from file"""
        icon_files = [
            "icon.ico", "icon.png", "logo.ico", "logo.png",
            "rock_icon.ico", "rock_icon.png"
        ]
        
        for icon_file in icon_files:
            if os.path.exists(icon_file):
                self.setWindowIcon(QIcon(icon_file))
                print(f"Loaded icon: {icon_file}")
                break
        else:
            print("No icon file found. Using default icon.")
    
    def apply_discord_theme(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1E1F22;
                font-family: 'Arial', sans-serif;
            }
            QWidget#sidebar {
                background-color: #232428;
                border-right: 1px solid #1A1B1E;
            }
            QWidget#content {
                background-color: #2B2D31;
            }
        """)
    
    def show_cloning_tab(self):
        self.tab_widget.setCurrentIndex(0)
    
    def show_settings_tab(self):
        self.tab_widget.setCurrentIndex(1)
    
    def show_documentation_tab(self):
        self.tab_widget.setCurrentIndex(2)
    
    def show_tips_tab(self):
        self.tab_widget.setCurrentIndex(3)
    
    def show_credits_tab(self):  # Updated from show_about_tab
        self.tab_widget.setCurrentIndex(4)
    
    def log_message(self, message):
        timestamp = time.strftime("%H:%M:%S")
        self.status_display.append(f"[{timestamp}] {message}")
        scrollbar = self.status_display.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def start_cloning(self):
        # Stop all players before starting new cloning
        self.loading_player.stop()
        self.cloning_player.stop()
        self.done_player.stop()
        
        # Validate inputs
        token = self.token_input.text().strip()
        source_id = self.source_input.text().strip()
        dest_id = self.dest_input.text().strip()
        
        if not token:
            QMessageBox.warning(self, "Input Error", "Please enter a bot token!")
            return
        
        if not source_id or not dest_id:
            QMessageBox.warning(self, "Input Error", "Please enter both server IDs!")
            return
        
        if not source_id.isnumeric() or not dest_id.isnumeric():
            QMessageBox.warning(self, "Input Error", "Server IDs must be numeric!")
            return
        
        # Get preferences
        preferences = {}
        for key, check in self.settings_checks.items():
            preferences[key] = check.isChecked()
        
        if not any(preferences.values()):
            QMessageBox.warning(self, "Settings Error", "Please select at least one cloning option!")
            return
        
        # Start cloning worker
        self.clone_worker = CloneWorker(token, source_id, dest_id, preferences)
        self.clone_worker.update_signal.connect(self.log_message)
        self.clone_worker.progress_signal.connect(self.progress_bar.setValue)
        self.clone_worker.finished_signal.connect(self.cloning_finished)
        
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.progress_bar.setValue(0)
        self.status_display.clear()
        
        self.log_message("Starting cloning process...")
        if self.cloning_player.source().isValid():
            self.cloning_player.play()  # Play cloning sound in loop
        else:
            print("Warning: Could not play cloning.mp3 - file not found or invalid.")
        self.status_text.setText("Cloning in progress...")
        self.status_text.setStyleSheet("color: #FEE75C;")
        
        self.clone_worker.start()
    
    def stop_cloning(self):
        if self.clone_worker and self.clone_worker.isRunning():
            self.clone_worker.terminate()
            self.clone_worker.wait()
            self.log_message("Cloning process stopped by user!")
            # Stop all players when cloning is stopped
            self.loading_player.stop()
            self.cloning_player.stop()
            self.done_player.stop()
            self.cloning_finished(False, "Process stopped by user")
    
    def cloning_finished(self, success, message):
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        # Stop all players
        self.loading_player.stop()
        self.cloning_player.stop()
        self.done_player.stop()
        
        if success:
            self.log_message("✅ " + message)
            self.status_text.setText("Cloning completed!")
            self.status_text.setStyleSheet("color: #57F287;")
            if self.done_player.source().isValid():
                self.done_player.play()  # Play done sound on success
            else:
                print("Warning: Could not play done.mp3 - file not found or invalid.")
            QMessageBox.information(self, "Success", "Server cloned successfully!")
        else:
            self.log_message("❌ " + message)
            self.status_text.setText("Cloning failed!")
            self.status_text.setStyleSheet("color: #ED4245;")
            QMessageBox.critical(self, "Error", f"Cloning failed:\n{message}")