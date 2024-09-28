import time
import pyscreenshot as ImageGrab
import cv2
import numpy as np
import pyautogui
import pyperclip
import re
import submit

# 指定截屏区域的坐标（左上角 x、y 和右下角 x、y）
# x1, y1, x2, y2 = 10, 50, 1690, 780

# 通过模拟键鼠输入，获取指定消息框里的内容
def get_msg(x, y):
  pyautogui.click(x - 5, y - 5)
  pyautogui.hotkey('ctrl', 'a')
  pyautogui.hotkey('ctrl', 'c')
  # 获取剪切板内容
  return pyperclip.paste()

# 定位最新的消息框的内容
def locate_msg_box(img):
  # 灰度
  gray_img = img.convert('L')
  # 二值化
  _, binary_img = cv2.threshold(np.array(gray_img), 20, 255, cv2.THRESH_BINARY)
  # 将 PIL 图像转换为 OpenCV 格式
  cv_img = binary_img
  cv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)
  # 边缘检测
  edges = cv2.Canny(cv_img, 50, 150)
  # 轮廓检测
  contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  bottommost_rectangle = None
  bottommost_y = 0
  for contour in contours:
      x, y, w, h = cv2.boundingRect(contour)
      if y + h > bottommost_y:
          bottommost_y = y + h
          bottommost_rectangle = (x, y, x + w, y + h)
  if bottommost_rectangle:
        _, _, rx2, ry2 = bottommost_rectangle
        return rx2, ry2
  else:
      print("未检测到矩形")
      return -1, -1

# interval: 轮询的时间间隔，单位：秒
# duration：持续时间，单位：秒
def launch(answer, x1=0, y1=0, x2=1, y2=1, interval=2, duration=180, submit_times=1):
  prev_img = None
  for i in range(0, duration // interval):
    time.sleep(interval)
    # 屏幕指定区域截图，比较两帧是否发生变化
    img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    gray_img = img.convert('L')
    _, curr_img = cv2.threshold(np.array(gray_img), 20, 255, cv2.THRESH_BINARY)
    if prev_img is not None:
        difference = np.sum(np.abs(curr_img - prev_img))
        # 允许一定误差，若无变化，一般diff为0; 若有变化，diff约为30M;
        if difference > 100000:
            print(f"图像有变化，diff={difference}")
            # 从下向上进行矩形检测，定位最新的消息框的位置
            x, y = locate_msg_box(img)
            x = x + x1
            y = y + y1
            if x > 0:
              # 获得消息框的内容
              msg = get_msg(x, y)
              # 从消息中提取网址
              urls = re.findall(r'https?://[^#\s\u4e00-\u9fa5，。！？；：“”‘’【】（）、《》]+', msg)
              if len(urls) > 0:
                print(urls[0])
                # 自动填写预设答案并提交
                submit.submit(answer=answer, url=urls[0], t=submit_times)
            break
        else:
            print("图像无变化")
    prev_img = curr_img.copy()

# 启动程序后等待5秒
# time.sleep(5)
# 启动程序，每隔1秒轮询
# launch(x1=10, y1=50, x2=1690, y2=780, interval=1)
