"""
GUI Interface for Jarvis - Modern animated interface
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTextEdit, QLineEdit, QLabel, QFrame)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtSignal, QThread, QRect, QPoint
from PyQt5.QtGui import QFont, QPalette, QColor, QPainter, QLinearGradient, QBrush, QPen
import math
import random

class VoiceVisualizerWidget(QWidget):
    """Animated voice visualizer widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(300, 300)
        self.is_listening = False
        self.is_speaking = False
        self.bars = []
        self.angle = 0
        
        # Initialize bars for circular visualizer
        num_bars = 36
        for i in range(num_bars):
            self.bars.append({
                'height': 0.2,
                'target': 0.2,
                'angle': i * (360 / num_bars)
            })
        
        # Animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(50)  # 20 FPS
    
    def paintEvent(self, event):
        """Draw the visualizer"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Background
        painter.fillRect(self.rect(), QColor(15, 15, 35))
        
        # Center point
        center_x = self.width() // 2
        center_y = self.height() // 2
        radius = 80
        
        # Draw outer circle
        painter.setPen(QPen(QColor(0, 150, 255, 100), 2))
        painter.drawEllipse(center_x - radius, center_y - radius, radius * 2, radius * 2)
        
        # Draw inner circle (core)
        core_color = QColor(0, 180, 255) if self.is_listening or self.is_speaking else QColor(100, 100, 150)
        painter.setBrush(QBrush(core_color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(center_x - 30, center_y - 30, 60, 60)
        
        # Draw bars
        if self.is_listening or self.is_speaking:
            for bar in self.bars:
                angle_rad = math.radians(bar['angle'] + self.angle)
                
                # Calculate bar position
                start_x = center_x + math.cos(angle_rad) * radius
                start_y = center_y + math.sin(angle_rad) * radius
                
                # Bar height based on activity
                bar_length = radius * bar['height']
                end_x = center_x + math.cos(angle_rad) * (radius + bar_length)
                end_y = center_y + math.sin(angle_rad) * (radius + bar_length)
                
                # Color gradient
                color = QColor(0, 150, 255, 200) if self.is_listening else QColor(0, 255, 150, 200)
                painter.setPen(QPen(color, 3))
                painter.drawLine(int(start_x), int(start_y), int(end_x), int(end_y))
        
        painter.end()
    
    def update_animation(self):
        """Update animation frame"""
        if self.is_listening or self.is_speaking:
            self.angle = (self.angle + 2) % 360
            
            # Update bar heights
            for bar in self.bars:
                # Random target for wave effect
                if random.random() < 0.1:
                    bar['target'] = random.uniform(0.3, 1.0)
                
                # Smooth transition
                bar['height'] += (bar['target'] - bar['height']) * 0.2
        else:
            # Reset to idle state
            for bar in self.bars:
                bar['height'] += (0.2 - bar['height']) * 0.1
        
        self.update()
    
    def set_listening(self, listening):
        """Set listening state"""
        self.is_listening = listening
    
    def set_speaking(self, speaking):
        """Set speaking state"""
        self.is_speaking = speaking


class ListeningThread(QThread):
    """Thread for voice listening"""
    result = pyqtSignal(str)
    
    def __init__(self, voice_handler):
        super().__init__()
        self.voice_handler = voice_handler
    
    def run(self):
        success, text = self.voice_handler.listen(timeout=5, phrase_time_limit=10)
        if success:
            self.result.emit(text)
        else:
            self.result.emit("")


class JarvisGUI(QMainWindow):
    """Main GUI window for Jarvis"""
    
    def __init__(self, jarvis_engine, voice_handler):
        super().__init__()
        self.jarvis_engine = jarvis_engine
        self.voice_handler = voice_handler
        self.listening_thread = None
        
        self.init_ui()
        
        # Show greeting
        greeting = self.jarvis_engine.get_greeting()
        self.add_message("Jarvis", greeting)
        self.voice_handler.speak_async(greeting)
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("JARVIS - Personal Assistant")
        self.setGeometry(100, 100, 900, 700)
        
        # Set dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0f0f23;
            }
            QTextEdit {
                background-color: #1a1a2e;
                color: #00d4ff;
                border: 2px solid #0096c7;
                border-radius: 10px;
                padding: 10px;
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
            QPushButton:pressed {
                background-color: #0077b6;
            }
            QLabel {
                color: #00d4ff;
                font-size: 14px;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("J.A.R.V.I.S")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #00d4ff; margin: 10px;")
        main_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Just A Rather Very Intelligent System")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("font-size: 12px; color: #0096c7; margin-bottom: 10px;")
        main_layout.addWidget(subtitle_label)
        
        # Voice visualizer
        self.visualizer = VoiceVisualizerWidget()
        visualizer_container = QWidget()
        visualizer_layout = QHBoxLayout(visualizer_container)
        visualizer_layout.addStretch()
        visualizer_layout.addWidget(self.visualizer)
        visualizer_layout.addStretch()
        main_layout.addWidget(visualizer_container)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 14px; color: #00ff00;")
        main_layout.addWidget(self.status_label)
        
        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setMinimumHeight(200)
        main_layout.addWidget(self.chat_display)
        
        # Input area
        input_layout = QHBoxLayout()
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your message here...")
        self.input_field.returnPressed.connect(self.send_text_message)
        input_layout.addWidget(self.input_field)
        
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_text_message)
        input_layout.addWidget(self.send_button)
        
        main_layout.addLayout(input_layout)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.voice_button = QPushButton("🎤 Voice Input")
        self.voice_button.clicked.connect(self.start_voice_input)
        button_layout.addWidget(self.voice_button)
        
        self.clear_button = QPushButton("Clear Chat")
        self.clear_button.clicked.connect(self.clear_chat)
        button_layout.addWidget(self.clear_button)
        
        self.settings_button = QPushButton("⚙ Settings")
        self.settings_button.clicked.connect(self.show_settings)
        button_layout.addWidget(self.settings_button)
        
        main_layout.addLayout(button_layout)
    
    def add_message(self, sender, message):
        """Add message to chat display"""
        color = "#00d4ff" if sender == "Jarvis" else "#ffffff"
        self.chat_display.append(f'<span style="color: {color}; font-weight: bold;">{sender}:</span> {message}<br>')
    
    def send_text_message(self):
        """Send text message"""
        text = self.input_field.text().strip()
        if not text:
            return
        
        self.input_field.clear()
        self.add_message("You", text)
        
        # Process command
        self.status_label.setText("Processing...")
        response = self.jarvis_engine.process_command(text)
        
        self.add_message("Jarvis", response)
        self.voice_handler.speak_async(response)
        self.status_label.setText("Ready")
    
    def start_voice_input(self):
        """Start voice input"""
        if self.listening_thread and self.listening_thread.isRunning():
            return
        
        self.status_label.setText("Listening...")
        self.voice_button.setEnabled(False)
        self.visualizer.set_listening(True)
        
        # Start listening in thread
        self.listening_thread = ListeningThread(self.voice_handler)
        self.listening_thread.result.connect(self.handle_voice_result)
        self.listening_thread.finished.connect(self.voice_input_finished)
        self.listening_thread.start()
    
    def handle_voice_result(self, text):
        """Handle voice recognition result"""
        if text:
            self.add_message("You", text)
            
            # Process command
            self.status_label.setText("Processing...")
            response = self.jarvis_engine.process_command(text)
            
            self.add_message("Jarvis", response)
            self.visualizer.set_speaking(True)
            self.voice_handler.speak(response)
            self.visualizer.set_speaking(False)
        else:
            self.add_message("Jarvis", "I didn't catch that. Please try again.")
    
    def voice_input_finished(self):
        """Called when voice input finishes"""
        self.voice_button.setEnabled(True)
        self.visualizer.set_listening(False)
        self.status_label.setText("Ready")
    
    def clear_chat(self):
        """Clear chat display"""
        self.chat_display.clear()
        self.jarvis_engine.clear_history()
        self.add_message("Jarvis", "Chat cleared. How can I help you?")
    
    def show_settings(self):
        """Show settings dialog"""
        from PyQt5.QtWidgets import QDialog, QFormLayout, QSpinBox, QDoubleSpinBox, QDialogButtonBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Settings")
        dialog.setModal(True)
        
        layout = QFormLayout(dialog)
        
        # Voice rate
        rate_spin = QSpinBox()
        rate_spin.setRange(50, 300)
        rate_spin.setValue(self.voice_handler.config.voice_rate)
        layout.addRow("Voice Rate:", rate_spin)
        
        # Voice volume
        volume_spin = QDoubleSpinBox()
        volume_spin.setRange(0.0, 1.0)
        volume_spin.setSingleStep(0.1)
        volume_spin.setValue(self.voice_handler.config.voice_volume)
        layout.addRow("Voice Volume:", volume_spin)
        
        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
        
        if dialog.exec_() == QDialog.Accepted:
            self.voice_handler.set_voice_rate(rate_spin.value())
            self.voice_handler.set_voice_volume(volume_spin.value())
            self.voice_handler.config.save_config()
    
    def closeEvent(self, event):
        """Handle window close"""
        self.voice_handler.stop_speaking()
        event.accept()
