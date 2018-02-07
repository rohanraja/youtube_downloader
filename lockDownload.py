from redisutils import redis
import os



def processExists(process_id):
    try:
        if process_id == "-1":
            return False

        os.kill(int(process_id), 0)
        return True
    except OSError:
        return False

def checkIfLocked(yid):
    key = yid

    try:
        pid = redis.get(key)

        if processExists(pid):
            return True

        return False
    except:

        return False

def lockYid(yid):
    key = yid
    val = os.getpid()
    redis.set(key, val)

def unlockYid(yid):
    key = yid
    redis.set(key, "-1")
