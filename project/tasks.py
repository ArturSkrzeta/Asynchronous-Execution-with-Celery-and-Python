
from celery import Celery
from job_scraper import main

celery = Celery('tasks', broker='redis://localhost:6379/0')

@celery.task
def task(search_phrase):
    main(search_phrase)
    return 'done for a phrase'
