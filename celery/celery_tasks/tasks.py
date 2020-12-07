from .app import app
import email

@app.task
def send_weather_email():
    content  = email.get_content()
    weathers = email.parse_weathers_hours(content) 
    weather_str=""
    for weather in weathers:
        date = weather['date']
        temp = weather.get('temp',"未知").strip()
        rain = weather.get('rain')
        rain = "有" if rain else "无"
        value = "时间：{0}  气温：{1}  有无降雨：{2}\n ".format (date,temp,rain)
        weather_str+=value
    
    send_emali(weather_str,"feipeixuan@163.com")
    send_emali(weather_str,"15210217527@163.com")
    
