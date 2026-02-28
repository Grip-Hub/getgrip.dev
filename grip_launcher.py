"""
GRIP Desktop — Search your files intelligently.
Double-click to run. Your browser opens automatically.
"""
import sys
import os
import time
import threading
import webbrowser

# ── Setup data directory in user's home folder ──
GRIP_HOME = os.path.join(os.path.expanduser("~"), ".grip")
os.makedirs(GRIP_HOME, exist_ok=True)
os.environ["GRIP_DATA_DIR"] = GRIP_HOME

# ── External packages folder ──
# Users can install optional deps here without rebuilding:
#   pip install --target ~/.grip/packages requests
#   pip install --target ~/.grip/packages openai
PACKAGES_DIR = os.path.join(GRIP_HOME, "packages")
os.makedirs(PACKAGES_DIR, exist_ok=True)
if PACKAGES_DIR not in sys.path:
    sys.path.insert(0, PACKAGES_DIR)

# If frozen (PyInstaller), suppress noisy logs
if getattr(sys, "frozen", False):
    os.environ.setdefault("GRIP_LOG_LEVEL", "warning")


def open_browser():
    """Wait for server to be ready, then open the browser."""
    import urllib.request
    for _ in range(60):  # Try for 30 seconds
        time.sleep(0.5)
        try:
            urllib.request.urlopen("http://localhost:7878/health")
            webbrowser.open("http://localhost:7878")
            return
        except Exception:
            continue
    webbrowser.open("http://localhost:7878")


def print_banner():
    print()
    print("  ╔══════════════════════════════════════════════╗")
    print("  ║              GRIP — File Search              ║")
    print("  ║                                              ║")
    print("  ║  Your browser will open automatically.       ║")
    print("  ║                                              ║")
    print("  ║  1. Click 'Browse' to pick a folder          ║")
    print("  ║  2. Wait for indexing to finish               ║")
    print("  ║  3. Search for anything                       ║")
    print("  ║                                              ║")
    print("  ║  Keep this window open while using GRIP.     ║")
    print("  ║  Close this window to stop GRIP.             ║")
    print("  ╚══════════════════════════════════════════════╝")
    print()
    print(f"  Extensions folder: {PACKAGES_DIR}")
    print(f"  Install optional deps with:")
    print(f"    pip install --target \"{PACKAGES_DIR}\" requests")
    print()


def main():
    print_banner()

    # Check if port is already in use
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(("127.0.0.1", 7878))
        sock.close()
    except OSError:
        print("  ⚠ Port 7878 is already in use.")
        print("  GRIP may already be running.")
        print("  Open http://localhost:7878 in your browser.")
        print()
        webbrowser.open("http://localhost:7878")
        input("  Press Enter to exit...")
        return

    # Open browser in background
    threading.Thread(target=open_browser, daemon=True).start()

    # Start the server
    import uvicorn
    from grip_retrieval.server import app
    uvicorn.run(app, host="127.0.0.1", port=7878, log_level="warning")


if __name__ == "__main__":
    main()
