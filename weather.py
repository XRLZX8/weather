# -*- coding: utf-8 -*-

# @project :weather
# @File    : weather.py
# @Date    : 2020-12-01-12
# @Author  : XRL
'''
http://www.weather.com.cn/weather/101190101.shtml
'''

from lxml import etree
import requests
import itchat#GG喽
import time
import ast
import datetime

#城市名转城市代码
def cityname_to_code():

    with open('全国城市对应代码.txt','r',encoding='utf8')as f:
        data = f.read()
        data = ast.literal_eval(data)
    cityname = input("请输入城市名：")
    try:
        if data[cityname]:
            citycode = data[cityname]
            return int(citycode)
        else:
            print('城市名错误,请重新输入')
            cityname_to_code()
    except KeyError:
        print('城市名输入错误，请重输')
        cityname_to_code()

#根据代码获取天气信息
def get_weatherdata(citycode):
    url = 'http://www.weather.com.cn/weather/{}.shtml'.format(citycode)
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
        'Connection':'keep-alive',
        'Content-Encoding':'gzip',
        'Content-Type':'text/html'
    }
    res = requests.get(url=url,headers=headers)
    res.encoding = 'utf8'
    html = etree.HTML(res.text)

    day = html.xpath('//ul/li/h1/text()') #日期
    weather = html.xpath('//ul/li/p[@class="wea"]/text()')#天气
    tem_top = html.xpath('//ul/li/p[@class="tem"]/span/text()')#最高温度
    tem_bot = html.xpath('//ul/li/p[@class="tem"]/i/text()')#最低温度
    wind_direction = html.xpath('//ul/li/p[@class="win"]/em/span/@title')#方向，两种
    wind_power = html.xpath('//ul/li/p[@class="win"]/i/text()')#风力

    if len(tem_top) == 6:
        tem_top.insert(0, '无')

    if len(wind_direction) == 13:
        wind_direction.insert(0, '')

    weather_info =[]
    for i in range(0,7):
        weather_temp = []
        weather_temp.append(day[i])
        weather_temp.append(weather[i])
        weather_temp.append(tem_top[i])
        weather_temp.append(tem_bot[i])
        weather_temp.append(wind_direction[2*i])
        weather_temp.append(wind_direction[2*i+1])
        weather_temp.append(wind_power[i])

        weather_info.append(weather_temp)

    return weather_info

#展示天气信息
def show_weather(weather_info,cityname):
    month = datetime.datetime.now().month
    print('\n')
    print(str(month)+'月'+weather_info[0][0] + '天气：' + weather_info[0][1] + '，最高/最低温度：' + weather_info[0][2] + '/' + weather_info[0][3] + '，风向：' + weather_info[0][4] + '-' + weather_info[0][5] + '，风力：' + weather_info[0][6] + '\n')
    print('未来6天天气'+'\n')
    for i in range(1,6):
        print(str(month)+'月'+weather_info[i][0]+'天气：'+weather_info[i][1]+'，最高/最低温度：'+weather_info[i][2]+'/'+weather_info[i][3]+'，风向：'+weather_info[i][4]+'-'+weather_info[i][5]+'，风力：'+weather_info[i][6])
    time.sleep(10)

def main():
    citycode = cityname_to_code()
    weather_info = get_weatherdata(citycode)
    show_weather(weather_info)

if __name__ == '__main__':
    main()