from selenium import webdriver
import random  # 用于产生随机数
import time  # 用于延时

# 准备工作
option = webdriver.ChromeOptions()
option.add_argument('headless')
url = 'http://exam.sdsafeschool.gov.cn:9001/#/do?id=244&type=1'  # 此处为你要填写的问卷网 问卷的地址
num = 200  # 设置提交问卷次数

username = "370725200107051218"
password = "!Ll010705"

# import os
# import requests
# from urllib.parse import urljoin
# from PIL import Image
# from io import BytesIO
# def download_images(img_url, save_folder):
#     # 发送GET请求获取网页内容
#     if img_url:
#         img_url = urljoin(url, img_url)  # 处理相对路径
#         img_name = os.path.basename(username)
#         img_path = os.path.join(save_folder, img_name)
#
#         # 发送GET请求下载图片
#         img_response = requests.get(img_url)
#         img = Image.open(BytesIO(img_response.content))
#
#         # 保存图片为jpg格式
#         img_path_jpg = img_path if img_path.lower().endswith('.jpg') else img_path + '.jpg'
#         img.save(img_path_jpg, 'JPEG')
#         print(f"Downloaded: {img_name} - Saved as: {img_path}")
# 主要程序
for times in range(num):
    # 打开网页
    driver = webdriver.Chrome()  # 此处使用chromedriver解压在python的scripts文件夹下的方法
    driver.get(url)  # 获取问卷信息
    print(driver.page_source)
    break
    # 打印页面html
    questions = driver.find_elements_by_class_name('el-input__inner')
    # 打印questions中的html
    # print(questions.get_attribute('outerHTML'))

    # #便利每个问题  index为（从0开始） 题目序号 第一题index=0
    for index, answers in enumerate(questions):
        if index == 0:
            answers.send_keys("曲阜师范大学")
        elif index == 1:
            answers.send_keys(username)
        elif index == 2:
            answers.send_keys(password)
        else:
            img_elements = driver.find_elements_by_tag_name('img')
            # 提取每个图像的src属性
            image_urls = [img.get_attribute('src') for img in img_elements]
            print(image_urls[1])
            target_url = image_urls[1]

            # 替换为您要保存图片的文件夹路径
            save_folder = "downloaded_images"

            # 下载网页中的所有图片
            download_images(target_url, save_folder)

# if answers.find_element_by_css_selector('.el-radio__input'):
#     # 所有问卷问题选项
#     answer = answers.find_elements_by_css_selector('.icheckbox_div')
#     # 填空选项，并填入相关内容
#     if not answer:
#         blank_potion = answers.find_element_by_css_selector('.blank.option')
#         blank_potion.send_keys('无') #此处 “无” 为填写信息
#         continue
#     #根据问卷的题目规定和预期结果  例如：1，2，4，5，6，7，8 为单选
#     # 单选题处理
#     if index == 0 or index == 7 :
#         choose_ans = answer[random.randint(0, 2)] #在前三个选项中随机选择一个
#         choose_ans.click() #相当于点击事件
#         time.sleep(random.randint(0, 1)) #随机一个延时 以免操作过快 影响问卷的质量
#
#     elif index==3:
#         choose_ans = answer[random.randint(0, 3)]
#         choose_ans.click()
#         time.sleep(random.randint(0, 1))
#
#     elif index == 5 or index == 6 :
#         choose_ans = answer[random.randint(0, 2)]
#         choose_ans.click()
#         time.sleep(random.randint(0, 1))
#
#     elif index == 1 :
#         choose_ans = answer[random.randint(0, 3)]
#         choose_ans.click()
#         time.sleep(random.randint(0, 1))
#     elif index == 4 :
#         choose_ans = answer[random.randint(0, 2)]
#         choose_ans.click()
#         time.sleep(random.randint(0, 1))
#
#     # 多选题处理
#     #四选二模式   该思想可用于互斥项
#     elif index ==2:
#          choose_ans = answer[random.randint(0, 1)]#前两个里面选一个
#          choose_ans.click()
#          time.sleep(random.randint(0, 1))
#          choose_ans = answer[random.randint(2, 3)]#后两个里选一个 可随机应变
#          choose_ans.click()
#          time.sleep(random.randint(0, 1))
#
#     #随机多选 存在缺陷
#     elif index ==9:
#         for i in range(1, random.randint(3, 4)): #随机选则两个或三个   或一个！
#             choose_ans = answer[random.randint(0, 3)]
#             choose_ans.click()
#             time.sleep(random.randint(0, 1))
# 		#分析 当随机选择三个时，有可能三个选项随机数中有两个相同
# 		#这时相当于点击两次 没有做选则 所以结果只剩一个
# 		#同理 当随机选则两个时，可能存在不做选择的情况 若为必填题 则不能提交
#
# 			#改进 仍有不足 不会出现偶数个选择项
#     elif index == 8:
#         for i in range(1,8):
#             choose_ans = answer[random.randint(0, 6)]
#             choose_ans.click()
#             time.sleep(random.randint(0, 1))
#           #同上理 此时选项个数为 1或3或5或7
#
# subumit_button = driver.find_element_by_css_selector('#next_button') #获取提交按钮
# #每个问卷网的提交按钮的获取不同 该方法为 问卷网 问卷提交按钮获取方法
# subumit_button.click() #点击提交事件
# print('已经为您提交了{}次问卷'.format(int(times) + int(1)))
# time.sleep(4)  # 延迟问卷结果提交时间，以免间隔时间太短而无法提交
# driver.quit()# 退出 关闭网页
