#!/usr/bin/env python
# -*- coding: utf_8 -*-

from flask import Flask, Response, jsonify
from .api import api
from .wsapi import NotifyHandler

class JsonResponse(Response):
    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, (list, dict)):
            response = jsonify(response)
        return super(Response, cls).force_type(response, environ)

class FlaskAPP(Flask):
    response_class = JsonResponse

def create_app():

    app = FlaskAPP(__name__)
    
    app.config.update({
        "STORAGE_PROVIDER": "LOCAL",
        "STORAGE_KEY": "",
        "STORAGE_SECRET": "",
        "STORAGE_SERVER": True
    })

    app.register_blueprint(api)
    return app

app = create_app()





