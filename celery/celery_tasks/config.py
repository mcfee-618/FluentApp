BROKER_URL  = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1' 

#定时任务
CELERYBEAT_SCHEDULE = {
    'send_mail': {
        "task": "celery_tasks.tasks.send_weather_email",
        "schedule": timedelta(seconds=5),  #每5秒执行一下receive_mail函数
        "args": (),  #参数
    },
}