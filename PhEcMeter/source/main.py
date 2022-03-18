# 电压值
REF = 5.08
# pH模拟输入引脚
AIN0 = 0
# 电导率模拟输入引脚
AIN1 = 1
# 每两次取样的时间间隔
CollectInterval = 0.02
# 单次执行的取样次数
CollectTimes = 40
# 取样若干次的列表
VoltageArray = []

import time
import sys
sys.path.append('./modules/')

# from modules.DFRobot_ADS1115 import ADS1115
from modules.ADS1263 import ADS1263
from modules.DFRobot_EC import DFRobot_EC
from modules.DFRobot_PH import DFRobot_PH
from modules.DS18B20 import read_temp

ads = ADS1263()
ec = DFRobot_EC()
ph = DFRobot_PH()

ec.begin()
ph.begin()


def _get_adc_value(pin):
    """获取一次电压值"""
    if ads.ADS1263_init_ADC1('ADS1263_7200SPS') == -1:
        exit()
    ads.ADS1263_SetMode(0)
    value = ads.ADS1263_GetAll()  # get ADC value
    if value[pin] >> 31 == 1:
        result = (REF * 2 - value[pin] * REF / 0x80000000) * -1
    else:
        result = (value[pin] * REF / 0x7fffffff)  # 32bit
    ads.ADS1263_Exit()
    return result


def _get_average_list():
    """获取列表均值"""
    if CollectTimes <= 0:
        print("Error number for the array to averaging!/n")
        return -1
    elif CollectTimes <= 5:   # 小于等于5，取均值
        return sum(VoltageArray) / CollectTimes
    else:   # 大于5，除去最大最小值，取均值
        VoltageArray.pop(max(VoltageArray))
        VoltageArray.pop(min(VoltageArray))
        return sum(VoltageArray) / len(VoltageArray)


while True:
    # Read your temperature sensor to execute temperature compensation
    temperature = read_temp()
    # Get the Digital Value of Analog of selected channel
    # pin0
    VoltageArray = []
    for i in range(CollectTimes):
        VoltageArray.append(_get_adc_value(0))
        time.sleep(CollectInterval)
    adc0 = _get_average_list()
    # pin1
    VoltageArray = []
    for i in range(CollectTimes):
        VoltageArray.append(_get_adc_value(1))
        time.sleep(CollectInterval)
    adc1 = _get_average_list()
    # Convert voltage to EC with temperature compensation
    EC = ec.readEC(adc0, temperature)
    PH = ph.readPH(adc1, temperature)
    print("Temperature:%.1f ^C EC:%.2f ms/cm PH:%.2f " % (temperature, EC, PH))
    time.sleep(1.0)
