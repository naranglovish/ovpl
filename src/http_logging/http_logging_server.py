#!/usr/bin/env python
# Authors : Nitish,Siddharth
# Organization : VLEAD, Virtual-Labs
# Services exposed by LoggingServer
# http://host-name/log/

import threading
import helper
import time
import json
import os
import __init__
# tornado imports
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
from tornado.options import define, options
from envsetup import EnvSetUp


current_file_path = os.path.dirname(os.path.abspath(__file__))
config_spec       = json.loads(open(current_file_path + "/../../config/config.json").read())
define("port",
       default=int(config_spec["LOGGING_CONFIGURATION"]["LOGSERVER_CONFIGURATION"]["SERVER_PORT"]),
       help="run on the given port", type=int)


class LogHandler(tornado.web.RequestHandler):
    def get(self):
        print "Hello World"

    def post(self):
        """Spawns a new thread for every request and passes the request as \
        arguments to log() function"""
        t = threading.Thread(target=helper.log,
                             args=(self.request.arguments,))
        t.start()


class OtherHandler(tornado.web.RequestHandler):
    def get(self):
        pass

    def post(self):
        pass

if __name__ == "__main__":
    e = EnvSetUp()
    app = tornado.web.Application(
        handlers=[
            (r"/log/.*", LogHandler),
            (r"/.*", OtherHandler),
        ],
        debug=True)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.bind(options.port)
    http_server.start(1)
    tornado.ioloop.IOLoop.instance().start()