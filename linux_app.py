"""
Linux Desktop App - Uses WebKitGTK (native Linux webview)
Full modern JavaScript support, persistent storage, custom icon
"""

import webview
import os
import sys
from pathlib import Path

# === CONFIGURATION ===
TARGET_URL = "https://telecord.idebugger.qzz.io"  # CHANGE THIS
APP_NAME = "Telecord"
ICON_FILE = "app.ico"  # Your icon file (optional, Linux may not use it)
# =====================

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
    # Setup persistent storage (localStorage, cookies, etc.)
    if getattr(sys, 'frozen', False):
        data_folder = os.path.join(os.environ.get('HOME', ''), '.config', APP_NAME)
    else:
        data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    
    Path(data_folder).mkdir(parents=True, exist_ok=True)
    
    # For Linux, WebKit stores data here
    os.environ['WEBKIT_DISABLE_COMPOSITING_MODE'] = '1'  # Better performance on some systems
    
    print(f"Data folder: {data_folder}")
    
    # Create window with icon (if available)
    icon_path = get_icon_path()
    
    window = webview.create_window(
        title=APP_NAME,
        url=TARGET_URL,
        width=1280,
        height=800,
        resizable=True,
        min_size=(800, 600),
        icon=icon_path if icon_path else None,  # Linux supports .png or .ico
    )
    
    # Run
    webview.start(
        gui='qt',  # Use Qt backend (more reliable than GTK on some systems)
        private_mode=False,  # Enable localStorage persistence
        storage_path=data_folder,
    )

if __name__ == "__main__":
    main()
