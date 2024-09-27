from selenium import webdriver
import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service

def submit(url='https://www.wenjuan.com/s/UZBZJvp0zJ/', t=1):
  # 预设答案
  answer = {
    '姓名': '李xx',
    '学号': '202100300xxx',
    '电话': '158xxxxxxxx',
    '手机': 'xxxxxx',
    '联系方式': '158533xxxx',
    '班级': 'xxxx21.x',
    '性别': '男',
  }
  # 自动答题数
  count = 0
  for times in range(t):
      driver = webdriver.Edge(service=Service('./edgedriver/msedgedriver'))
      driver.get(url)
      # 定位所有的问卷问题
      parent_id = 'question-warper'
      parent = driver.find_element(by=By.ID, value=parent_id)
      children = parent.find_elements(by=By.XPATH, value='./*')
      for index in range(1, len(children)+1):
        lable_path = f'./div[{index}]/div[1]/div/div/div/div'
        lable = parent.find_element(by=By.XPATH, value=lable_path).text
        pattern = r"\. (.*)"
        match = re.search(pattern, lable)
        if match:
          lable_content = match.group(1)
          print(lable_content)
          if lable_content in answer:
            element_path = f'./div[{index}]/div[2]/div/div/div/div/textarea'
            element = parent.find_element(by=By.XPATH, value=element_path)
            print(answer[lable_content])
            element.send_keys(answer[lable_content])
            count = count + 1
      if count==len(children):
        submit_btn = driver.find_element(by=By.ID, value='answer-submit-btn')
        submit_btn.click()
        time.sleep(1)
        driver.quit()