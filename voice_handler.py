"""
Voice Handler - Speech recognition and text-to-speech
"""
import speech_recognition as sr
import pyttsx3
import threading
import queue

class VoiceHandler:
    """Handles voice input and output"""
    
    def __init__(self, config):
        self.config = config
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech engine
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', config.voice_rate)
        self.tts_engine.setProperty('volume', config.voice_volume)
        
        # Try to set a better voice
        voices = self.tts_engine.getProperty('voices')
        if len(voices) > 1:
            self.tts_engine.setProperty('voice', voices[1].id)  # Usually female voice
        
        # Queue for thread-safe speech
        self.speech_queue = queue.Queue()
        self.speech_thread = None
        self.is_speaking = False
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
    
    def speak(self, text):
        """Convert text to speech"""
        if not self.config.voice_enabled:
            return
        
        try:
            self.is_speaking = True
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            self.is_speaking = False
        except Exception as e:
            print(f"TTS Error: {e}")
            self.is_speaking = False
    
    def speak_async(self, text):
        """Speak text asynchronously"""
        if not self.config.voice_enabled:
            return
        
        thread = threading.Thread(target=self.speak, args=(text,))
        thread.daemon = True
        thread.start()
    
    def listen(self, timeout=5, phrase_time_limit=10):
        """Listen for voice input"""
        try:
            with self.microphone as source:
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            
            print("Recognizing...")
            text = self.recognizer.recognize_google(audio)
            return True, text
            
        except sr.WaitTimeoutError:
            return False, "Listening timeout"
        except sr.UnknownValueError:
            return False, "Could not understand audio"
        except sr.RequestError as e:
            return False, f"Could not request results; {e}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def listen_in_background(self, callback):
        """Listen for voice input in background"""
        def background_listener():
            while True:
                try:
                    with self.microphone as source:
                        audio = self.recognizer.listen(source, timeout=None, phrase_time_limit=10)
                    
                    try:
                        text = self.recognizer.recognize_google(audio)
                        if callback:
                            callback(text)
                    except sr.UnknownValueError:
                        pass
                    except sr.RequestError:
                        pass
                except Exception as e:
                    print(f"Background listening error: {e}")
        
        thread = threading.Thread(target=background_listener)
        thread.daemon = True
        thread.start()
    
    def stop_speaking(self):
        """Stop current speech"""
        try:
            self.tts_engine.stop()
            self.is_speaking = False
        except:
            pass
    
    def set_voice_rate(self, rate):
        """Set speech rate"""
        self.tts_engine.setProperty('rate', rate)
        self.config.voice_rate = rate
    
    def set_voice_volume(self, volume):
        """Set speech volume"""
        self.tts_engine.setProperty('volume', volume)
        self.config.voice_volume = volume
