from celery import Celery
from .tasks import *

app = Celery('tasks')
app.config_from_object("celery_tasks.config")
app.autodiscover_tasks(['celery_tasks.tasks'])
app.conf.timezone ='Asia/Shanghai'



