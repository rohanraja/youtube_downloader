from celery_config import app
import config
import youtube_dl
import os
from persistance import *
from dloadWorker import enqueueDownload
from categorizer import moveMusicFile
import urllib.request, urllib.parse, urllib.error

@app.task
def processUrl(url, title = ''):

    url = urllib.parse.unquote_plus(url)
    title = urllib.parse.unquote_plus(title)
    print("Processing URL %s" % url)
    print("Processing TITLE %s" % title)
    done = checkIfAlreadyDone(url)
    if done == True:
        print("Already Done")
        if checkIfUnfinished(url):
            enqueueDownload(url)
            print("STILL Enqueued For Download")
        return

    saveLink(url, title)
    enqueueDownload(url)
    print("Enqueued For Download")


@app.task
def processVLCUrl(url, cat):

    print("Processing VLC URL %s for cat: %s" % (url, cat))
    hdd = "/Users/rraja/mount"

    if cat == "music":
        folder = "youMusic"

    if cat == "pon":
        folder = "MacStuff/youpon"

    cmd = "mv \"%s\" \"%s/%s\"" % (url, hdd, folder)
    print("RUNNING CMD: %s" % cmd)
    os.system(cmd)

    print("DONE MOVING")

@app.task
def checkMusicFile(url):
    try:
        print("Processing %s" % url)
        moveMusicFile(url)
    except Exception as e:
        print("Some Error %s" % e)

from mp3convert import convertToMp3, outFol

@app.task
def convertMp3(url):
    try:
        print("Processing %s" % url)
        convertToMp3(url, outFol)
    except Exception as e:
        print("Some Error %s" % e)

