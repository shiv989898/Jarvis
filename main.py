"""
JARVIS - Just A Rather Very Intelligent System
Main application entry point
"""
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

from config import Config
from system_controller import SystemController
from voice_handler import VoiceHandler
from jarvis_engine import JarvisEngine
from gui_interface import JarvisGUI


class APIKeyDialog(QDialog):
    """Dialog for entering API key"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("JARVIS - API Key Required")
        self.setModal(True)
        self.setFixedWidth(500)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #0f0f23;
            }
            QLabel {
                color: #00d4ff;
                font-size: 13px;
            }
            QLineEdit {
                background-color: #1a1a2e;
                color: #ffffff;
                border: 2px solid #0096c7;
                border-radius: 5px;
                padding: 8px;
                font-size: 13px;
            }
            QPushButton {
                background-color: #0096c7;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00b4d8;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Welcome to JARVIS")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #00d4ff;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Instructions
        instructions = QLabel(
            "Please enter your Google Gemini API key to continue.\n\n"
            "You can get your API key from:\n"
            "https://makersuite.google.com/app/apikey"
        )
        instructions.setWordWrap(True)
        instructions.setAlignment(Qt.AlignCenter)
        layout.addWidget(instructions)
        
        # API key input
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("Enter your Gemini API key here...")
        self.api_key_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.api_key_input)
        
        # Show/Hide button
        self.toggle_button = QPushButton("Show API Key")
        self.toggle_button.clicked.connect(self.toggle_visibility)
        layout.addWidget(self.toggle_button)
        
        # Submit button
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.validate_and_accept)
        layout.addWidget(submit_button)
        
        # Skip button (for testing)
        skip_button = QPushButton("Skip (Not Recommended)")
        skip_button.clicked.connect(self.reject)
        skip_button.setStyleSheet("""
            QPushButton {
                background-color: #666;
            }
            QPushButton:hover {
                background-color: #888;
            }
        """)
        layout.addWidget(skip_button)
    
    def toggle_visibility(self):
        """Toggle API key visibility"""
        if self.api_key_input.echoMode() == QLineEdit.Password:
            self.api_key_input.setEchoMode(QLineEdit.Normal)
            self.toggle_button.setText("Hide API Key")
        else:
            self.api_key_input.setEchoMode(QLineEdit.Password)
            self.toggle_button.setText("Show API Key")
    
    def validate_and_accept(self):
        """Validate API key and accept"""
        api_key = self.api_key_input.text().strip()
        if not api_key:
            QMessageBox.warning(self, "Error", "Please enter an API key!")
            return
        
        if len(api_key) < 20:
            QMessageBox.warning(self, "Error", "API key seems too short. Please check and try again.")
            return
        
        self.accept()
    
    def get_api_key(self):
        """Get the entered API key"""
        return self.api_key_input.text().strip()


def main():
    """Main application entry point"""
    print("=" * 50)
    print("JARVIS - Just A Rather Very Intelligent System")
    print("=" * 50)
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("JARVIS")
    
    # Load configuration
    config = Config()
    
    # Check for API key
    if not config.get_api_key():
        print("\nAPI key not found. Requesting from user...")
        dialog = APIKeyDialog()
        if dialog.exec_() == QDialog.Accepted:
            api_key = dialog.get_api_key()
            config.set_api_key(api_key)
            print("API key saved successfully!")
        else:
            print("Warning: Running without API key. Limited functionality available.")
    else:
        print("API key found in configuration.")
    
    try:
        # Initialize components
        print("\nInitializing components...")
        
        print("  ✓ Loading configuration")
        
        print("  ✓ Initializing system controller")
        system_controller = SystemController()
        
        print("  ✓ Initializing voice handler")
        voice_handler = VoiceHandler(config)
        
        print("  ✓ Initializing Jarvis engine")
        jarvis_engine = JarvisEngine(config, system_controller)
        
        print("  ✓ Creating GUI interface")
        window = JarvisGUI(jarvis_engine, voice_handler)
        
        print("\n✓ JARVIS initialized successfully!")
        print("=" * 50)
        
        # Show window
        window.show()
        
        # Run application
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"\n✗ Error initializing JARVIS: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Show error dialog
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("JARVIS Error")
        error_dialog.setText("Failed to initialize JARVIS")
        error_dialog.setDetailedText(str(e))
        error_dialog.exec_()
        
        sys.exit(1)


if __name__ == "__main__":
    main()
