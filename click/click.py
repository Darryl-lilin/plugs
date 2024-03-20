import pyautogui
from pynput import keyboard
import threading
import time

class Clicker:
    def __init__(self):
        self.running = False

    def start_clicking(self, interval):
        self.running = True
        print("连点器开始运行，按 F9 停止。")
        while self.running:
            pyautogui.click()
            time.sleep(interval)

    def stop_clicking(self):
        self.running = False
        print("连点器停止。")

clicker = Clicker()

def on_press(key):
    if key == keyboard.Key.f8:
        threading.Thread(target=clicker.start_clicking, args=(0.1,)).start()
    elif key == keyboard.Key.f9:
        clicker.stop_clicking()

def on_release(key):
    pass

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
