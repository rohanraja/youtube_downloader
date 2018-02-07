from persistance import *
from dloadWorker import enqueueDownload


ylinks = getUnfinished()

idd = 0
import sys

if len(sys.argv) > 1:
    idd = sys.argv[1]

for ylink in ylinks:
    if int(ylink.id) >= int(idd):
        print("Enqueing Youlink with Id %s and Path %s" % (ylink.id, ylink.path))
        enqueueDownload(ylink.url, ylink.category)
