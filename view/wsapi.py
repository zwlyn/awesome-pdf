#!/usr/bin/env python
# -*- coding: utf_8 -*-
from flask import json
from tornado.websocket import WebSocketHandler, WebSocketClosedError
from log import logger
from utils import ObjectDict
from collections import OrderedDict
from tornado import ioloop
import datetime
import time
import requests
import threading


class WebsocketResponse(ObjectDict):

    def __init__(self, type="Response", api_code=-1, message='fail', data=None, traceback=""):
        super(WebsocketResponse, self).__init__()
        self.type = type
        self.code = api_code
        self.message = message
        self.data = data
        self.traceback = traceback
        if isinstance(self.data, list):
            self.count = len(self.data)


def pushmessage(func):
    def send(*agrs, **kwargs):
        self = agrs[0]
        ret = func(*agrs, **kwargs)
        if ret:
            msg, binary = ret
            try:
                if isinstance(msg, WebsocketResponse) or isinstance(msg, dict):
                    self.write_message(json.dumps(msg), binary)
                elif isinstance(msg, str) or isinstance(msg, unicode):
                    self.write_message(msg, binary)
                else:
                    self.write_message(repr(msg), binary)

            except WebSocketClosedError as e:
                self.on_close()
    return send


class BaseWebsocket(WebSocketHandler):

    handlers = {}

    def open(self):
        logger.warn("websocket of %s is opened", repr(self))
        className = self.__class__.__name__
        if className not in self.handlers:
            self.handlers[className] = set()
        self.handlers[className].add(self)

    @pushmessage
    def send(self, message, binary=False):
        return message, binary

    def on_close(self):
        logger.warn("websocket of %s is closed", repr(self))
        className = self.__class__.__name__
        if className in self.handlers:
            self.handlers[className].remove(self)

    def check_origin(self, origin):
        return True

    @classmethod
    def boardcastMessage(cls, message, binary=False):
        className = cls.__name__
        if className in cls.handlers:
            for handler in cls.handlers[className]:
                handler.send(message, binary)


class NotifyHandler(BaseWebsocket):
    """
        建立与web前端的通信连接，发送状态信息报文
    """

    def open(self):
        super(NotifyHandler, self).open()

    def on_message(self, message):
        # logger.info(message)
        pass
