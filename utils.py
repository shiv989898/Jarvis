"""
Utility functions for Jarvis Personal Assistant
"""
import datetime
import re

def get_greeting():
    """Get time-appropriate greeting"""
    current_hour = datetime.datetime.now().hour
    
    if current_hour < 12:
        return "Good morning"
    elif current_hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"

def format_time():
    """Get current time in readable format"""
    now = datetime.datetime.now()
    return now.strftime("%I:%M %p")

def format_date():
    """Get current date in readable format"""
    now = datetime.datetime.now()
    return now.strftime("%B %d, %Y")

def extract_app_name(text):
    """Extract application name from command"""
    # Patterns for opening apps
    patterns = [
        r'open\s+(.+)',
        r'launch\s+(.+)',
        r'start\s+(.+)',
        r'run\s+(.+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            return match.group(1).strip()
    return None

def extract_close_app_name(text):
    """Extract application name for closing"""
    patterns = [
        r'close\s+(.+)',
        r'quit\s+(.+)',
        r'exit\s+(.+)',
        r'stop\s+(.+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            return match.group(1).strip()
    return None

def clean_text(text):
    """Clean and normalize text"""
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    return text

def is_question(text):
    """Check if text is a question"""
    question_words = ['what', 'when', 'where', 'who', 'why', 'how', 'is', 'are', 'can', 'could', 'would', 'should']
    text_lower = text.lower().strip()
    return text_lower.endswith('?') or any(text_lower.startswith(word) for word in question_words)
