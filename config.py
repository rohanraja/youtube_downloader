__author__ = 'rohanraja'

import os

_BASE_DIR = "/Volumes/Seagate Backup Plus Drive/MacStuff/asdyoudl"
_BASE_DIR_LOCAL = "/Volumes/MbpStuff/youdl"

def getBaseDir():
    base = ''
    if os.getenv("YOUDL_PATH") is not None:
        return os.getenv("YOUDL_PATH")

    if os.path.exists(_BASE_DIR) :
        base = _BASE_DIR
    else:
        base = _BASE_DIR_LOCAL

    return base

def get_VID_DIR():

    base = getBaseDir()

    VIDEO_DOWNLOAD_DIR = os.path.join(base,"youvideos")
    THUMBNAILS_DIR     = os.path.join(base,"thumbs")

    return VIDEO_DOWNLOAD_DIR, THUMBNAILS_DIR



def getDBDir():
    base = getBaseDir()
    DB_DIR = os.path.join(base,"db")
    DB_DIR = os.path.join(DB_DIR,"youlinks.db")
    return DB_DIR

def getRedisIP():
    if os.getenv("YOUDL_REDIS") is not None:
        return os.getenv("YOUDL_REDIS")
    return "localhost"


VIDEO_DOWNLOAD_DIR = os.path.join(_BASE_DIR,"youvideos")
THUMBNAILS_DIR     = os.path.join(_BASE_DIR,"thumbs")


THUMB_URL_PATH = "/thumbs"

HTTPS_LISTEN_PORT = 3011
HTTP_LISTEN_PORT = 3009

# CERT_FILE = '/usr/local/etc/nginx/ssl/nginx.crt'
# KEY_FILE = '/usr/local/etc/nginx/ssl/nginx.key'
CERT_FILE = 'certs/nginx.crt'
KEY_FILE = 'certs/nginx.key'

VIDEO_SERVER_URL = "http://localhost:8989/"

NUM_RETRIES = 3

# DOWNLOAD_VIDEO_PROXY = ''
# DOWNLOAD_VIDEO_PROXY_PN = ''
DOWNLOAD_VIDEO_PROXY = ''# 'http://10.3.100.207:8080'
DOWNLOAD_VIDEO_PROXY_PN = 'http://localhost:8118'
