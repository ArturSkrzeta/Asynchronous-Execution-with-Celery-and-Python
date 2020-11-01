from tasks import task
from time import sleep
p_list = ['Big Data','Data Analyst','Data Engineer']

for p in p_list:
    task.delay(p)
    sleep(10)


    # celery -A tasks worker -l info -P gevent
# cd Documents\env\myenv\Scripts
