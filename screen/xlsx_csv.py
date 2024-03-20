import pandas as pd
import os

def convert_xlsx_to_csv(input_file, output_file):
    try:
        # 读取 Excel 文件
        df = pd.read_excel(input_file)
        # 将数据保存为 CSV 文件（如果文件存在，则追加数据）
        mode = 'a' if os.path.exists(output_file) else 'w'
        df.to_csv(output_file, index=False, mode=mode, header=not os.path.exists(output_file))
        print("Conversion successful!")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    input_file = "input.xlsx"
    output_file = "output.csv"
    convert_xlsx_to_csv(input_file, output_file)
