# 两次防抖判断的间隔时间
Interval = 0.5
# 定义超时阈值
Timeout = 60
# 检测引脚
PIN = 11

# 总开门秒数
OpenSecs = 0
# 总开门次数
OpenTimes = 0
# 超时秒数
TimeoutSecs = 0
# 超时次数
TimeoutTimes = 0

from RPi import GPIO
from datetime import datetime
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN, GPIO.IN)


def check_refresh():
    """0点刷新"""
    if datetime.hour == 0 and datetime.minute == 0 and datetime.second <= Interval + 1:
        global OpenSecs, OpenTimes, TimeoutSecs, TimeoutTimes
        OpenSecs = 0
        OpenTimes = 0
        TimeoutSecs = 0
        TimeoutTimes = 0


def get_state():
    """获取门的状态"""
    if GPIO.input(PIN):
        time.sleep(Interval)
        if GPIO.input(PIN):
            return True
        else:
            return False
    else:
        return False


def update_database():
    """更新数据库"""
    # 在这里编写代码以将数据写入数据库
    # 各个变量对应的意义见文件开头
    pass


def main():
    """主函数"""
    open_flag = False
    open_time = datetime.now()
    close_time = datetime.now()
    open_sec = 0
    global OpenSecs, OpenTimes, TimeoutSecs, TimeoutTimes
    while True:
        if get_state():
            if open_flag is False:
                open_time = datetime.now()
                open_flag = True
        else:
            if open_flag is True:
                close_time = datetime.now()
                open_flag = False
                open_sec = (close_time - open_time).seconds

                OpenSecs += open_sec
                OpenTimes += 1
                if open_sec - Timeout > 0:
                    TimeoutSecs += open_sec - Timeout
                    TimeoutTimes += 1
        check_refresh()
        update_database()


if __name__ == '__main__':
    main()
