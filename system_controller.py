"""
System Controller - Handles system operations like opening/closing apps
"""
import subprocess
import psutil
import os
import sys
import pygetwindow as gw

class SystemController:
    """Controller for system-level operations"""
    
    def __init__(self):
        self.common_apps = {
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'paint': 'mspaint.exe',
            'chrome': 'chrome.exe',
            'firefox': 'firefox.exe',
            'edge': 'msedge.exe',
            'explorer': 'explorer.exe',
            'word': 'WINWORD.EXE',
            'excel': 'EXCEL.EXE',
            'powerpoint': 'POWERPNT.EXE',
            'vscode': 'Code.exe',
            'vs code': 'Code.exe',
            'visual studio code': 'Code.exe',
            'spotify': 'Spotify.exe',
            'discord': 'Discord.exe',
            'teams': 'Teams.exe',
            'outlook': 'OUTLOOK.EXE',
            'cmd': 'cmd.exe',
            'command prompt': 'cmd.exe',
            'powershell': 'powershell.exe',
        }
    
    def open_application(self, app_name):
        """Open an application"""
        try:
            app_name_lower = app_name.lower().strip()
            
            # Check common apps
            if app_name_lower in self.common_apps:
                subprocess.Popen(self.common_apps[app_name_lower])
                return True, f"Opening {app_name}"
            
            # Try to open as is
            try:
                subprocess.Popen(app_name)
                return True, f"Opening {app_name}"
            except:
                pass
            
            # Try with .exe extension
            try:
                subprocess.Popen(f"{app_name}.exe")
                return True, f"Opening {app_name}"
            except:
                pass
            
            # Try using start command
            try:
                subprocess.Popen(f'start {app_name}', shell=True)
                return True, f"Opening {app_name}"
            except:
                pass
            
            return False, f"Could not find application: {app_name}"
            
        except Exception as e:
            return False, f"Error opening {app_name}: {str(e)}"
    
    def close_application(self, app_name):
        """Close an application"""
        try:
            app_name_lower = app_name.lower().strip()
            closed = False
            
            # Get the process name
            process_name = self.common_apps.get(app_name_lower, f"{app_name}.exe")
            if not process_name.endswith('.exe'):
                process_name += '.exe'
            
            # Find and terminate the process
            for proc in psutil.process_iter(['name']):
                try:
                    if proc.info['name'].lower() == process_name.lower():
                        proc.terminate()
                        closed = True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if closed:
                return True, f"Closed {app_name}"
            else:
                return False, f"{app_name} is not running"
                
        except Exception as e:
            return False, f"Error closing {app_name}: {str(e)}"
    
    def get_running_apps(self):
        """Get list of running applications"""
        try:
            apps = set()
            for proc in psutil.process_iter(['name']):
                try:
                    apps.add(proc.info['name'])
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            return list(apps)
        except Exception as e:
            return []
    
    def minimize_all_windows(self):
        """Minimize all windows"""
        try:
            import ctypes
            ctypes.windll.user32.keybd_event(0x5B, 0, 0, 0)  # Win key down
            ctypes.windll.user32.keybd_event(0x4D, 0, 0, 0)  # M key down
            ctypes.windll.user32.keybd_event(0x4D, 0, 2, 0)  # M key up
            ctypes.windll.user32.keybd_event(0x5B, 0, 2, 0)  # Win key up
            return True, "Minimized all windows"
        except Exception as e:
            return False, f"Error minimizing windows: {str(e)}"
    
    def open_website(self, url):
        """Open a website in default browser"""
        try:
            import webbrowser
            if not url.startswith('http'):
                url = 'https://' + url
            webbrowser.open(url)
            return True, f"Opening {url}"
        except Exception as e:
            return False, f"Error opening website: {str(e)}"
    
    def search_google(self, query):
        """Search Google"""
        try:
            import webbrowser
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            return True, f"Searching Google for {query}"
        except Exception as e:
            return False, f"Error searching: {str(e)}"
    
    def get_system_info(self):
        """Get system information"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            info = f"CPU Usage: {cpu_percent}%\n"
            info += f"Memory Usage: {memory.percent}%\n"
            info += f"Disk Usage: {disk.percent}%"
            
            return True, info
        except Exception as e:
            return False, f"Error getting system info: {str(e)}"
    
    def shutdown_system(self):
        """Shutdown the system"""
        try:
            os.system("shutdown /s /t 30")
            return True, "System will shutdown in 30 seconds"
        except Exception as e:
            return False, f"Error shutting down: {str(e)}"
    
    def restart_system(self):
        """Restart the system"""
        try:
            os.system("shutdown /r /t 30")
            return True, "System will restart in 30 seconds"
        except Exception as e:
            return False, f"Error restarting: {str(e)}"
