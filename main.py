import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from ui.main_window import DiscordClonerGUI
from utils.constants import APP_NAME, APP_VERSION

def main():
    # Create QApplication
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)

    # ✅ Set taskbar icon (root directory)
    icon_path = os.path.join(current_dir, "icon.png")  # or .ico
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    # Create and show main window
    window = DiscordClonerGUI()
    window.show()

    # Run application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
