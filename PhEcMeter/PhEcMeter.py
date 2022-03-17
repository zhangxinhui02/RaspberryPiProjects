import time
import ADS1263
import RPi.GPIO as GPIO

# 电压值
REF = 5.08
# pH模拟输入引脚
AIN0 = 0
# 电导率模拟输入引脚
AIN1 = 1
# pH系数
k = -5.8887
# pH偏差值
Offset = 21.677
# 电导率最大值
kValue_max = 1
# 电导率最小值
kValue_min = 1
kValue = 1
TempData = 0
# 运放电阻，与硬件电路有关
RES2 = 820.0
# 极片输入电压，与硬件电路相关
ECREF = 200.0
# 每两次取样的时间间隔
CollectInterval = 0.02
# 单次执行的取样次数
CollectTimes = 40
# 取样若干次的列表
VoltageArray = []


def _get_adc_value(pin):
    """获取一次电压值"""
    ADC = ADS1263.ADS1263()
    if ADC.ADS1263_init_ADC1('ADS1263_7200SPS') == -1:
        exit()
    ADC.ADS1263_SetMode(0)
    value = ADC.ADS1263_GetAll()  # get ADC value
    # for i in range(0, 10):
    #     if (ADC_Value[i] >> 31 == 1):
    #         print("ADC1 IN%d = -%lf" % (i, (REF * 2 - ADC_Value[i] * REF / 0x80000000)))
    #     else:
    #         print("ADC1 IN%d = %lf" % (i, (ADC_Value[i] * REF / 0x7fffffff)))  # 32bit
    # print("\33[11A")
    if value[pin] >> 31 == 1:
        result = (REF * 2 - value[pin] * REF / 0x80000000) * -1
    else:
        result = (value[pin] * REF / 0x7fffffff)  # 32bit
    ADC.ADS1263_Exit()
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


def get_ph():
    """获取pH值"""
    for i in range(CollectTimes):
        VoltageArray.append(_get_adc_value(AIN0))
        time.sleep(CollectInterval)
    voltage = _get_average_list()
    ph_value = k * voltage + Offset
    if ph_value <= 0.0:
        ph_value = 0.0
    elif ph_value > 14.0:
        ph_value = 14.0
    return ph_value


def get_ele():
    """获取电导率"""
    global kValue
    for i in range(CollectTimes):
        VoltageArray.append(_get_adc_value(AIN1))
        time.sleep(CollectInterval)
    voltage = _get_average_list()
    EC_voltage = voltage
    rawEC = 1000 * EC_voltage / RES2 / ECREF
    EC_valueTemp = rawEC * kValue
    # / *First
    # Range: (0, 2);
    # Second
    # Range: (2, 20) * /
    if EC_valueTemp > 2.0:
        kValue = kValue_max
    elif EC_valueTemp <= 2.0:
        kValue = kValue_min
    EC_value = rawEC * kValue
    compensationCoefficient = 1.0 + 0.0185 * ((TempData / 10) - 25.0)
    EC_value = EC_value / compensationCoefficient
    if EC_value <= 0:
        EC_value=0
    if EC_value > 20:
        EC_value=20
    return EC_value

get_ph()
get_ele()
