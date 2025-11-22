# Quick Start Guide for JARVIS

## Installation (3 Easy Steps)

### Step 1: Install Dependencies
Open PowerShell in the Jarvis folder and run:
```powershell
.\install.ps1
```

Or manually:
```powershell
pip install -r requirements.txt
```

### Step 2: Get Gemini API Key
1. Visit: https://makersuite.google.com/app/apikey
2. Create an API key
3. Copy it (you'll need it when you first run JARVIS)

### Step 3: Run JARVIS
Double-click `run_jarvis.bat` or run:
```powershell
python main.py
```

## First Run

1. JARVIS will ask for your API key
2. Paste it and click Submit
3. Start talking to JARVIS!

## Common Commands

- "Open Chrome"
- "Close Notepad"
- "What time is it?"
- "Search Google for [query]"
- "Open website [url]"
- "System info"
- "Tell me about [topic]"

## Troubleshooting

**PyAudio won't install?**
- Download from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
- Install with: `pip install downloaded_file.whl`

**Voice input not working?**
- Check microphone permissions
- Ensure internet connection
- Set microphone as default input device

**API errors?**
- Verify API key is correct
- Check internet connection
- Ensure Gemini API is enabled in your Google Cloud account

## Testing Installation

Run the test script:
```powershell
python test_installation.py
```

This will verify all components are working correctly.

---

Enjoy your personal AI assistant! 🚀
