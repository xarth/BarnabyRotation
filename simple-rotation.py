import time
import mss
from PIL import Image
import pytesseract
import pyautogui
import keyboard
from random import randint
import threading

running = False

#if tesseract isn’t on the path, set manually:
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# use cords.py to select a section of the screen and give the cords you should use.
region = {
    "top": 1943, 
    "left": 2849,
    "width": 262,
    "height": 140
}


def read_keybind(region):
    """Grab the screen region and OCR the keybind."""
    with mss.mss() as sct:
        img = sct.grab(region)
        img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
        img = img.convert("L")  # grayscale
        text = pytesseract.image_to_string(img, config="--psm 7")
        return text.strip().lower()


def press_keybind(keybind):
    """Parse OCR output and press the key (with modifier if exists)."""
    if not keybind:
        print("[!] No keybind detected.")
        return

    print(f"[+] OCR detected: {keybind}")

    parts = [p.strip() for p in keybind.split('-')]

    if len(parts) == 1:
        # Single key
        key = parts[0]
        try:
            pyautogui.press(key)
            print(f"[+] Pressed: {key}")
        except:
            print(f"[!] Could not press key: {key}")

    elif len(parts) == 2:
        # Modifier + key
        modifier, key = parts
        modifier_map = {
            's': 'shift',
            'shift': 'shift',
            'ctrl': 'ctrl',
            'c': 'ctrl',
            'alt': 'alt',
        }
        mod_key = modifier_map.get(modifier, modifier)

        try:
            pyautogui.keyDown(mod_key)
            pyautogui.press(key)
            pyautogui.keyUp(mod_key)
            print(f"[+] Pressed: {mod_key} + {key}")
        except:
            print(f"[!] Could not press combination: {mod_key} + {key}")
    else:
        print("[!] Unexpected format:", keybind)


def scan_loop():
    global running
    print("[*] Scan loop started. Press F8 to stop.")
    while running:
        keybind = read_keybind(region)
        press_keybind(keybind)
        sleep_time = randint(50, 250) / 1000.0  # small delay to prevent spamming
        print(f"[-] Wait time on key press: {sleep_time:3f}")
        time.sleep(sleep_time)


def toggle_running():
    global running
    running = not running
    if running:
        # Start the scanning loop in a new thread
        threading.Thread(target=scan_loop, daemon=True).start()
        print("[*] Keybind scanning activated!")
    else:
        print("[*] Keybind scanning deactivated!")


def main():
    print("[*] Press F8 to start/stop keybind scanning.")
    keyboard.add_hotkey("F8", toggle_running)

    # Keep the script alive
    while True:
        time.sleep(0.1)

if __name__ == "__main__":
    main()