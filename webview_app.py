"""
WebView2 App with Custom Taskbar Icon - FIXED
Uses Windows API to set the icon after window creation
"""

import webview
import os
import sys
from pathlib import Path
import ctypes
from ctypes import wintypes

# === CONFIGURATION ===
TARGET_URL = "https://app.telecord.qzz.io"  # CHANGE THIS
APP_NAME = "Telecord"
ICON_FILE = "app.ico"  # Your icon file
# =====================

def set_window_icon(window, icon_path):
    """Set the window icon using Windows API"""
    try:
        if not os.path.exists(icon_path):
            print(f"Warning: Icon not found: {icon_path}")
            return False
        
        # Get window handle
        hwnd = window.get_current_window()
        if not hwnd:
            print("Error: Could not get window handle")
            return False
        
        # Load icon
        hinst = ctypes.windll.kernel32.GetModuleHandleW(None)
        hicon = ctypes.windll.user32.LoadImageW(
            hinst,
            icon_path,
            1,  # IMAGE_ICON
            0,  # Default width
            0,  # Default height
            0x00000010  # LR_LOADFROMFILE
        )
        
        if hicon:
            # Set the window icon
            ctypes.windll.user32.SendMessageW(
                hwnd,
                0x0080,  # WM_SETICON
                0,  # ICON_SMALL
                hicon
            )
            ctypes.windll.user32.SendMessageW(
                hwnd,
                0x0080,  # WM_SETICON
                1,  # ICON_BIG
                hicon
            )
            print("Icon set successfully!")
            return True
        else:
            print("Failed to load icon")
            return False
            
    except Exception as e:
        print(f"Error setting icon: {e}")
        return False

def get_icon_path():
    """Get the full path to icon file"""
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    
    icon_path = os.path.join(base, ICON_FILE)
    print(f"Looking for icon at: {icon_path}")
    return icon_path if os.path.exists(icon_path) else None

def main():
    # Setup persistent storage
    if getattr(sys, 'frozen', False):
        data_folder = os.path.join(os.environ.get('LOCALAPPDATA', ''), APP_NAME)
    else:
        data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    
    Path(data_folder).mkdir(parents=True, exist_ok=True)
    os.environ['WEBVIEW2_USER_DATA_FOLDER'] = data_folder
    
    print(f"Data folder: {data_folder}")
    
    # Create window (without icon parameter)
    window = webview.create_window(
        title=APP_NAME,
        url=TARGET_URL,
        width=1280,
        height=800,
        resizable=True,
        min_size=(800, 600),
    )
    
    # Set icon after window creation
    icon_path = get_icon_path()
    if icon_path:
        # We need to set icon after the window is created
        # Using a timer to set it when window appears
        def set_icon_later():
            import time
            time.sleep(0.5)  # Wait for window to be created
            set_window_icon(window, icon_path)
        
        import threading
        threading.Thread(target=set_icon_later, daemon=True).start()
    
    # Run
    webview.start(
        gui='edgechromium',
        private_mode=False,
        storage_path=data_folder,
    )

if __name__ == "__main__":
    main()
