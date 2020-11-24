import requests
from bs4 import BeautifulSoup
from common import *

response = requests.get("http://www.nmc.cn/publish/forecast/ABJ/beijing.html")
response.encoding="utf-8"
content  = response.text

    
def parse_weathers(content):
    soup = BeautifulSoup(content, "html.parser")
    items = soup.find_all(class_="weatherWrap")[:]
    dates = soup.select(".weatherWrap .date")[:]
    climates = soup.select(".weatherWrap .desc")[:]
    temper_array1 = soup.select(".weatherWrap .tmp_lte_-1")[:]
    temper_array2 = soup.select(".weatherWrap .tmp_lte_10")[:]
    temper_array2.extend(soup.select(".weatherWrap .tmp_lte_4")[:])
    weathers =[]
    for i in range(3):
        entry = {}
        item = items[i]
        for sub_item in dates:
            if item in sub_item.parents:
                entry['date'] = sub_item.contents[0].strip()
        for sub_item in temper_array1:
            if item in sub_item.parents:
                entry['temp2'] = sub_item.string.strip()
        for sub_item in temper_array2:
            if item in sub_item.parents:
                entry['temp1'] = sub_item.string.strip()
        weathers.append(entry)
    return weathers
    

weathers = parse_weathers(content)
weather_str=""
for weather in weathers:
    date = weather['date']
    temp1 = weather.get('temp1',"未知").strip()
    temp2 = weather.get('temp2',"未知").strip()
    value = "日期：{0}  白天气温：{1}  夜晚气温：{2}\n ".format (date,temp1,temp2)
    weather_str+=value


send_emali(weather_str,"feipeixuan@163.com")
send_emali(weather_str,"15210217527@163.com")
    
    