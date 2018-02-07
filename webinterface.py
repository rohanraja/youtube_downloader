__author__ = 'rohanraja'

import Youlink
import jobsmanager

def reDownload(youid):

    youlink = Youlink.getYoulinkFromId(youid)

    job = jobsmanager.DownloadJob()
    job.addDownloadJob(youlink)

def stopDownload(youid):

    jobsmanager.cancelDownload(youid)

def deleteVideo(youid):

    youlink = Youlink.getYoulinkFromId(youid)

    youlink.delete()

