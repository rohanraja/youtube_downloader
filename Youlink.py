

__author__ = 'rohanraja'

from mongoengine import *
import MongoConnection
import youtube_dl
from multiprocessing import Process
import json
import os
import config
import utils
import redisutils
import time

_DOWNLOADING = "DOWNLOADING"

class Youlink(Document):

    url = StringField(max_length=200)
    status = StringField(max_length=20, default="Downloading")             # Inactive, Paused, Downloading, Finished, Error
    filename = StringField(max_length=200)
    filedir = StringField(max_length=200)
    thumburl = StringField(max_length=200)
    thumbUrl = StringField(max_length=200)

    youId = StringField(max_length=200, default="")


    dlDetails = DictField()
    vidinfo = DictField()

    #jobid = StringField(max_length=20)

    title = StringField(max_length=200, default="0")

    def onProgress(self, stats):

        print(stats)


    def _download(self, onProgress):

        directory = os.path.join(config.VIDEO_DOWNLOAD_DIR)

        ydl_options = {
            'outtmpl': os.path.join(directory, '%(uploader)s_%(title)s-%(id)s.%(ext)s'),
            'nocheckcertificate': True,
        }

        if "youtube.com" in self.url:
            ydl_options["proxy"] = config.DOWNLOAD_VIDEO_PROXY #'http://10.3.100.207:8080'
        else:
            ydl_options["proxy"] = config.DOWNLOAD_VIDEO_PROXY_PN #'http://localhost:8118'

        retry = True
        numTries = config.NUM_RETRIES
        while(retry and numTries > 0):
            with youtube_dl.YoutubeDL(ydl_options) as ydl:
                ydl.add_progress_hook(onProgress)



                try:
                    # import pdb; pdb.set_trace()
                    ydl.extract_info(self.url)

                    self.markDownloadComplete() # ToDo: Check marking on error conditions

                except:

                    print("YOUDOWNLOAD Error OCCURED")


                finally:

                    print("Downloading Stopped**********")
                    if(self.status != "Finished"):
                        retry = True

                        print("Retrying #%d ********###############************" % (config.NUM_RETRIES - numTries + 1))
                        time.sleep(5)

                    else:
                        retry = False
                        
                        import subprocess
                        cmd = "curl --noproxy 127.0.0.1 http://127.0.0.1:3009/newlink" 
                        subprocess.call(cmd, shell=True)  
                        print("Calling download all videos to server!")



                    numTries -= 1


    def startDownload(self, onProgress):

        self._download(onProgress)
        print("done")



    def updateDetails(self, vidinfo):

        testVidinfo = vidinfo#{u'upload_date': '20141014', u'extractor': u'youtube', u'height': 720, u'like_count': None, u'duration': 201, u'player_url': None, u'id': u'ARO82lUakMw', u'view_count': 17452677, u'playlist': None, u'title': u'"Stay High" - Tove Lo - Against The Current Cover', u'playlist_index': None, u'dislike_count': None, u'average_rating': 4.83459329605, u'categories': [u'Entertainment'], u'age_limit': 0, u'annotations': None, u'webpage_url_basename': u'watch', u'display_id': u'ARO82lUakMw', u'automatic_captions': {}, u'description': u"SUBSCRIBE! I promise, it's fun :1 http://bit.ly/SubscribeKHS\nGrab this on iTunes here: https://itunes.apple.com/us/album/habits-stay-high-single/id929726828\nCheck out our epic song with Coke Bottles! https://www.youtube.com/watch?v=ZzuRvzsNpTU\n\nAnd check http://kurthugoschneider.com/tour for New York and New Jersey show info!!\n_______________________________\n\nGET IN TOUCH!\n\nKURT SCHNEIDER:\nFacebook: http://www.facebook.com/kurthugoschneider\nTwitter: http://www.twitter.com/kurthschneider\n\nAGAINST THE CURRENT\nYouTube: http://www.youtube.com/AgainstTheCurrentNY\nFacebook: http://www.facebook.com/againstthecurrentband\nTwitter: http://www.twitter.com/ATC_BAND\n\nCHRISSY, DAN, AND WILL\nhttp://www.twitter.com/ChrissyCostanza\nhttp://www.twitter.com/DanielGow\nhttp://www.twitter.com/WillFerri", u'format': u'22 - 1280x720', u'requested_subtitles': None, u'uploader': u'Kurt Hugo Schneider', u'format_id': u'22', u'uploader_id': u'KurtHugoSchneider', u'subtitles': {}, u'thumbnails': [{u'url': u'https://i.ytimg.com/vi/ARO82lUakMw/maxresdefault.jpg', u'id': u'0'}], u'url': u'https://r9---sn-h557sn7y.googlevideo.com/videoplayback?ip=59.164.96.123&upn=_H1jB3crDuU&id=o-AOf2yaeAXNKIYT4mqozs4rSAoYn7snsGGRzJ3MjOxzRd&sparams=dur%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Cratebypass%2Crequiressl%2Csource%2Cupn%2Cexpire&initcwndbps=95000&source=youtube&mm=31&mn=sn-h557sn7y&sver=3&ratebypass=yes&dur=200.039&fexp=9406983%2C9407141%2C9408142%2C9408420%2C9408710%2C9413503%2C9414764%2C9415304%2C9416126&ms=au&mt=1434551329&mv=m&mime=video%2Fmp4&itag=22&key=yt5&ipbits=0&lmt=1415109036535899&signature=9A96860C79D5E9394CDA01786DFF6C180726526E.C2BD9E3BB1D0EFABA7ABE873497CDE2DE7792C90&expire=1434573049&requiressl=yes&pl=20', u'extractor_key': 'Youtube', u'http_headers': {u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'}, u'thumbnail': u'https://i.ytimg.com/vi/ARO82lUakMw/maxresdefault.jpg', u'ext': u'mp4', u'webpage_url': u'https://www.youtube.com/watch?v=ARO82lUakMw', u'formats': [{u'http_headers': {u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'}, u'format': u'nondash-171 - audio only (DASH audio)', u'url': u'https://r9---sn-h557sn7y.googlevideo.com/videoplayback?ip=59.164.96.123&id=o-AOf2yaeAXNKIYT4mqozs4rSAoYn7snsGGRzJ3MjOxzRd&sparams=clen%2Cdur%2Cgir%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Ckeepalive%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Crequiressl%2Csource%2Cupn%2Cexpire&initcwndbps=95000&source=youtube&mm=31&mn=sn-h557sn7y&sver=3&upn=_H1jB3crDuU&dur=199.986&fexp=9406983%2C9407141%2C9408142%2C9408420%2C9408710%2C9413503%2C9414764%2C9415304%2C9416126&ms=au&mt=1434551329&mv=m&mime=audio%2Fwebm&itag=171&key=yt5&ipbits=0&lmt=1413351345760660&signature=AB04E5A6D33B0B6B9BC6C890AE9F3885AF1D4D4C.706B7CBA225813F201BA3865E1DA5E661C8FCAF0&clen=2988367&gir=yes&expire=1434573049&requiressl=yes&keepalive=yes&pl=20&ratebypass=yes', u'vcodec': u'none', u'format_note': u'DASH audio', u'abr': 128, u'player_url': None, u'ext': u'webm', u'preference': -10050, u'format_id': u'nondash-171'}, {u'http_headers': {u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'}, u'container': u'm4a_dash', u'format': u'nondash-140 - audio only (DASH audio)', u'url': u'https://r9---sn-h557sn7y.googlevideo.com/videoplayback?ip=59.164.96.123&id=o-AOf2yaeAXNKIYT4mqozs4rSAoYn7snsGGRzJ3MjOxzRd&sparams=clen%2Cdur%2Cgir%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Ckeepalive%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Crequiressl%2Csource%2Cupn%2Cexpire&initcwndbps=95000&source=youtube&mm=31&mn=sn-h557sn7y&sver=3&upn=_H1jB3crDuU&dur=200.039&fexp=9406983%2C9407141%2C9408142%2C9408420%2C9408710%2C9413503%2C9414764%2C9415304%2C9416126&ms=au&mt=1434551329&mv=m&mime=audio%2Fmp4&itag=140&key=yt5&ipbits=0&lmt=1415087040625265&signature=0DE9FCE5467CCC4B2B6F0575F68DA88488A21462.A1202D9D0842F7DE4ABD5DADB5E37F4F1FA7F155&clen=3212492&gir=yes&expire=1434573049&requiressl=yes&keepalive=yes&pl=20&ratebypass=yes', u'vcodec': u'none', u'format_note': u'DASH audio', u'abr': 128, u'player_url': None, u'ext': u'm4a', u'preference': -10050, u'format_id': u'nondash-140', u'acodec': u'aac'}, {u'http_headers': {u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'}, u'format': u'nondash-160 - 144p (DASH video)', u'url': u'https://r9---sn-h557sn7y.googlevideo.com/videoplayback?ip=59.164.96.123&id=o-AOf2yaeAXNKIYT4mqozs4rSAoYn7snsGGRzJ3MjOxzRd&sparams=clen%2Cdur%2Cgir%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Ckeepalive%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Crequiressl%2Csource%2Cupn%2Cexpire&initcwndbps=95000&source=youtube&mm=31&mn=sn-h557sn7y&sver=3&upn=_H1jB3crDuU&dur=200.033&fexp=9406983%2C9407141%2C9408142%2C9408420%2C9408710%2C9413503%2C9414764%2C9415304%2C9416126&ms=au&mt=1434551329&mv=m&mime=video%2Fmp4&itag=160&key=yt5&ipbits=0&lmt=1415109055383527&signature=8835BCA1D31FF19EC0E3667DBD2D553043BAAD2F.26E19A36361D26D2BFF794144FAB66A30DC3BB45&clen=2732270&gir=yes&expire=1434573049&requiressl=yes&keepalive=yes&pl=20&ratebypass=yes', u'format_note': u'DASH video', u'player_url': None, u'ext': u'mp4', u'preference': -10040, u'format_id': u'nondash-160', u'height': 144, u'acodec': u'none'}, {u'http_headers': {u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'}, u'format': u'nondash-242 - 240p (DASH video)', u'url': u'https://r9---sn-h557sn7y.googlevideo.com/videoplayback?ip=59.164.96.123&id=o-AOf2yaeAXNKIYT4mqozs4rSAoYn7snsGGRzJ3MjOxzRd&sparams=clen%2Cdur%2Cgir%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Ckeepalive%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Crequiressl%2Csource%2Cupn%2Cexpire&initcwndbps=95000&source=youtube&mm=31&mn=sn-h557sn7y&sver=3&upn=_H1jB3crDuU&dur=199.950&fexp=9406983%2C9407141%2C9408142%2C9408420%2C9408710%2C9413503%2C9414764%2C9415304%2C9416126&ms=au&mt=1434551329&mv=m&mime=video%2Fwebm&itag=242&key=yt5&ipbits=0&lmt=1413351369421465&signature=4D941249F3523C8B02B559672351337061AEFEBF.27552588ACAD8D38CACC68C4087F6C275DE0D614&clen=3668805&gir=yes&expire=1434573049&requiressl=yes&keepalive=yes&pl=20&ratebypass=yes', u'format_note': u'DASH video', u'player_url': None, u'ext': u'webm', u'preference': -10040, u'format_id': u'nondash-242', u'height': 240, u'acodec': u'none'}, {u'http_headers': {u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'}, u'format': u'nondash-133 - 240p (DASH video)', u'url': u'https://r9---sn-h557sn7y.googlevideo.com/videoplayback?ip=59.164.96.123&id=o-AOf2yaeAXNKIYT4mqozs4rSAoYn7snsGGRzJ3MjOxzRd&sparams=clen%2Cdur%2Cgir%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Ckeepalive%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Crequiressl%2Csource%2Cupn%2Cexpire&initcwndbps=95000&source=youtube&mm=31&mn=sn-h557sn7y&sver=3&upn=_H1jB3crDuU&dur=199.949&fexp=9406983%2C9407141%2C9408142%2C9408420%2C9408710%2C9413503%2C9414764%2C9415304%2C9416126&ms=au&mt=1434551329&mv=m&mime=video%2Fmp4&itag=133&key=yt5&ipbits=0&lmt=1415109050904308&signature=96B5939A5908D0D4C0981CFA2B5026AF325DA0DB.F674BD07C8EDEBF744F95F014E311EC59724D7ED&clen=6123375&gir=yes&expire=1434573049&requiressl=yes&keepalive=yes&pl=20&ratebypass=yes', u'format_note': u'DASH video', u'player_url': None, u'ext': u'mp4', u'preference': -10040, u'format_id': u'nondash-133', u'height': 240, u'acodec': u'none'}, {u'http_headers': {u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'}, u'format': u'nondash-243 - 360p (DASH video)', u'url': u'https://r9---sn-h557sn7y.googlevideo.com/videoplayback?ip=59.164.96.123&id=o-AOf2yaeAXNKIYT4mqozs4rSAoYn7snsGGRzJ3MjOxzRd&sparams=clen%2Cdur%2Cgir%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Ckeepalive%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Crequiressl%2Csource%2Cupn%2Cexpire&initcwndbps=95000&source=youtube&mm=31&mn=sn-h557sn7y&sver=3&upn=_H1jB3crDuU&dur=199.950&fexp=9406983%2C9407141%2C9408142%2C9408420%2C9408710%2C9413503%2C9414764%2C9415304%2C9416126&ms=au&mt=1434551329&mv=m&mime=video%2Fwebm&itag=243&key=yt5&ipbits=0&lmt=1413351453081018&signature=5F8430C21F73AB7170B8453087A0B4BB57EB83CB.5C5904B74496D7FF4B2865ED2B8779BD33316165&clen=6527455&gir=yes&expire=1434573049&requiressl=yes&keepalive=yes&pl=20&ratebypass=yes', u'format_note': u'DASH video', u'player_url': None, u'ext': u'webm', u'preference': -10040, u'format_id': u'nondash-243', u'height': 360, u'acodec': u'none'}, {u'http_headers': {u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'}, u'format': u'nondash-134 - 360p (DASH video)', u'url': u'https://r9---sn-h557sn7y.googlevideo.com/videoplayback?ip=59.164.96.123&id=o-AOf2yaeAXNKIYT4mqozs4rSAoYn7snsGGRzJ3MjOxzRd&sparams=clen%2Cdur%2Cgir%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Ckeepalive%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Crequiressl%2Csource%2Cupn%2Cexpire&initcwndbps=95000&source=youtube&mm=31&mn=sn-h557sn7y&sver=3&upn=_H1jB3crDuU&dur=199.949&fexp=9406983%2C9407141%2C9408142%2C9408420%2C9408710%2C9413503%2C9414764%2C9415304%2C9416126&ms=au&mt=1434551329&mv=m&mime=video%2Fmp4&itag=134&key=yt5&ipbits=0&lmt=1415109083892727&signature=8043E45CF61E4A97598E1671C86FA0EA1F7CA89F.663EB1375F8E7464DE0436E227C83364CEE2B720&clen=7283850&gir=yes&expire=1434573049&requiressl=yes&keepalive=yes&pl=20&ratebypass=yes', u'format_note': u'DASH video', u'player_url': None, u'ext': u'mp4', u'preference': -10040, u'format_id': u'nondash-134', u'height': 360, u'acodec': u'none'}, {u'http_headers': {u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'}, u'format': u'nondash-244 - 480p (DASH video)', u'url': u'https://r9---sn-h557sn7y.googlevideo.com/videoplayback?ip=59.164.96.123&id=o-AOf2yaeAXNKIYT4mqozs4rSAoYn7snsGGRzJ3MjOxzRd&sparams=clen%2Cdur%2Cgir%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Ckeepalive%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Crequiressl%2Csource%2Cupn%2Cexpire&initcwndbps=95000&source=youtube&mm=31&mn=sn-h557sn7y&sver=3&upn=_H1jB3crDuU&dur=199.950&fexp=9406983%2C9407141%2C9408142%2C9408420%2C9408710%2C9413503%2C9414764%2C9415304%2C9416126&ms=au&mt=1434551329&mv=m&mime=video%2Fwebm&itag=244&key=yt5&ipbits=0&lmt=1413351387514250&signature=BC20F2184758F280E4C3511883BE37D3FE77B429.BB6911F3946C93C11FDE0F72238F64BEF9CF81A9&clen=10703278&gir=yes&expire=1434573049&requiressl=yes&keepalive=yes&pl=20&ratebypass=yes', u'format_note': u'DASH video', u'player_url': None, u'ext': u'webm', u'preference': -10040, u'format_id': u'nondash-244', u'height': 480, u'acodec': u'none'}, {u'http_headers': {u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'}, u'format': u'nondash-135 - 480p (DASH video)', u'url': u'https://r9---sn-h557sn7y.googlevideo.com/videoplayback?ip=59.164.96.123&id=o-AOf2yaeAXNKIYT4mqozs4rSAoYn7snsGGRzJ3MjOxzRd&sparams=clen%2Cdur%2Cgir%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Ckeepalive%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Crequiressl%2Csource%2Cupn%2Cexpire&initcwndbps=95000&source=youtube&mm=31&mn=sn-h557sn7y&sver=3&upn=_H1jB3crDuU&dur=199.949&fexp=9406983%2C9407141%2C9408142%2C9408420%2C9408710%2C9413503%2C9414764%2C9415304%2C9416126&ms=au&mt=1434551329&mv=m&mime=video%2Fmp4&itag=135&key=yt5&ipbits=0&lmt=1415109057889511&signature=75397F61114E1F1682B64CC905B56F20C11C34F5.8EC6B5ABB628F0C45BC81C35144B4B648A547398&clen=14447026&gir=yes&expire=1434573049&requiressl=yes&keepalive=yes&pl=20&ratebypass=yes', u'format_note': u'DASH video', u'player_url': None, u'ext': u'mp4', u'preference': -10040, u'format_id': u'nondash-135', u'height': 480, u'acodec': u'none'}, {u'http_headers': {u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'}, u'format': u'nondash-247 - 720p (DASH video)', u'url': u'https://r9---sn-h557sn7y.googlevideo.com/videoplayback?ip=59.164.96.123&id=o-AOf2yaeAXNKIYT4mqozs4rSAoYn7snsGGRzJ3MjOxzRd&sparams=clen%2Cdur%2Cgir%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Ckeepalive%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Crequiressl%2Csource%2Cupn%2Cexpire&initcwndbps=95000&source=youtube&mm=31&mn=sn-h557sn7y&sver=3&upn=_H1jB3crDuU&dur=199.950&fexp=9406983%2C9407141%2C9408142%2C9408420%2C9408710%2C9413503%2C9414764%2C9415304%2C9416126&ms=au&mt=1434551329&mv=m&mime=video%2Fwebm&itag=247&key=yt5&ipbits=0&lmt=1413351459776458&signature=ECB7E596B9205B2ED3969FA3EDE48A84EE65DAC3.6327902E59BE65293672E57D760BDFEE66F36CDB&clen=19984301&gir=yes&expire=1434573049&requiressl=yes&keepalive=yes&pl=20&ratebypass=yes', u'format_note': u'DASH video', u'player_url': None, u'ext': u'webm', u'preference': -10040, u'format_id': u'nondash-247', u'height': 720, u'acodec': u'none'}, {u'http_headers': {u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'}, u'format': u'nondash-136 - 720p (DASH video)', u'url': u'https://r9---sn-h557sn7y.googlevideo.com/videoplayback?ip=59.164.96.123&id=o-AOf2yaeAXNKIYT4mqozs4rSAoYn7snsGGRzJ3MjOxzRd&sparams=clen%2Cdur%2Cgir%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Ckeepalive%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Crequiressl%2Csource%2Cupn%2Cexpire&initcwndbps=95000&source=youtube&mm=31&mn=sn-h557sn7y&sver=3&upn=_H1jB3crDuU&dur=199.949&fexp=9406983%2C9407141%2C9408142%2C9408420%2C9408710%2C9413503%2C9414764%2C9415304%2C9416126&ms=au&mt=1434551329&mv=m&mime=video%2Fmp4&itag=136&key=yt5&ipbits=0&lmt=1415109060265509&signature=A1944C5AD616DE89F81A5596038D5E150DF63DA6.553BB8F148E721E5582089D798AC74CAB46BFED5&clen=27844269&gir=yes&expire=1434573049&requiressl=yes&keepalive=yes&pl=20&ratebypass=yes', u'format_note': u'DASH video', u'player_url': None, u'ext': u'mp4', u'preference': -10040, u'format_id': u'nondash-136', u'height': 720, u'acodec': u'none'}, {u'http_headers': {u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'}, u'format': u'nondash-248 - 1080p (DASH video)', u'url': u'https://r9---sn-h557sn7y.googlevideo.com/videoplayback?ip=59.164.96.123&id=o-AOf2yaeAXNKIYT4mqozs4rSAoYn7snsGGRzJ3MjOxzRd&sparams=clen%2Cdur%2Cgir%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Ckeepalive%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Crequiressl%2Csource%2Cupn%2Cexpire&initcwndbps=95000&source=youtube&mm=31&mn=sn-h557sn7y&sver=3&upn=_H1jB3crDuU&dur=199.950&fexp=9406983%2C9407141%2C9408142%2C9408420%2C9408710%2C9413503%2C9414764%2C9415304%2C9416126&ms=au&mt=1434551329&mv=m&mime=video%2Fwebm&itag=248&key=yt5&ipbits=0&lmt=1413351482186992&signature=671CD9F2AB63960295AC7666151EE8D4B59EF4BC.D25211862A6A14A7C1E624E353251A6EA0547E26&clen=35665583&gir=yes&expire=1434573049&requiressl=yes&keepalive=yes&pl=20&ratebypass=yes', u'format_note': u'DASH video', u'player_url': None, u'ext': u'webm', u'preference': -10040, u'format_id': u'nondash-248', u'height': 1080, u'acodec': u'none'}, {u'http_headers': {u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'}, u'format': u'nondash-137 - 1080p (DASH video)', u'url': u'https://r9---sn-h557sn7y.googlevideo.com/videoplayback?ip=59.164.96.123&id=o-AOf2yaeAXNKIYT4mqozs4rSAoYn7snsGGRzJ3MjOxzRd&sparams=clen%2Cdur%2Cgir%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Ckeepalive%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Crequiressl%2Csource%2Cupn%2Cexpire&initcwndbps=95000&source=youtube&mm=31&mn=sn-h557sn7y&sver=3&upn=_H1jB3crDuU&dur=199.949&fexp=9406983%2C9407141%2C9408142%2C9408420%2C9408710%2C9413503%2C9414764%2C9415304%2C9416126&ms=au&mt=1434551329&mv=m&mime=video%2Fmp4&itag=137&key=yt5&ipbits=0&lmt=1415109076900537&signature=75AAE64993862FECFC56BC9B4DDC6CF6B6BE7EA9.D7B716E5ECA0460F4A46B5FCFF6D7A59B07F80F8&clen=57925196&gir=yes&expire=1434573049&requiressl=yes&keepalive=yes&pl=20&ratebypass=yes', u'format_note': u'DASH video', u'player_url': None, u'ext': u'mp4', u'preference': -10040, u'format_id': u'nondash-137', u'height': 1080, u'acodec': u'none'}, {u'asr': 44100, u'tbr': 127, u'format': u'171 - audio only (DASH audio)', u'url': 'https://r9---sn-h557sn7y.googlevideo.com/videoplayback?id=0113bcda551a90cc&itag=171&source=youtube&requiressl=yes&mm=31&mn=sn-h557sn7y&ms=au&mv=m&pl=20&ratebypass=yes&mime=audio/webm&gir=yes&clen=2988367&lmt=1413351345760660&dur=199.986&sver=3&upn=_H1jB3crDuU&fexp=9406983,9407141,9408142,9408420,9408710,9413503,9414764,9415304,9416126&mt=1434551329&key=dg_yt0&signature=9C28C4D813703E83EF6770535F9814E892A63FDC.2731103376C6DE5C99039099EB87410C1766395C&ip=59.164.96.123&ipbits=0&expire=1434573049&sparams=ip,ipbits,expire,id,itag,source,requiressl,mm,mn,ms,mv,pl,ratebypass,mime,gir,clen,lmt,dur', u'vcodec': u'none', u'format_note': u'DASH audio', u'ext': u'webm', u'height': None, u'width': None, u'abr': 128, u'preference': -50, u'fps': None, u'format_id': '171', u'http_headers': {u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'}, u'filesize': 2988367}, {u'asr': 44100, u'tbr': 156, u'container': u'm4a_dash', u'format': u'140 - audio only (DASH audio)', u'url': 'https://r9---sn-h557sn7y.googlevideo.com/videoplayback?id=0113bcda551a90cc&itag=140&source=youtube&requiressl=yes&mm=31&mn=sn-h557sn7y&ms=au&mv=m&pl=20&ratebypass=yes&mime=audio/mp4&gir=yes&clen=3212492&lmt=1415087040625265&dur=200.039&sver=3&upn=_H1jB3crDuU&fexp=9406983,9407141,9408142,9408420,9408710,9413503,9414764,9415304,9416126&mt=1434551329&key=dg_yt0&signature=53FE089D3B28666FADCF44EBD92EF1973F7DC945.8A8D962E88EB696A9308C453663D3CD9B99AB1BB&ip=59.164.96.123&ipbits=0&expire=1434573049&sparams=ip,ipbits,expire,id,itag,source,requiressl,mm,mn,ms,mv,pl,ratebypass,mime,gir,clen,lmt,dur', u'filesize': 3212492, u'vcodec': u'none', u'format_note': u'DASH audio', u'abr': 128, u'height': None, u'width': None, u'ext': u'm4a', u'preference': -50, u'fps': None, u'format_id': '140', u'http_headers': {u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'}, u'acodec': u'aac'}, {u'asr': 44100, u'tbr': 276, u'container': u'm4a_dash', u'format': u'141 - audio only (DASH audio)', u'url': 'https://r9---sn-h557sn7y.googlevideo.com/videoplayback?id=0113bcda551a90cc&itag=141&source=youtube&requiressl=yes&mm=31&mn=sn-h557sn7y&ms=au&mv=m&pl=20&ratebypass=yes&mime=audio/mp4&gir=yes&clen=6378436&lmt=1415087040874304&dur=200.039&sver=3&upn=_H1jB3crDuU&fexp=9406983,9407141,9408142,9408420,9408710,9413503,9414764,9415304,9416126&mt=1434551329&key=dg_yt0&signature=1A8EAEDDD18CC94996AF226CF58F3224502919C7.69FA6A35433B30CB3E9469A787828DCD22CE65CD&ip=59.164.96.123&ipbits=0&expire=1434573049&sparams=ip,ipbits,expire,id,itag,source,requiressl,mm,mn,ms,mv,pl,ratebypass,mime,gir,clen,lmt,dur', u'filesize': 6378436, u'vcodec': u'none', u'format_note': u'DASH audio', u'abr': 256, u'height': None, u'width': None, u'ext': u'm4a', u'preference': -50, u'fps': None, u'format_id': '141', u'http_headers': {u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'}, u'acodec': u'aac'}, {u'asr': None, u'tbr': 99, u'container': u'webm', u'format': u'278 - 256x144 (DASH video)', u'url': 'https://r9---sn-h557sn7y.googlevideo.com/videoplayback?id=0113bcda551a90cc&itag=278&source=youtube&requiressl=yes&mm=31&mn=sn-h557sn7y&ms=au&mv=m&pl=20&ratebypass=yes&mime=video/webm&gir=yes&clen=2171235&lmt=1413351408023221&dur=199.950&sver=3&upn=_H1jB3crDuU&fexp=9406983,9407141,9408142,9408420,9408710,9413503,9414764,9415304,9416126&mt=1434551329&key=dg_yt0&signature=55C82E95296D26E160F09862C1ABC64C98426E11.604A280515B1F3796454D94A156116E579B0D8FC&ip=59.164.96.123&ipbits=0&expire=1434573049&sparams=ip,ipbits,expire,id,itag,source,requiressl,mm,mn,ms,mv,pl,ratebypass,mime,gir,clen,lmt,dur', u'filesize': 2171235, u'vcodec': u'VP9', u'format_note': u'DASH video', u'height': 144, u'width': 256, u'ext': u'webm', u'preference': -40, u'fps': 12, u'format_id': '278', u'http_headers': {u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'}, u'acodec': u'none'}, {u'asr': None, u'tbr': 111, u'format': u'160 - 256x144 (DASH video)', u'url': 'https://r9---sn-h557sn7y.googlevideo.com/videoplayback?id=0113bcda551a90cc&itag=160&source=youtube&requiressl=yes&mm=31&mn=sn-h557sn7y&ms=au&mv=m&pl=20&ratebypass=yes&mime=video/mp4&gir=yes&clen=2732270&lmt=1415109055383527&dur=200.033&sver=3&upn=_H1jB3crDuU&fexp=9406983,9407141,9408142,9408420,9408710,9413503,9414764,9415304,9416126&mt=1434551329&key=dg_yt0&signature=317C42BCB2BB38BBA2399F50CD189587870E4775.63F045F8E80F369C44129AB1A9D7DD21470C8F85&ip=59.164.96.123&ipbits=0&expire=1434573049&sparams=ip,ipbits,expire,id,itag,source,requiressl,mm,mn,ms,mv,pl,ratebypass,mime,gir,clen,lmt,dur', u'filesize': 2732270, u'format_note': u'DASH video', u'height': 144, u'width': 256, u'ext': u'mp4', u'preference': -40, u'fps': 12, u'format_id': '160', u'http_headers': {u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'}, u'acodec': u'none'}, {u'asr': None, u'tbr': 206, u'format': u'242 - 426x240 (DASH video)', u'url': 'https://r9---sn-h557sn7y.googlevideo.com/videoplayback?id=0113bcda551a90cc&itag=242&source=youtube&requiressl=yes&mm=31&mn=sn-h557sn7y&ms=au&mv=m&pl=20&ratebypass=yes&mime=video/webm&gir=yes&clen=3668805&lmt=1413351369421465&dur=199.950&sver=3&upn=_H1jB3crDuU&fexp=9406983,9407141,9408142,9408420,9408710,9413503,9414764,9415304,9416126&mt=1434551329&key=dg_yt0&signature=6810162ED1B77C332ACA6B9EA9FCCD515BA8C7C5.2AB826EDE2840935FB39DD5DF9EEEBBA0FDF5246&ip=59.164.96.123&ipbits=0&expire=1434573049&sparams=ip,ipbits,expire,id,itag,source,requiressl,mm,mn,ms,mv,pl,ratebypass,mime,gir,clen,lmt,dur', u'filesize': 3668805, u'format_note': u'DASH video', u'height': 240, u'width': 426, u'ext': u'webm', u'preference': -40, u'fps': 24, u'format_id': '242', u'http_headers': {u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'}, u'acodec': u'none'}, {u'asr': None, u'tbr': 249, u'format': u'133 - 426x240 (DASH video)', u'url': 'https://r9---sn-h557sn7y.googlevideo.com/videoplayback?id=0113bcda551a90cc&itag=133&source=youtube&requiressl=yes&mm=31&mn=sn-h557sn7y&ms=au&mv=m&pl=20&ratebypass=yes&mime=video/mp4&gir=yes&clen=6123375&lmt=1415109050904308&dur=199.949&sver=3&upn=_H1jB3crDuU&fexp=9406983,9407141,9408142,9408420,9408710,9413503,9414764,9415304,9416126&mt=1434551329&key=dg_yt0&signature=2D5F62BD41B84CF2C1CEE87AA61591E1BFBB93AC.1DC8A755F615373AAD09202A954AAF808AA43BCA&ip=59.164.96.123&ipbits=0&expire=1434573049&sparams=ip,ipbits,expire,id,itag,source,requiressl,mm,mn,ms,mv,pl,ratebypass,mime,gir,clen,lmt,dur', u'filesize': 6123375, u'format_note': u'DASH video', u'height': 240, u'width': 426, u'ext': u'mp4', u'preference': -40, u'fps': 24, u'format_id': '133', u'http_headers': {u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'}, u'acodec': u'none'}, {u'asr': None, u'tbr': 379, u'format': u'243 - 640x360 (DASH video)', u'url': 'https://r9---sn-h557sn7y.googlevideo.com/videoplayback?id=0113bcda551a90cc&itag=243&source=youtube&requiressl=yes&mm=31&mn=sn-h557sn7y&ms=au&mv=m&pl=20&ratebypass=yes&mime=video/webm&gir=yes&clen=6527455&lmt=1413351453081018&dur=199.950&sver=3&upn=_H1jB3crDuU&fexp=9406983,9407141,9408142,9408420,9408710,9413503,9414764,9415304,9416126&mt=1434551329&key=dg_yt0&signature=981CB46CF5B7F3051ABB4B944AD8444BB275BF88.63F9EB65964D8D40B88BCE1967F2DB631887BF4F&ip=59.164.96.123&ipbits=0&expire=1434573049&sparams=ip,ipbits,expire,id,itag,source,requiressl,mm,mn,ms,mv,pl,ratebypass,mime,gir,clen,lmt,dur', u'filesize': 6527455, u'format_note': u'DASH video', u'height': 360, u'width': 640, u'ext': u'webm', u'preference': -40, u'fps': 24, u'format_id': '243', u'http_headers': {u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'}, u'acodec': u'none'}, {u'asr': None, u'tbr': 407, u'format': u'134 - 640x360 (DASH video)', u'url': 'https://r9---sn-h557sn7y.googlevideo.com/videoplayback?id=0113bcda551a90cc&itag=134&source=youtube&requiressl=yes&mm=31&mn=sn-h557sn7y&ms=au&mv=m&pl=20&ratebypass=yes&mime=video/mp4&gir=yes&clen=7283850&lmt=1415109083892727&dur=199.949&sver=3&upn=_H1jB3crDuU&fexp=9406983,9407141,9408142,9408420,9408710,9413503,9414764,9415304,9416126&mt=1434551329&key=dg_yt0&signature=3EB80AD5FCCB8500E0275943791A3805238D2401.2D7A143C29E1BD8EE8C58091736C28EE2FBC6D8F&ip=59.164.96.123&ipbits=0&expire=1434573049&sparams=ip,ipbits,expire,id,itag,source,requiressl,mm,mn,ms,mv,pl,ratebypass,mime,gir,clen,lmt,dur', u'filesize': 7283850, u'format_note': u'DASH video', u'height': 360, u'width': 640, u'ext': u'mp4', u'preference': -40, u'fps': 24, u'format_id': '134', u'http_headers': {u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'}, u'acodec': u'none'}, {u'asr': None, u'tbr': 635, u'format': u'244 - 854x480 (DASH video)', u'url': 'https://r9---sn-h557sn7y.googlevideo.com/videoplayback?id=0113bcda551a90cc&itag=244&source=youtube&requiressl=yes&mm=31&mn=sn-h557sn7y&ms=au&mv=m&pl=20&ratebypass=yes&mime=video/webm&gir=yes&clen=10703278&lmt=1413351387514250&dur=199.950&sver=3&upn=_H1jB3crDuU&fexp=9406983,9407141,9408142,9408420,9408710,9413503,9414764,9415304,9416126&mt=1434551329&key=dg_yt0&signature=9A9AF29000F961E78F1B205FDA2AABF0CBB5BC93.9B533BADBDE57CBBBE41B3C766E577F2EF11C2CC&ip=59.164.96.123&ipbits=0&expire=1434573049&sparams=ip,ipbits,expire,id,itag,source,requiressl,mm,mn,ms,mv,pl,ratebypass,mime,gir,clen,lmt,dur', u'filesize': 10703278, u'format_note': u'DASH video', u'height': 480, u'width': 854, u'ext': u'webm', u'preference': -40, u'fps': 24, u'format_id': '244', u'http_headers': {u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'}, u'acodec': u'none'}, {u'asr': None, u'tbr': 797, u'format': u'135 - 854x480 (DASH video)', u'url': 'https://r9---sn-h557sn7y.googlevideo.com/videoplayback?id=0113bcda551a90cc&itag=135&source=youtube&requiressl=yes&mm=31&mn=sn-h557sn7y&ms=au&mv=m&pl=20&ratebypass=yes&mime=video/mp4&gir=yes&clen=14447026&lmt=1415109057889511&dur=199.949&sver=3&upn=_H1jB3crDuU&fexp=9406983,9407141,9408142,9408420,9408710,9413503,9414764,9415304,9416126&mt=1434551329&key=dg_yt0&signature=38B3E951D08FB0491FCEBD0C33E5E703CD2F256F.1CFDB34A14F80D04653F47FA2688BD80D75D60AF&ip=59.164.96.123&ipbits=0&expire=1434573049&sparams=ip,ipbits,expire,id,itag,source,requiressl,mm,mn,ms,mv,pl,ratebypass,mime,gir,clen,lmt,dur', u'filesize': 14447026, u'format_note': u'DASH video', u'height': 480, u'width': 854, u'ext': u'mp4', u'preference': -40, u'fps': 24, u'format_id': '135', u'http_headers': {u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'}, u'acodec': u'none'}, {u'asr': None, u'tbr': 1204, u'format': u'247 - 1280x720 (DASH video)', u'url': 'https://r9---sn-h557sn7y.googlevideo.com/videoplayback?id=0113bcda551a90cc&itag=247&source=youtube&requiressl=yes&mm=31&mn=sn-h557sn7y&ms=au&mv=m&pl=20&ratebypass=yes&mime=video/webm&gir=yes&clen=19984301&lmt=1413351459776458&dur=199.950&sver=3&upn=_H1jB3crDuU&fexp=9406983,9407141,9408142,9408420,9408710,9413503,9414764,9415304,9416126&mt=1434551329&key=dg_yt0&signature=1476D3CD568171DEF50D733794B9091398A0F5AA.15B5F2EC2C2C42D53338896E6F356752BD8011B9&ip=59.164.96.123&ipbits=0&expire=1434573049&sparams=ip,ipbits,expire,id,itag,source,requiressl,mm,mn,ms,mv,pl,ratebypass,mime,gir,clen,lmt,dur', u'filesize': 19984301, u'format_note': u'DASH video', u'height': 720, u'width': 1280, u'ext': u'webm', u'preference': -40, u'fps': 24, u'format_id': '247', u'http_headers': {u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'}, u'acodec': u'none'}, {u'asr': None, u'tbr': 1465, u'format': u'136 - 1280x720 (DASH video)', u'url': 'https://r9---sn-h557sn7y.googlevideo.com/videoplayback?id=0113bcda551a90cc&itag=136&source=youtube&requiressl=yes&mm=31&mn=sn-h557sn7y&ms=au&mv=m&pl=20&ratebypass=yes&mime=video/mp4&gir=yes&clen=27844269&lmt=1415109060265509&dur=199.949&sver=3&upn=_H1jB3crDuU&fexp=9406983,9407141,9408142,9408420,9408710,9413503,9414764,9415304,9416126&mt=1434551329&key=dg_yt0&signature=63B26B57C7E155CE1F8F445918B57699E93D3E8F.563984800D8BF8CDB1115AF6158A8B5E247CEA32&ip=59.164.96.123&ipbits=0&expire=1434573049&sparams=ip,ipbits,expire,id,itag,source,requiressl,mm,mn,ms,mv,pl,ratebypass,mime,gir,clen,lmt,dur', u'filesize': 27844269, u'format_note': u'DASH video', u'height': 720, u'width': 1280, u'ext': u'mp4', u'preference': -40, u'fps': 24, u'format_id': '136', u'http_headers': {u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'}, u'acodec': u'none'}, {u'asr': None, u'tbr': 2001, u'format': u'248 - 1920x1080 (DASH video)', u'url': 'https://r9---sn-h557sn7y.googlevideo.com/videoplayback?id=0113bcda551a90cc&itag=248&source=youtube&requiressl=yes&mm=31&mn=sn-h557sn7y&ms=au&mv=m&pl=20&ratebypass=yes&mime=video/webm&gir=yes&clen=35665583&lmt=1413351482186992&dur=199.950&sver=3&upn=_H1jB3crDuU&fexp=9406983,9407141,9408142,9408420,9408710,9413503,9414764,9415304,9416126&mt=1434551329&key=dg_yt0&signature=54326737291EBDC1412729EB992713684A26BE6E.0898DDAA0B8822947B50C0C2F74FE42E49DA23BE&ip=59.164.96.123&ipbits=0&expire=1434573049&sparams=ip,ipbits,expire,id,itag,source,requiressl,mm,mn,ms,mv,pl,ratebypass,mime,gir,clen,lmt,dur', u'filesize': 35665583, u'format_note': u'DASH video', u'height': 1080, u'width': 1920, u'ext': u'webm', u'preference': -40, u'fps': 24, u'format_id': '248', u'http_headers': {u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'}, u'acodec': u'none'}, {u'asr': None, u'tbr': 2897, u'format': u'137 - 1920x1080 (DASH video)', u'url': 'https://r9---sn-h557sn7y.googlevideo.com/videoplayback?id=0113bcda551a90cc&itag=137&source=youtube&requiressl=yes&mm=31&mn=sn-h557sn7y&ms=au&mv=m&pl=20&ratebypass=yes&mime=video/mp4&gir=yes&clen=57925196&lmt=1415109076900537&dur=199.949&sver=3&upn=_H1jB3crDuU&fexp=9406983,9407141,9408142,9408420,9408710,9413503,9414764,9415304,9416126&mt=1434551329&key=dg_yt0&signature=2FFC5F9CC12EE2ADC168D53EE3DBC0F545F3C2BE.0D6FC4D492AF377980F024BC399D9209307BA45C&ip=59.164.96.123&ipbits=0&expire=1434573049&sparams=ip,ipbits,expire,id,itag,source,requiressl,mm,mn,ms,mv,pl,ratebypass,mime,gir,clen,lmt,dur', u'filesize': 57925196, u'format_note': u'DASH video', u'height': 1080, u'width': 1920, u'ext': u'mp4', u'preference': -40, u'fps': 24, u'format_id': '137', u'http_headers': {u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'}, u'acodec': u'none'}, {u'width': 176, u'ext': u'3gp', u'format': u'17 - 176x144', u'url': u'https://r9---sn-h557sn7y.googlevideo.com/videoplayback?ip=59.164.96.123&mime=video%2F3gpp&itag=17&key=yt5&ipbits=0&id=o-AOf2yaeAXNKIYT4mqozs4rSAoYn7snsGGRzJ3MjOxzRd&sparams=dur%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Crequiressl%2Csource%2Cupn%2Cexpire&lmt=1413282650625849&signature=331EA729C43B3C8F6A6731C3B4A654A7956C55BA.783AB50CBB490BF66F5E32CE1117075AB3B56188&initcwndbps=95000&source=youtube&mm=31&mn=sn-h557sn7y&sver=3&upn=_H1jB3crDuU&expire=1434573049&requiressl=yes&dur=200.202&pl=20&fexp=9406983%2C9407141%2C9408142%2C9408420%2C9408710%2C9413503%2C9414764%2C9415304%2C9416126&ms=au&mt=1434551329&mv=m&ratebypass=yes', u'format_id': u'17', u'height': 144, u'http_headers': {u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'}, u'player_url': None}, {u'width': 320, u'ext': u'3gp', u'format': u'36 - 320x240', u'url': u'https://r9---sn-h557sn7y.googlevideo.com/videoplayback?ip=59.164.96.123&mime=video%2F3gpp&itag=36&key=yt5&ipbits=0&id=o-AOf2yaeAXNKIYT4mqozs4rSAoYn7snsGGRzJ3MjOxzRd&sparams=dur%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Crequiressl%2Csource%2Cupn%2Cexpire&lmt=1413282667581345&signature=B689BAA4690E8737455DAC59700BB4F7212E5B89.367BC9B3523C446DEB79721FECE7CA5685278007&initcwndbps=95000&source=youtube&mm=31&mn=sn-h557sn7y&sver=3&upn=_H1jB3crDuU&expire=1434573049&requiressl=yes&dur=200.202&pl=20&fexp=9406983%2C9407141%2C9408142%2C9408420%2C9408710%2C9413503%2C9414764%2C9415304%2C9416126&ms=au&mt=1434551329&mv=m&ratebypass=yes', u'format_id': u'36', u'height': 240, u'http_headers': {u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'}, u'player_url': None}, {u'width': 400, u'ext': u'flv', u'format': u'5 - 400x240', u'url': u'https://r9---sn-h557sn7y.googlevideo.com/videoplayback?ip=59.164.96.123&mime=video%2Fx-flv&itag=5&key=yt5&ipbits=0&id=o-AOf2yaeAXNKIYT4mqozs4rSAoYn7snsGGRzJ3MjOxzRd&sparams=dur%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Crequiressl%2Csource%2Cupn%2Cexpire&lmt=1413282511468157&signature=3B74647ADA9B7CD653040C69AD0783ABEE3BE83B.F81704314D8612BA896C10930E1CDC7A5959431B&initcwndbps=95000&source=youtube&mm=31&mn=sn-h557sn7y&sver=3&upn=_H1jB3crDuU&expire=1434573049&requiressl=yes&dur=200.019&pl=20&fexp=9406983%2C9407141%2C9408142%2C9408420%2C9408710%2C9413503%2C9414764%2C9415304%2C9416126&ms=au&mt=1434551329&mv=m&ratebypass=yes', u'format_id': u'5', u'height': 240, u'http_headers': {u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'}, u'player_url': None}, {u'width': 640, u'ext': u'webm', u'format': u'43 - 640x360', u'url': u'https://r9---sn-h557sn7y.googlevideo.com/videoplayback?ip=59.164.96.123&upn=_H1jB3crDuU&id=o-AOf2yaeAXNKIYT4mqozs4rSAoYn7snsGGRzJ3MjOxzRd&sparams=dur%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Cratebypass%2Crequiressl%2Csource%2Cupn%2Cexpire&initcwndbps=95000&source=youtube&mm=31&mn=sn-h557sn7y&sver=3&ratebypass=yes&dur=0.000&fexp=9406983%2C9407141%2C9408142%2C9408420%2C9408710%2C9413503%2C9414764%2C9415304%2C9416126&ms=au&mt=1434551329&mv=m&mime=video%2Fwebm&itag=43&key=yt5&ipbits=0&lmt=1413289173196342&signature=7C36D8BEF0BC15069A5DF04B48397BCAC0376F39.D56E9C1917E2B56507ACB561DFDC517BED9C71B0&expire=1434573049&requiressl=yes&pl=20', u'format_id': u'43', u'height': 360, u'http_headers': {u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'}, u'player_url': None}, {u'width': 640, u'ext': u'mp4', u'format': u'18 - 640x360', u'url': u'https://r9---sn-h557sn7y.googlevideo.com/videoplayback?ip=59.164.96.123&upn=_H1jB3crDuU&id=o-AOf2yaeAXNKIYT4mqozs4rSAoYn7snsGGRzJ3MjOxzRd&sparams=dur%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Cratebypass%2Crequiressl%2Csource%2Cupn%2Cexpire&initcwndbps=95000&source=youtube&mm=31&mn=sn-h557sn7y&sver=3&ratebypass=yes&dur=200.039&fexp=9406983%2C9407141%2C9408142%2C9408420%2C9408710%2C9413503%2C9414764%2C9415304%2C9416126&ms=au&mt=1434551329&mv=m&mime=video%2Fmp4&itag=18&key=yt5&ipbits=0&lmt=1415108968914419&signature=7959F40569D8FF86AE02849D3A23DE942DC1284A.A32ADD340E04992561607D2F34CB3F60237630C6&expire=1434573049&requiressl=yes&pl=20', u'format_id': u'18', u'height': 360, u'http_headers': {u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'}, u'player_url': None}, {u'width': 1280, u'ext': u'mp4', u'format': u'22 - 1280x720', u'url': u'https://r9---sn-h557sn7y.googlevideo.com/videoplayback?ip=59.164.96.123&upn=_H1jB3crDuU&id=o-AOf2yaeAXNKIYT4mqozs4rSAoYn7snsGGRzJ3MjOxzRd&sparams=dur%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Cratebypass%2Crequiressl%2Csource%2Cupn%2Cexpire&initcwndbps=95000&source=youtube&mm=31&mn=sn-h557sn7y&sver=3&ratebypass=yes&dur=200.039&fexp=9406983%2C9407141%2C9408142%2C9408420%2C9408710%2C9413503%2C9414764%2C9415304%2C9416126&ms=au&mt=1434551329&mv=m&mime=video%2Fmp4&itag=22&key=yt5&ipbits=0&lmt=1415109036535899&signature=9A96860C79D5E9394CDA01786DFF6C180726526E.C2BD9E3BB1D0EFABA7ABE873497CDE2DE7792C90&expire=1434573049&requiressl=yes&pl=20', u'format_id': u'22', u'height': 720, u'http_headers': {u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'}, u'player_url': None}], u'width': 1280}

        youlink = getYoulink(self.url)

        youlink.title = testVidinfo['title']
        youlink.thumburl = os.path.join(config.THUMB_URL_PATH, "%s.jpg"%self.getId())
        youlink.youId = testVidinfo['id']

        youlink.filename = "%(title)s-%(id)s.%(ext)s" % vidinfo

        vidinfo["url"] = ""
        vidinfo["formats"] = []

        youlink.vidinfo = vidinfo

        youlink.save()


        pass


    def getVideoDetails(self):

        #if(redisutils.checkInfoDownloaded(self.getId())):
        #    return 0

        ydl_options = {

        }

        if "youtube.com" in self.url:
            # ydl_options["proxy"] = 'http://10.3.100.207:8080'
            ydl_options["proxy"] = ''
        else:
            ydl_options["proxy"] = 'http://localhost:8118'


        with youtube_dl.YoutubeDL(ydl_options) as ydl:
            vidinfo = ydl.extract_info(self.url, download=False)

        thUrl = vidinfo["thumbnails"][0]["url"] #"http://img.youtube.com/vi/%s/mqdefault.jpg" % vidinfo['id']
        file_path = os.path.join(config.THUMBNAILS_DIR, "%s.jpg"%self.getId())
        
        # print thUrl, file_path
        utils.download_photo(thUrl, file_path)
        
        self.updateDetails(vidinfo)

        redisutils.markInfoDownloaded(self.getId())

        return vidinfo


    def updateDownloadDetails(self, stats):

        self.dlDetails = stats
        self.save()
        self.reload()
        return self

    def markDownloadComplete(self):

        self.status = "Finished"
        self.save()


    def getId(self):
        return str(self.id)

    def getFileName(self):

        if(self.status != "Finished"):
            return self.filename + ".part"

        return self.filename

    def downloadThumb(self):

        try:
            thUrl = self.vidinfo["thumbnails"][0]["url"] #"http://img.youtube.com/vi/%s/mqdefault.jpg" % vidinfo['id']
            file_path = os.path.join(config.THUMBNAILS_DIR, "%s.jpg"%self.getId())
            utils.download_photo(thUrl, file_path)
        except:
            return False

    def checkThumbExists(self):

        file_path = os.path.join(config.THUMBNAILS_DIR, "%s.jpg"%self.getId())
        return os.path.isfile(file_path)


