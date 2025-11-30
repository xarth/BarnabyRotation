import cv2
import numpy as np
import pytesseract
import pyautogui
from random import randint
from time import sleep
from PIL import ImageGrab
import webcolors
from multiprocessing import Process
import getpixelcolor

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]


def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return closest_name


def combat_check():
    ARE_WE_GOOD = 'No'
    is_in_combat_checker = getpixelcolor.pixel(2604, 908)
    ARE_WE_GOOD = get_colour_name(is_in_combat_checker)
    print(ARE_WE_GOOD)
    return (ARE_WE_GOOD)
    

def rotation():
    while True:
        if combat_check() == "red":
            # This instance will generate an image from the point
            rotation = ImageGrab.grab(bbox=(1850, 1300, 1900, 1385))
            rotation_array = np.array(rotation)
            cv2.imshow("", rotation_array)

            keybind = pytesseract.image_to_string(rotation,config ='--psm 7')
            keybind = keybind.strip()
            keybind = keybind.lower()

            if len(keybind) > 0:
                print(keybind)

            #Random sleep in milliseconds to ensure that its  not just being spammed and try and avoid detection
            #pause = randint(50, 250) / 1000.0
            #sleep(pause)
            if keybind.startswith('s'):
                pyautogui.hotkey('shift', keybind.lower().strip('s'))
            elif keybind.startswith('c'):
                pyautogui.hotkey('ctrl', keybind.lower().strip('c'))
            else:
                pyautogui.press(keybind.lower())
        else:
            print("not in combat")
            sleep(0.3)

if __name__ == '__main__':
    p1 = Process(target=rotation)
    p1.start()
