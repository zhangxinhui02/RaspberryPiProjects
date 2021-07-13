import requests
import time

path = '/home/pi/image.jpg'
url = 'https://www.bilibili.com/'
#最终的url样式示例：https://s0.wordpress.com/mshots/v1/http://www.baidu.com?w=600&h=450
api_url = 'https://s0.wordpress.com/mshots/v1/'
#获取的图片的长宽
width = 600
height = 450
#每次获取的间隔时间(秒)
time_s = 30

final_url = api_url + url + '?w=' + str(width) +'&h=' + str(height)

def get_image():
    try:
        r = requests.get(final_url)
        with open(path,'wb') as f:
            f.write(r.content)
            f.close()
    except:
        pass


while True:
    get_image()
    time.sleep(time_s)