def getDownloadingList():

    return Youlink.objects(status__ne = "Finished").order_by('-id')[:10]

def getAllList():

    return Youlink.objects(status = "Finished").order_by('id')

import jobsmanager

def startAllUnfinishedDownloads():


    vids = getDownloadingList()
    for vid in vids:
        job = jobsmanager.DownloadJob()
        job.addDownloadJob(vid)


def stopAllUnfinishedDownloads():

    for jobid in jobsmanager.JOBS:
        job = jobsmanager.JOBS.get(jobid)
        job.p.terminate()

    jobsmanager.JOBS = {}

    print("Cancelled ALL DOWNLOAD")

def getActiveDownloads():

    results = []

    for jobid in jobsmanager.JOBS:
        job = jobsmanager.JOBS.get(jobid)
        results.append(json.loads(job.youlink.to_json()))

    return json.dumps(results)

def getYoulinkFromId(the_id):

    return Youlink.objects.get(id=the_id)


def getYoulink(pUrl):

    youlink = None
    youresult = Youlink.objects(url=pUrl)

    if( youresult.count() > 0):
        youlink = youresult.first()

    return youlink


def addUrl(newurl):

    youlink = Youlink(url=newurl, title=newurl, thumbUrl="/static/images/default.jpg", status=_DOWNLOADING)

    youlink_exist = getYoulink(newurl)

    if(youlink_exist  == None):
        youlink.save()
        msg = "Added"
    else:
        youlink = youlink_exist
        msg = "Already Downloaded"

    return youlink, msg


def updateDetails():
    pass
