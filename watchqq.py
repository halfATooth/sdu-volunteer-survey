import time
import pyscreenshot as ImageGrab
import cv2
import numpy as np
import pyautogui
import pyperclip
import re
import submit

def get_msg(x, y):
  pyautogui.click(x - 5, y - 5)
  pyautogui.hotkey('ctrl', 'a')
  pyautogui.hotkey('ctrl', 'c')
  # 获取剪切板内容
  return pyperclip.paste()

# 指定截屏区域的坐标（左上角 x、y 和右下角 x、y）
x1, y1, x2, y2 = 10, 50, 1690, 780

def locate_msg_box(img):
  # img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
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
        return x1 + rx2, y1 + ry2
  else:
      print("未检测到矩形")
      return -1, -1

def launch():
  prev_img = None
  for i in range(0, 100):
    time.sleep(2)
    img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    curr_img_array = np.array(img)
    if prev_img is not None:
        difference = np.sum(np.abs(curr_img_array - prev_img))
        if difference > 100000:
            print(f"图像有变化，diff={difference}")
            x, y = locate_msg_box(img)
            if x > 0:
              msg = get_msg(x, y)
              urls = re.findall(r'https?://[^#\s\u4e00-\u9fa5，。！？；：“”‘’【】（）、《》]+', msg)
              if len(urls) > 0:
                print(urls[0])
                submit.submit(url=urls[0])
            break
        else:
            print("图像无变化")
    prev_img = curr_img_array.copy()

time.sleep(5)
launch()
