from celery_tasks.app import app

@app.task
def add(x, y):
    return x + y