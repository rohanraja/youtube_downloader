from celery import Celery

app = Celery('dloadWorker', broker='redis://localhost:6379/0', include=['dloadWorker', 'processUrl'])
# app2 = Celery('processUrl', broker='redis://localhost:6379/0', include=['processUrl'])
