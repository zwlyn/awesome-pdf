#!/usr/bin/env python
# -*- coding: utf_8 -*-
import sys, os

if ((3, 0) <= sys.version_info <= (3, 9)):
    sys.path.insert(0, os.sep.join([os.getcwd(), "site-packages-37"]))
elif ((2, 0) <= sys.version_info <= (2, 9)):
    sys.path.insert(0, os.sep.join([os.getcwd(), "site-packages-27"]))
from tornado.wsgi import WSGIContainer
from tornado.web import Application, RequestHandler, FallbackHandler
from tornado.ioloop import IOLoop
from tornado.autoreload import watch
from view import app, NotifyHandler
from log import logger

class VueHandler(RequestHandler):
    def get(self):
        self.render("index.html")

if __name__ == '__main__':
    settings = {
        'debug' : True,
        'template_path': os.path.join(os.path.dirname(__file__), "static"),
        'static_path': os.path.join(os.path.dirname(__file__), "static"),
        'xsrf_cookies':False,
    }
    watch(os.sep.join([os.getcwd(), "restart.json"]))
    wsgi_app = WSGIContainer(app)
    application = Application([
        (r'/index', VueHandler),
        (r'/ws/api/v1/notify', NotifyHandler),
        (r'.*', FallbackHandler, dict(fallback=wsgi_app))
    ], **settings)

    if len(sys.argv) == 2:
        application.listen(int(sys.argv[1]), address="0.0.0.0")
    else:
        application.listen(8800, address="0.0.0.0")
    IOLoop.instance().start()

