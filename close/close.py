import keyboard
import pyautogui
import tkinter as tk
from tkinter import messagebox
import threading
import subprocess

def is_ctrl_space_pressed():
    return keyboard.is_pressed('ctrl') and keyboard.is_pressed('space')

def show_confirmation():
    # 创建顶级窗口
    top = tk.Toplevel(root)
    top.attributes('-alpha', 0.0001)
    top.attributes('-topmost', True)
    top.overrideredirect(True)
    top.title("确认")
    top.geometry("300x100")
    # 在顶级窗口中显示确认框，并传递父窗口信息
    result = messagebox.askyesno("确认", "是否执行点击操作？", parent=top)

    # 销毁顶级窗口
    top.destroy()

    return result

def click_screen():
    # 获取屏幕的宽度和高度
    screen_width, screen_height = pyautogui.size()

    # 保存当前鼠标位置
    original_x, original_y = pyautogui.position()

    # 设置要点击的位置为屏幕右上角
    target_x = screen_width - 1
    target_y = 1

    # 检测Ctrl键和空格键是否同时被按下
    while is_ctrl_space_pressed():
        pass  # 等待

    # 显示确认框
    if show_confirmation():
        # 移动鼠标到目标位置
        pyautogui.moveTo(target_x, target_y)
        # 在目标位置点击鼠标
        pyautogui.click()

        # 恢复鼠标到原来位置
        pyautogui.moveTo(original_x, original_y)

def listen_keyboard():
    # 监听 Ctrl + Space 键按下事件
    keyboard.add_hotkey('ctrl+space', lambda: click_screen())

# 创建一个 tkinter 窗口并隐藏
root = tk.Tk()
root.withdraw()

# 定义一个函数用于在主线程中运行 tkinter 的主循环
def run_tkinter():
    root.mainloop()

# 使用 threading 在新线程中运行键盘监听
keyboard_thread = threading.Thread(target=listen_keyboard)
keyboard_thread.start()

# 使用 subprocess 调用 pythonw.exe 来运行程序，以实现后台运行
subprocess.Popen(["pythonw", "main.py"], creationflags=subprocess.DETACHED_PROCESS, close_fds=True)

# 运行 tkinter 主循环（在主线程中运行）
run_tkinter()

# 防止主线程结束，这样键盘监听和 tkinter 主循环能够一直运行
keyboard_thread.join()
