# screenshot_logger.py
from PIL import ImageGrab
import time
import os

SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def capture_screenshot():
    try:
        screenshot = ImageGrab.grab()
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        screenshot.save(os.path.join(SCREENSHOT_DIR, f"screenshot_{timestamp}.png"))
    except Exception as e:
        print(f"Screenshot Logger Error: {e}")