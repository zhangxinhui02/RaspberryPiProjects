#自动窗帘程序   AutomaticCurain
#Reedit by zhangxinhui02
#2021.7.6

import PCF8591 as ADC
import RPi.GPIO as GPIO
import time


makerobo_motorPin = (29,31,33,35)     # 步进电机管脚PIN
makerobo_rolePerMinute =15            # 每分钟转数
makerobo_stepsPerRevolution = 2048    # 每转一圈的步数
makerobo_stepSpeed = (60/makerobo_rolePerMinute)/makerobo_stepsPerRevolution  # 每一步所用的时间

# 初始化设置
def makerobo_setup():
    GPIO.setmode(GPIO.BOARD)  # 将GPIO模式设置为BOARD编号
    GPIO.setwarnings(False) # 忽略警告
    for i in makerobo_motorPin:
        GPIO.setup(i, GPIO.OUT) # 设置步进电机的所有管脚为输出模式
    ADC.setup(0x48)      # 设置PCF8591模块地址

# 步进电机旋转
def makerobo_rotary(clb_direction):
    if(clb_direction == 'c'):
        for j in range(4):
            for i in range(4):
                GPIO.output(makerobo_motorPin[i],0x99>>j & (0x08>>i))
            time.sleep(makerobo_stepSpeed)

    elif(clb_direction == 'a'):
        for j in range(4):
            for i in range(4):
                GPIO.output(makerobo_motorPin[i],0x99<<j & (0x80>>i))
            time.sleep(makerobo_stepSpeed)

# 循环函数
def makerobo_loop():
    makerobo_status = 1 # 状态值
    while True:
        clb_direction = input('Makerobo select motor direction a=anticlockwise, c=clockwise: ')
        if(clb_direction == 'c'):
            print('Makerobo motor running clockwise\n')       # 顺时针旋转
            break
        elif(clb_direction == 'a'):
            print('Makerobo motor running anti-clockwise\n')  # 逆时针旋转
            break
        else:
            print('Makerobo input error, please try again!') # 输入错误，再次输入
    while True:
        makerobo_rotary(clb_direction)       # 让步进电机旋转
        print ('Photoresistor Value: ', ADC.read(1)) # 读取AIN1的值，获取光敏模拟量值	

# 释放资源
def destroy():
    for i in makerobo_motorPin:
        GPIO.output(i, GPIO.LOW) # 设置步进电机的所有管脚为输出模式
    #GPIO.cleanup() # 释放资源




    # 程序入口
if __name__ == '__main__':
    makerobo_setup()   # 初始化设置函数
    try:
        makerobo_loop()  # 循环函数
    except KeyboardInterrupt:   # 当按下Ctrl+C时，将执行destroy()子程序。
        destroy()  # 资源释放s