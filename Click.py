import pyautogui
from PIL import Image
import mss
import tkinter as tk
from tkinter import scrolledtext
import logging
import threading
import time
import cv2
import numpy as np

# 共享变量
shared_variable = "开始"

# 锁用于同步线程对共享变量的访问
lock = threading.Lock()


class LogWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("日志窗口")

        # 创建滚动文本框
        self.log_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=50, height=20)
        self.log_text.pack(expand=True, fill='both')

        # 设置日志级别和格式
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        # 创建并启动日志处理线程
        self.log_thread = threading.Thread(target=self.log_worker, daemon=True)
        self.log_thread.start()

        # 启动定时任务，模拟产生日志信息
        # self.start_logging_simulation()

    def log_worker(self):
        global shared_variable
        with lock:
            # 模拟日志信息
            log_message = f"{time.strftime('%H:%M:%S')}:{shared_variable}"

            # 将日志信息显示在滚动文本框中
            self.log_text.insert(tk.END, log_message + '\n')
            self.log_text.see(tk.END)  # 滚动到底部

            # 记录日志到文件
            logging.info(log_message)
        while True:
            time.sleep(1)
            if shared_variable != "开始":
                with lock:
                    # 模拟日志信息
                    log_message = f"{time.strftime('%H:%M:%S')}:{shared_variable}"

                    # 将日志信息显示在滚动文本框中
                    self.log_text.insert(tk.END, log_message + '\n')
                    self.log_text.see(tk.END)  # 滚动到底部

                    # 记录日志到文件
                    logging.info(log_message)

                # 等待一段时间
                time.sleep(2)
                shared_variable = "开始"

    # def start_logging_simulation(self):


# 不再使用定时任务，因为 log_worker 中已经有了循环


def find_target_on_screen(target_image_path, confidence=0.8):
    # 读取目标图片
    target_image = cv2.imread(target_image_path, cv2.IMREAD_UNCHANGED)
    target_height, target_width = target_image.shape[:2]

    while True:
        # 截取屏幕截图
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # 在屏幕截图中进行模板匹配
        result = cv2.matchTemplate(screenshot, target_image, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # 如果置信度足够高，认为目标被找到
        if max_val >= confidence:
            top_left = max_loc
            bottom_right = (top_left[0] + target_width, top_left[1] + target_height)

            # 返回目标位置
            return top_left, bottom_right

        # 按 'q' 键退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


def click(target_image_path):
    while True:
        time.sleep(1)
        try:
            # 在动态屏幕中实时检测目标图片
            result = find_target_on_screen(target_image_path)
            if result is not None:
                # 获取目标图片中心坐标
                target_center_x = (result[0][0] + result[1][0]) / 2
                target_center_y = (result[0][1] + result[1][1]) / 2
                # 移动鼠标到目标图片中心并点击
                pyautogui.moveTo(target_center_x, target_center_y)
                pyautogui.click()
                with lock:
                    global shared_variable
                    shared_variable = "签到成功"
                print("目标图片已找到并点击成功！")
                return True
            else:
                print("未找到目标图片")
        except Exception as e:
            print(f"发生错误: {e}")


def locate_and_click(target_image_path, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:

        # 从屏幕中找到指定图像的位置
        try:
            # 在动态屏幕中实时检测目标图片
            result = find_target_on_screen(target_image_path)
            if result is not None:
                # 获取目标图片中心坐标
                target_center_x = (result[0][0] + result[1][0]) / 2
                target_center_y = (result[0][1] + result[1][1]) / 2
                # 移动鼠标到目标图片中心并点击
                pyautogui.moveTo(target_center_x, target_center_y)
                pyautogui.click()
            time.sleep(2)
            if click("sign.png"):
                time.sleep(1)
                capture_and_save_screen(f"{time.strftime('%Y-%m-%d', time.localtime())}-{time.strftime('%H-%M-%S')}.png")
                time.sleep(1)
                pyautogui.click()
            return True
        except Exception as e:
            print("未找到目标图片")
            # 等待一小段时间再进行下一次识别
            time.sleep(1)

    return False


def capture_and_save_screen(output_path="screenshot.png"):
    print(output_path)
    with mss.mss() as sct:
        screenshot = sct.shot(output=output_path)
    return screenshot


def windowT():
    log_window = LogWindow()
    log_window.mainloop()


def sign():
    # 图像文件路径，替换成即将出现的目标图像
    target_image_path = "join.png"
    # 执行屏幕识别并点击，设置超时时间为30秒
    success = locate_and_click(target_image_path, timeout=360000)

    if success:
        print("点击成功！")
        while True:
            locate_and_click(target_image_path, timeout=360000)
    else:
        print("在超时时间内找不到目标图像。")


if __name__ == "__main__":
    t1 = threading.Thread(target=windowT)  # 定义线程t1，线程任务为调用task1函数，task1函数的参数是6
    t2 = threading.Thread(target=sign)  # 定义线程t2，线程任务为调用task2函数，task2函数无参数
    t1.start()  # 开始运行t1线程
    t2.start()  # 开始运行t2线程
