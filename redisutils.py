__author__ = 'rohanraja'

import redis as Redis
from redisQueue import RedisQueue

redis = Redis.StrictRedis(host='localhost', port=6379, db=0)

def saveDownloadDetails(youid, dldetails):

    key = "download.%s" % youid

    redis.set(key, dldetails)

def getDownloadDetails(youid):

    key = "download.%s" % youid

    redis.get(key)

def markInfoDownloaded(youid):

    key = "infobool.%s" % youid

    redis.set(key, "true")


def checkInfoDownloaded(youid):

    key = "infobool.%s" % youid

    val = redis.get(key)

    if val == "true" :
        return True
    else:
        return False

def enqueueForDownload(url):

    q = RedisQueue("youlinks")
    q.put(url)
    return "URL Enqueued"
