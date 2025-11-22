# JARVIS Installation Script
# Run this script to install all dependencies

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "JARVIS Installation Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow

# Try different Python commands
$pythonCmd = $null
foreach ($cmd in @("python", "python3", "C:\Python\python.exe", "C:\Python39\python.exe", "C:\Python310\python.exe", "C:\Python311\python.exe", "C:\Python312\python.exe")) {
    try {
        $version = & $cmd --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            $pythonCmd = $cmd
            Write-Host "✓ Python found: $version (using: $cmd)" -ForegroundColor Green
            break
        }
    } catch {}
}

if (-not $pythonCmd) {
    Write-Host "✗ Python not found. Please make sure Python is in PATH or installed." -ForegroundColor Red
    exit 1
}

# Use the found Python command for installations
$python = $pythonCmd

Write-Host ""
Write-Host "Installing Python packages..." -ForegroundColor Yellow
Write-Host ""

# Install main packages
& $python -m pip install --upgrade pip
& $python -m pip install google-generativeai SpeechRecognition pyttsx3 PyQt5 pydub psutil pygetwindow pillow numpy

Write-Host ""
Write-Host "Installing PyAudio (this might take a moment)..." -ForegroundColor Yellow

# Try to install PyAudio
$pyaudioInstalled = $false

# Method 1: Direct pip install
try {
    & $python -m pip install pyaudio 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        $pyaudioInstalled = $true
        Write-Host "✓ PyAudio installed successfully" -ForegroundColor Green
    }
} catch {}

# Method 2: Try pipwin if first method failed
if (-not $pyaudioInstalled) {
    Write-Host "Trying alternative installation method..." -ForegroundColor Yellow
    try {
        & $python -m pip install pipwin
        & $python -m pipwin install pyaudio
        $pyaudioInstalled = $true
        Write-Host "✓ PyAudio installed successfully via pipwin" -ForegroundColor Green
    } catch {}
}

if (-not $pyaudioInstalled) {
    Write-Host "⚠ PyAudio installation may have failed." -ForegroundColor Red
    Write-Host "Voice input might not work properly." -ForegroundColor Red
    Write-Host "Please install PyAudio manually from:" -ForegroundColor Yellow
    Write-Host "https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To run JARVIS, use: $python main.py" -ForegroundColor Yellow
Write-Host "Or double-click: run_jarvis.bat" -ForegroundColor Yellow
Write-Host ""
Write-Host "Make sure you have:" -ForegroundColor Yellow
Write-Host "  1. A Google Gemini API key" -ForegroundColor White
Write-Host "  2. A working microphone" -ForegroundColor White
Write-Host "  3. Internet connection" -ForegroundColor White
Write-Host ""
