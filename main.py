#!/usr/bin/env python
# encoding: utf-8

__author__ = 'rohanraja'

import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.websocket
import tornado.template as template
import time
import Youlink
import json
import jobsmanager
import config
import os
import webinterface

class MainHandler(tornado.web.RequestHandler):

    def get(self):

        loader = template.Loader("static/partials/")
        outp = loader.load("index.html").generate(myvalue="XXX")
        self.write(outp)

        #print "Got"

        f = open("static/partials/index.html")
        self.write(f.read())


class DownloadAllVideo(tornado.web.RequestHandler):

    def get(self):

        Youlink.startAllUnfinishedDownloads()
        self.write("Downloading ALL")
        return

lastVid = ''

class AddVideo(tornado.web.RequestHandler):

    def get(self):
        
        global lastVid
        
        newUrl = self.get_argument('q', '')

        youlink, msg = Youlink.addUrl(newUrl)

        print("Added %s" % newUrl)
        if lastVid == newUrl :
            print("Starting Download..")
            youlink.getVideoDetails()

            job = jobsmanager.DownloadJob()
            job.addDownloadJob(youlink)

        lastVid = newUrl
        self.write(msg)


class EchoWebSocket(tornado.websocket.WebSocketHandler):

    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        
        print("Recieved")
        self.write_message(message)


    def on_close(self):
        print("WebSocket closed")

class DLlist(tornado.websocket.WebSocketHandler):

    def open(self):
        pass
        #print("WebSocket opened")

    def on_message(self, message):

        # print("Recieved List Request")

        if(len(message.split('_')) > 1):

            funcName = message.split('_')[1]

            func = getattr(Youlink, funcName)

            func()

        else:
            if message=="active":
                dlList = Youlink.getActiveDownloads()
                self.write_message(dlList)
            else:
                dlList = Youlink.getDownloadingList()

                self.write_message(dlList.to_json())

                jobsmanager.NEWDOWNLOADLISTENERS.append(self.onNewDlNotification)

    def onNewDlNotification(self, youlink):

        dlList = Youlink.getDownloadingList()
        self.write_message(dlList.to_json())

    def on_close(self):

        try:
            jobsmanager.NEWDOWNLOADLISTENERS.remove(self.onNewDlNotification)
        except:
            pass
        # print("WebSocket closed")


class DLUpdateSocket(tornado.websocket.WebSocketHandler):

    def open(self, jid):

        jobid = jid
        # print("WebSocket opened")
        jobsmanager.addListener(jobid, self.write_message)
        # print "Job Added"
        #self.write_message("1")

    def on_message(self, message):

        # print("Recieved %s "%message)

        if(len(message.split('_')) > 1):

            funcSig = message.split('_')[1]

            funcName = funcSig.split('/')[0]
            funcArgs = funcSig.split('/')[1:]

            func = getattr(webinterface, funcName)
            func(*funcArgs)
            self.write_message("gotfunc")



    def on_close(self):

        jobsmanager.delListener(self.write_message)
        #print("WebSocket closed")


class ReDownload(tornado.web.RequestHandler):

    def get(self, youid):


        youlink = Youlink.getYoulinkFromId(youid)

        # ToDo : If vidinfo not there, download it

        job = jobsmanager.DownloadJob()
        job.addDownloadJob(youlink)

        self.write("Added")

class StopDownload(tornado.web.RequestHandler):

    def get(self, youid):
        jobsmanager.cancelDownload(youid)

class VideoHandler(tornado.web.RequestHandler):

    def get(self, youid):

        youlink = Youlink.getYoulinkFromId(youid)

        redirUrl = os.path.join(config.VIDEO_SERVER_URL, youlink.getFileName())

        self.redirect(redirUrl)

class MyStaticFileHandler(tornado.web.StaticFileHandler):
    def set_extra_headers(self, path):
        # Disable cache
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')

handlers = [

     (r"/",                         MainHandler),
     (r"/websocket",                EchoWebSocket),
     (r"/dlupdates/(.*)",           DLUpdateSocket),
     (r"/dlList",                   DLlist),
     (r"/newlink",                  DownloadAllVideo),
     (r"/redownload/(.*)",          ReDownload),
     (r"/stopdownload/(.*)",        StopDownload),
     (r"/video/(.*)",               VideoHandler),
     (r'/static/(.*)',              MyStaticFileHandler, {'path': "static"}),
     (r'/thumbs/(.*)',              tornado.web.StaticFileHandler, {'path': config.THUMBNAILS_DIR})

]

extHandlers = [

     (r"/add_link",             AddVideo)

]



application = tornado.web.Application(handlers)

extensionApp = tornado.web.Application(extHandlers)

if __name__ == "__main__":



    application.listen(config.HTTP_LISTEN_PORT)

    http_server = tornado.httpserver.HTTPServer(extensionApp, ssl_options={
    "certfile": config.CERT_FILE,
    "keyfile": config.KEY_FILE,
    })

    http_server.listen(config.HTTPS_LISTEN_PORT)

    tornado.ioloop.IOLoop.instance().start()
