import redisutils

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
from processUrl import processUrl

class AddVideo(tornado.web.RequestHandler):

    def get(self):

        newUrl = self.get_argument('q', '')
        newTitle = self.get_argument('title', '')

        print("Adding URL %s" % newUrl)
        print("Adding TITLE %s" % newTitle)

        processUrl.apply_async(args=[newUrl, newTitle], queue="processUrl")
        msg = "Enqueued URL"
        # redisutils.enqueueForDownload(newUrl)
        self.write(msg)


extHandlers = [

     (r"/add_link",             AddVideo)

]

extensionApp = tornado.web.Application(extHandlers)

if __name__ == "__main__":


    http_server = tornado.httpserver.HTTPServer(extensionApp, ssl_options={
    "certfile": config.CERT_FILE,
    "keyfile": config.KEY_FILE,
    })
    http_server.listen(config.HTTPS_LISTEN_PORT)
    print("Listening for Youdownload Requests on HTTPS PORT: %d" % config.HTTPS_LISTEN_PORT)
    tornado.ioloop.IOLoop.instance().start()
