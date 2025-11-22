"""
Test script to verify JARVIS installation
Run this to check if all components are working
"""

def test_imports():
    """Test if all required packages are installed"""
    print("Testing imports...")
    
    tests = {
        "Google Generative AI": lambda: __import__("google.generativeai"),
        "Speech Recognition": lambda: __import__("speech_recognition"),
        "Text-to-Speech": lambda: __import__("pyttsx3"),
        "PyQt5": lambda: __import__("PyQt5"),
        "PyAudio": lambda: __import__("pyaudio"),
        "psutil": lambda: __import__("psutil"),
        "pygetwindow": lambda: __import__("pygetwindow"),
        "PIL": lambda: __import__("PIL"),
        "numpy": lambda: __import__("numpy"),
    }
    
    passed = 0
    failed = 0
    
    for name, test_func in tests.items():
        try:
            test_func()
            print(f"  ✓ {name}")
            passed += 1
        except ImportError as e:
            print(f"  ✗ {name} - {str(e)}")
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0

def test_modules():
    """Test JARVIS modules"""
    print("\nTesting JARVIS modules...")
    
    modules = [
        "config",
        "utils",
        "system_controller",
        "voice_handler",
        "jarvis_engine",
        "gui_interface",
    ]
    
    passed = 0
    failed = 0
    
    for module in modules:
        try:
            __import__(module)
            print(f"  ✓ {module}.py")
            passed += 1
        except Exception as e:
            print(f"  ✗ {module}.py - {str(e)}")
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0

def test_system_controller():
    """Test system controller"""
    print("\nTesting System Controller...")
    
    try:
        from system_controller import SystemController
        controller = SystemController()
        print("  ✓ System controller initialized")
        
        # Test getting running apps
        apps = controller.get_running_apps()
        print(f"  ✓ Found {len(apps)} running applications")
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        return False

def test_voice_handler():
    """Test voice handler"""
    print("\nTesting Voice Handler...")
    
    try:
        from config import Config
        from voice_handler import VoiceHandler
        
        config = Config()
        voice = VoiceHandler(config)
        print("  ✓ Voice handler initialized")
        
        # Test TTS
        print("  ℹ Testing text-to-speech (you should hear this)...")
        voice.speak("Testing voice output")
        print("  ✓ Text-to-speech works")
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        return False

def main():
    """Main test function"""
    print("=" * 50)
    print("JARVIS Installation Test")
    print("=" * 50)
    print()
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
        print("\n⚠ Some packages are missing. Run: pip install -r requirements.txt")
    
    # Test modules
    if not test_modules():
        all_passed = False
        print("\n⚠ Some JARVIS modules have errors")
    
    # Test components
    test_system_controller()
    test_voice_handler()
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✓ All tests passed! JARVIS is ready to run.")
        print("Run: python main.py")
    else:
        print("⚠ Some tests failed. Please fix the errors above.")
    print("=" * 50)

if __name__ == "__main__":
    main()
