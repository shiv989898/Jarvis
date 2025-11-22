"""
Jarvis Engine - Core AI processing using Google Gemini
"""
import google.generativeai as genai
from utils import *
from datetime import datetime
import re

class JarvisEngine:
    """Core engine for Jarvis AI assistant"""
    
    def __init__(self, config, system_controller):
        self.config = config
        self.system_controller = system_controller
        self.model = None
        self.chat = None
        self.conversation_history = []
        
        # Initialize if API key is available
        if config.api_key:
            self.initialize_gemini()
    
    def initialize_gemini(self):
        """Initialize Gemini AI"""
        try:
            genai.configure(api_key=self.config.api_key)
            
            # Configure the model
            generation_config = {
                "temperature": 0.9,
                "top_p": 1,
                "top_k": 1,
                "max_output_tokens": 2048,
            }
            
            safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            ]
            
            self.model = genai.GenerativeModel(
                model_name="gemini-pro",
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            
            # Start chat with context
            self.chat = self.model.start_chat(history=[])
            
            return True, "Gemini AI initialized successfully"
        except Exception as e:
            return False, f"Error initializing Gemini: {str(e)}"
    
    def process_command(self, user_input):
        """Process user command and return response"""
        user_input = clean_text(user_input)
        
        if not user_input:
            return "I didn't catch that. Could you please repeat?"
        
        # Store in history
        self.conversation_history.append({
            'timestamp': datetime.now(),
            'user': user_input,
            'response': None
        })
        
        # Check for system commands first
        response = self._handle_system_commands(user_input)
        if response:
            self.conversation_history[-1]['response'] = response
            return response
        
        # Use Gemini AI for general queries
        if self.model and self.chat:
            try:
                # Add context to the query
                enhanced_query = self._enhance_query(user_input)
                response_obj = self.chat.send_message(enhanced_query)
                response = response_obj.text
                self.conversation_history[-1]['response'] = response
                return response
            except Exception as e:
                error_msg = f"I encountered an error: {str(e)}"
                self.conversation_history[-1]['response'] = error_msg
                return error_msg
        else:
            response = "I'm not fully initialized yet. Please make sure the API key is set."
            self.conversation_history[-1]['response'] = response
            return response
    
    def _handle_system_commands(self, user_input):
        """Handle system-level commands"""
        input_lower = user_input.lower()
        
        # Time and date
        if any(word in input_lower for word in ['what time', 'current time', 'time is it']):
            return f"The current time is {format_time()}"
        
        if any(word in input_lower for word in ['what date', 'today date', 'what day']):
            return f"Today is {format_date()}"
        
        # Open application
        if any(word in input_lower for word in ['open', 'launch', 'start', 'run']):
            app_name = extract_app_name(user_input)
            if app_name:
                success, message = self.system_controller.open_application(app_name)
                return message
        
        # Close application
        if any(word in input_lower for word in ['close', 'quit', 'exit', 'stop']):
            app_name = extract_close_app_name(user_input)
            if app_name and app_name not in ['jarvis', 'yourself']:
                success, message = self.system_controller.close_application(app_name)
                return message
        
        # Search Google
        if 'search google' in input_lower or 'google search' in input_lower:
            query = re.sub(r'(search google|google search)\s*(for)?', '', input_lower, flags=re.IGNORECASE).strip()
            if query:
                success, message = self.system_controller.search_google(query)
                return message
        
        # Open website
        if 'open website' in input_lower or 'go to' in input_lower:
            url = re.sub(r'(open website|go to)\s*', '', input_lower, flags=re.IGNORECASE).strip()
            if url:
                success, message = self.system_controller.open_website(url)
                return message
        
        # System info
        if 'system info' in input_lower or 'system status' in input_lower:
            success, message = self.system_controller.get_system_info()
            return message
        
        # Minimize windows
        if 'minimize all' in input_lower or 'minimize windows' in input_lower:
            success, message = self.system_controller.minimize_all_windows()
            return message
        
        # Running apps
        if 'running apps' in input_lower or 'open apps' in input_lower:
            apps = self.system_controller.get_running_apps()
            return f"Currently running {len(apps)} applications"
        
        # Shutdown
        if 'shutdown' in input_lower and 'computer' in input_lower:
            success, message = self.system_controller.shutdown_system()
            return message
        
        # Restart
        if 'restart' in input_lower and 'computer' in input_lower:
            success, message = self.system_controller.restart_system()
            return message
        
        return None
    
    def _enhance_query(self, query):
        """Enhance query with context"""
        # Add personality and context
        system_context = """You are Jarvis, an advanced AI personal assistant inspired by Iron Man's AI. 
        You are helpful, intelligent, and have a sophisticated personality. 
        Respond in a concise, friendly, and professional manner. 
        Keep responses brief unless asked for detailed information."""
        
        enhanced = f"{system_context}\n\nUser query: {query}"
        return enhanced
    
    def get_greeting(self):
        """Get personalized greeting"""
        greeting = get_greeting()
        return f"{greeting}! I'm Jarvis, your personal assistant. How may I help you today?"
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        if self.model:
            self.chat = self.model.start_chat(history=[])
