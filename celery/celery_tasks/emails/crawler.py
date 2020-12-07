import requests
from bs4 import BeautifulSoup
from .common import *


def get_content():
    response = requests.get("http://www.nmc.cn/publish/forecast/ABJ/beijing.html")
    response.encoding="utf-8"
    content  = response.text
    return content


def parse_weathers_hours(content):
    soup = BeautifulSoup(content, "html.parser")
    divs = soup.select(".hour3")[:3]
    weathers =[]
    for div in divs:
        entry = {}
        items = list(div.children)
        date = items[0].string.strip()
        rain = False if items[2].string.strip()=="-" else True
        temp = items[3].string.strip()
        entry['date'] = date
        entry['temp'] = temp
        entry['rain'] = rain
        weathers.append(entry)
    return weathers

    
def parse_weathers_days(content):
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
    
    
    
