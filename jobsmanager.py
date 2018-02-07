__author__ = 'rohanraja'

from multiprocessing.pool import ThreadPool
from multiprocessing import Queue
import Youlink
import tornado
from multiprocessing import Process, Queue


poolWorkers = ThreadPool(10)

ALL_PROGRESSES = []
JOBCOUNT = 0
ALLHANDLERS = {}
NEWDOWNLOADLISTENERS = []
JOBS = {}

PROCESSES = []

ALLQUEUES = {}

from timer import Timer

def addListener(jobid, listener):

    handlerList = ALLHANDLERS.setdefault(jobid, [])
    handlerList.append(listener)

def delListener(listener):

    for k in list(ALLHANDLERS.keys()):

        if(listener in ALLHANDLERS[k]):
            ALLHANDLERS[k].remove(listener)


class DownloadJob():

    jobid = None
    youlink = None

    def onDlStatusUpdate(self, stats):


        q = ALLQUEUES[self.jobid]
        q.put(stats)

        #ioloop = tornado.ioloop.IOLoop.instance()

        #ioloop.add_callback(lambda: self.sendDataMessage(stats, self.jobid))
        pass


    def sendDataMessage(self, message, jobid):

        y = Youlink.getYoulinkFromId(jobid).updateDownloadDetails(message)

        message = y.to_json()

        for updater in ALLHANDLERS[jobid]:
            updater(message)


    def statListener(self):

        ioloop = tornado.ioloop.IOLoop.instance()
        q = ALLQUEUES[self.jobid]
        while True:
            stats = q.get()
            ioloop.add_callback(lambda: self.sendDataMessage(stats, self.jobid))

    def addDownloadJob(self,youlink, msgWriter = None):



        self.jobid = youlink.getId()

        if self.jobid in JOBS:
            print("Already Downloading")
            return 0

        global JOBCOUNT

        JOBCOUNT += 1

        self.youlink = youlink

        ALLHANDLERS.setdefault(self.jobid, [])

        q = Queue()
        ALLQUEUES[self.jobid] = q

        target = lambda : youlink.startDownload(self.onDlStatusUpdate)

        self.p = Process(target=target, args=())
        self.p.start()
        print(self.p.pid)

        p2 = Process(target=youlink.getVideoDetails, args=())
        p2.start()

        poolWorkers.apply_async(self.statListener, (), {})

        JOBS.setdefault(self.jobid, self)

        notifyDownloadListeners(youlink)

        print("Added download job to pool")



def cancelDownload(youid):

    job = JOBS.get(youid)
    job.p.terminate()
    del JOBS[youid]
    print("Cancelled DOWNLOAD")




def notifyDownloadListeners(youlink):

    for listener in NEWDOWNLOADLISTENERS :
        listener(youlink)
