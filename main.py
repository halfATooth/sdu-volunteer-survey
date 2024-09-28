import watchqq
import time

# 预设答案
answer = {
  '姓名': 'xxx',
  '学号': '202100300xxx',
  '电话': '15812345678',
  '手机': '15812345678',
  '联系方式': '15812345678',
  '班级': 'xxxx21.x',
  '性别': '男',
}

# 指定屏幕监听区域，不清楚可以使用qq截图工具看一下
# 左上角坐标
x1 = 10
y1 = 50
# 右下角坐标
x2 = 1690
y2 = 780

# 监听屏幕轮询的时间间隔（秒）
interval = 2

# 监听的持续时间（秒）
duration = 180

# 同一个问卷链接的提交次数
submit_times = 1

# 从运行到开始监听的等待时间（秒）
wait_time = 5

# 启动程序
time.sleep(wait_time)
watchqq.launch(answer=answer, x1=x1, y1=y1, x2=x2, y2=y2, interval=interval, duration=duration, submit_times=submit_times)
