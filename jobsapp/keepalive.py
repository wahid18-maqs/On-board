import threading
import time
import requests
import os

def ping_self():
    while True:
        try:
            print("⏰ Pinging self to prevent Render sleep...")
            requests.get("https://on-board.onrender.com/")
        except Exception as e:
            print(" Ping failed:", e)
        time.sleep(900)  # 15 minutes

def start_ping_thread():
    # Only start pinging if deployed on Render
    if os.environ.get("RENDER", "").lower() == "true":
        thread = threading.Thread(target=ping_self, daemon=True)
        thread.start()
