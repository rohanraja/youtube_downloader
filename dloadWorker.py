from celery_config import app
import config
import youtube_dl
import os
from persistance import *
from lockDownload import *

def downloadDirectly(url, fname=''):
    Oriurl = url
    if url[:2] == "//":
        url = url[2:]
    directory, thumbs = config.get_VID_DIR()
    print("Directly Dloading " , url)
    print(directory)

    cmd = "wget --content-disposition -c -P '%s' '%s'" % (directory, url)

    if fname != '' and fname[0] != '_':
        fname = fname.replace(" ","_")
        cmd = "wget -O '%s/%s.mp4' -c '%s'" % (directory, fname, url)

    outP = os.system(cmd)
    if outP == 0 or outP == "0":
        markFinished(Oriurl)

def _download(url, onProgress = None):

    directory, thumbs = config.get_VID_DIR()
    ylink = getYoulinkByURL(url)

    if checkIfLocked(ylink.id):
        print("Someone already downloading!!")
        return

    lockYid(ylink.id)

    if "youtube.com" not in url:
        downloadDirectly(url, "%s_%s"%(ylink.path, ylink.id))
        unlockYid(ylink.id)
        return

    if "youtube.com/watch?v" not in url:
        print("NOT A VIDEO URL")
        return

    ydl_options = {
        'outtmpl': os.path.join(directory, '%(uploader)s_%(title)s-%(id)s.%(ext)s')
    }

    if "youtube.com" in url:
        ydl_options["proxy"] = config.DOWNLOAD_VIDEO_PROXY #'http://10.3.100.207:8080'
    else:
        ydl_options["proxy"] = config.DOWNLOAD_VIDEO_PROXY_PN #'http://localhost:8118'

    retry = True
    numTries = config.NUM_RETRIES
    while(retry and numTries > 0):
        with youtube_dl.YoutubeDL(ydl_options) as ydl:
            # ydl.add_progress_hook(onProgress)

            try:
                ydl.extract_info(url)
                markFinished(url)

                retry = False

                # self.markDownloadComplete() # ToDo: Check marking on error conditions

            except:

                print("YOUDOWNLOAD Error OCCURED")



            finally:

                print("Downloading Stopped**********")
                unlockYid(ylink.id)
                # if(self.status != "Finished"):
                #     retry = True
                #
                #     print "Retrying #%d ********###############************" % (config.NUM_RETRIES - numTries + 1)
                #     time.sleep(5)
                #
                # else:
                #     retry = False
                #     
                #     import subprocess
                #     cmd = "curl --noproxy 127.0.0.1 http://127.0.0.1:3009/newlink" 
                #     subprocess.call(cmd, shell=True)  
                #     print "Calling download all videos to server!"

                numTries -= 1


@app.task
def download_Youvideo(url):

    print("Downloading Video")
    markProcessing(url)
    _download(url)


def enqueueDownload(url):
    download_Youvideo.apply_async(args=[url], queue="youdownload")

if __name__ == "__main__":
    #download_Youvideo.delay("https://www.youtube.com/watch?v=zRS9odTRHEs")
    # download_Youvideo.delay("//cdnf-mobile.youjizz.com/videos/b/2/b/5/0/b2b5084217057fbaeceaf23a7c4cc3b81432307102-480-270-399-h264.mp4?ri=5000000&rs=1620&ttl=1490004238&hash=bcd752d89c7a2c50519ad3c83dd45d36")
    downloadDirectly("//cdnf-mobile.youjizz.com/videos/b/2/b/5/0/b2b5084217057fbaeceaf23a7c4cc3b81432307102-480-270-399-h264.mp4?ri=5000000&rs=1620&ttl=1490004238&hash=bcd752d89c7a2c50519ad3c83dd45d36")
