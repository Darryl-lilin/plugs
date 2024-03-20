import pyperclip
import csv
import tkinter as tk


def fuzzy_match(pattern, text):
    """
    实现简单的模糊匹配，如果模式中的字符在文本中出现，则返回 True，否则返回 False。
    """
    pattern = pattern.lower()
    text = text.lower()
    return all(char in text for char in pattern)


def find_last_answer(csv_file, pattern):
    """
    从 CSV 文件中查找每行的最后一个答案，如果行中有模糊匹配的项，则返回最后一个答案。
    """
    results = []
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            for item in row:
                if fuzzy_match(pattern, item):
                    results.append(row[-1])
                    break
        return results


def get_latest_clipboard_text(csv_file):
    previous_clipboard_text = ""

    def update_result():
        nonlocal previous_clipboard_text
        # 获取最新的剪贴板内容
        new_clipboard_text = pyperclip.paste()
        # 如果内容与上一次不同，才进行打印和匹配
        if new_clipboard_text != previous_clipboard_text:
            # 对剪贴板内容进行模糊匹配并返回最后一个答案
            answers = find_last_answer(csv_file, new_clipboard_text)
            result_label.config(text=new_clipboard_text+"\n"+"答案:\n" + "\n".join(answers))
            # 更新上一个剪贴板内容为当前内容
            previous_clipboard_text = new_clipboard_text
        # 每隔一段时间检查剪贴板内容变化
        root.after(1000, update_result)

    root = tk.Tk()
    root.title("助手")
    # 设置窗口一直置顶
    root.attributes("-topmost", True)

    root.geometry("200x200")
    result_label = tk.Label(root, text="")
    result_label.pack()

    update_result()

    root.mainloop()


if __name__ == "__main__":
    csv_file = "output.csv"  # 修改为你的 CSV 文件路径
    get_latest_clipboard_text(csv_file)
