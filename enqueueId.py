from dloadWorker import enqueueDownload
from persistance import getYoulinkById

import sys

idd = sys.argv[1]
ylink = getYoulinkById(idd)
enqueueDownload(ylink.url)
