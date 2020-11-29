from .crawler import *


content = get_content()
parse_weathers_hours(content)
weathers = parse_weathers_days(content)
weather_str=""
for weather in weathers:
    date = weather['date']
    temp1 = weather.get('temp1',"未知").strip()
    temp2 = weather.get('temp2',"未知").strip()
    value = "日期：{0}  白天气温：{1}  夜晚气温：{2}\n ".format (date,temp1,temp2)
    weather_str+=value

send_emali(weather_str,"feipeixuan@163.com")
send_emali(weather_str,"15210217527@163.com")