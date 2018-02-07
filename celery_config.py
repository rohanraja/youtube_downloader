from celery import Celery
import config

redis_broker = "redis://%s:6379/0"%config.getRedisIP()

app = Celery('dloadWorker', broker=redis_broker, include=['dloadWorker', 'processUrl'])
# app2 = Celery('processUrl', broker='redis://localhost:6379/0', include=['processUrl'])
