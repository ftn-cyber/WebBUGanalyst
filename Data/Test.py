#!/usr/bin/env python3
import os
import sys
import webbrowser
import platform

TARGET_URL = "https://www.gzzjgf.com/promopadang"

def main():
    print(f"[+] Membuka URL: {TARGET_URL}")
    try:
        # Buka URL di browser default
        webbrowser.open(TARGET_URL)
        
        # Opsional: Sembunyikan jendela konsol (Windows)
        if platform.system() == "Windows":
            import ctypes
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
            
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    main()
