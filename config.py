"""
Configuration file for Jarvis Personal Assistant
"""
import os
import json

class Config:
    """Configuration manager for Jarvis"""
    
    CONFIG_FILE = "jarvis_config.json"
    
    def __init__(self):
        self.api_key = None
        self.voice_enabled = True
        self.voice_rate = 150
        self.voice_volume = 0.9
        self.wake_word = "jarvis"
        self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, 'r') as f:
                    config_data = json.load(f)
                    self.api_key = config_data.get('api_key')
                    self.voice_enabled = config_data.get('voice_enabled', True)
                    self.voice_rate = config_data.get('voice_rate', 150)
                    self.voice_volume = config_data.get('voice_volume', 0.9)
                    self.wake_word = config_data.get('wake_word', 'jarvis')
            except Exception as e:
                print(f"Error loading config: {e}")
    
    def save_config(self):
        """Save configuration to file"""
        try:
            config_data = {
                'api_key': self.api_key,
                'voice_enabled': self.voice_enabled,
                'voice_rate': self.voice_rate,
                'voice_volume': self.voice_volume,
                'wake_word': self.wake_word
            }
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(config_data, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def set_api_key(self, api_key):
        """Set and save API key"""
        self.api_key = api_key
        self.save_config()
    
    def get_api_key(self):
        """Get API key"""
        return self.api_key
