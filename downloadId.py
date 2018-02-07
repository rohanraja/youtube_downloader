from dloadWorker import enqueueDownload, download_Youvideo
from persistance import getYoulinkById

import sys

idd = sys.argv[1]
ylink = getYoulinkById(idd)
download_Youvideo(ylink.url)
