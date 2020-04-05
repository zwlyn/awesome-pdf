#!/usr/bin/env python
# -*- coding: utf_8 -*-

from flask import Blueprint, request, redirect, url_for, json, Response, send_file, render_template, send_from_directory, make_response
from flask_cors import CORS
import json
import requests
import os
from log import logger
from decimal import Decimal
import time
import threading
from pprint import pformat
import traceback
import copy
import datetime
from threading import Thread
from controller import reportManage
import codecs
import base64

api = Blueprint("api", __name__, url_prefix="/report", static_url_path='')
CORS(api)


def stopApp():
    fpath = os.sep.join([os.getcwd(), "restart.json"])
    with open(fpath, "r") as f:
        ret = json.loads(f.read())

    ret["count"] = ret["count"] + 1

    with open(fpath, "w") as f:
        f.write(json.dumps(ret, indent=4))


class ObjectDict(dict):
    """Makes a dictionary behave like an object, with attribute-style access.
    """

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value


def timeToSeconds(t, sep=":"):
    if t == "":
        t = "0:0:0"
    ts = [int(i) for i in t.split(sep)]
    return ts[0] * 60 * 60 + ts[1] * 60 + ts[2]


def secondsToTime(seconds, sep=":"):
    h = seconds / 3600
    m = seconds % 3600 / 60
    s = (seconds - h * 3600 - m * 60) % 60

    return sep.join([str(i) for i in [h, m, s]])


def writeFile(fpath, result):
    with open(fpath, 'w') as f:
        f.write(result)

@api.route("/", methods=['GET'])
def reportHome():
    if request.method == "GET":
        ret = {}
        try:
            ret["retcode"] = 0
            ret["message"] = "成功"
        except Exception as e:
            logger.error(traceback.format_exc(e))
            ret["retcode"] = -1
            #ret["message"] = traceback.format_exc(e)
            ret["message"] = "失败"
        return render_template('index.html')

@api.route("/reportmanage/templatesList", methods=['GET'])
def templatesList():
    if request.method == "GET":
        ret = {}
        try:
            ret["retcode"] = 0
            ret["message"] = reportManage.templatesList()
        except Exception as e:
            logger.error(traceback.format_exc(e))
            ret["retcode"] = -1
            #ret["message"] = traceback.format_exc(e)
            ret["message"] = "失败"
        return ret

@api.route("/reportmanage/setTemplate", methods=['POST'])
def setTemplate():
    if request.method == "POST":
        ret = {}
        templateName = json.loads(request.data)['templateName']
        logger.info(templateName)
        try:
            ret["retcode"] = 0
            ret["message"] = reportManage.setTemplate(templateName)
        except Exception as e:
            logger.error(traceback.format_exc(e))
            ret["retcode"] = -1
            #ret["message"] = traceback.format_exc(e)
            ret["message"] = "失败"
        return ret

@api.route("/reportmanage/delTemplate", methods=['POST'])
def delTemplate():
    if request.method == "POST":
        ret = {}
        templateName = json.loads(request.data)['templateName']
        logger.info(templateName)
        try:
            ret["retcode"] = 0
            ret["message"] = reportManage.delTemplate(templateName)
        except Exception as e:
            logger.error(traceback.format_exc(e))
            ret["retcode"] = -1
            #ret["message"] = traceback.format_exc(e)
            ret["message"] = "失败"
        return ret

@api.route("/reportmanage/newTemplate", methods=['POST'])
def newTemplate():
    if request.method == "POST":
        ret = {}
        data = json.loads(request.data)
        try:
            ret["retcode"] = 0
            ret["message"] = reportManage.newTemplate(data)
        except Exception as e:
            logger.error(traceback.format_exc(e))
            ret["retcode"] = -1
            #ret["message"] = traceback.format_exc(e)
            ret["message"] = "失败"
        return ret

@api.route("/load", methods=['GET'])
def loadTemplate():
    if request.method == "GET":
        ret = {}
        try:
            ret["retcode"] = 0
            ret["message"] = "成功"
        except Exception as e:
            logger.error(traceback.format_exc(e))
            ret["retcode"] = -1
            #ret["message"] = traceback.format_exc(e)
            ret["message"] = "失败"
        return reportManage.loadTemplate()

@api.route("/report/save", methods=['POST'])
def save():
    if request.method == "POST":
        ret = {}
        json_data = json.loads(request.data.decode('utf-8'))
        try:
            ret["retcode"] = 0
            ret["message"] = reportManage.save(json_data)
        except Exception as e:
            logger.error(traceback.format_exc(e))
            ret["retcode"] = -1
            #ret["message"] = traceback.format_exc(e)
            ret["message"] = "失败"
        return ret

@api.route("/report/run", methods=['PUT'])
def render():
    if request.method == "PUT":
        ret = {}
        json_data = json.loads(request.data.decode('utf-8'))
        return reportManage.renderReport(json_data)


@api.route("/report/run", methods=['GET'])
def getReportPdf():
    if request.method == "GET":
        ret = {}
        #json_data = json.loads(request.data)
        key = request.args.get('key')
        return reportManage.getReportPdf(key)


@api.route("/reportmanage/getData", methods=['GET'])
def getdata():
    if request.method == "GET":
        ret = {}
        try:
            ret["retcode"] = 0
            ret["message"] = reportManage.getData()

        except Exception as e:
            logger.error(traceback.format_exc(e))
            ret["retcode"] = -1
            ret["message"] = traceback.format_exc(e)
        return ret

@api.route("/reportmanage/setData", methods=['POST'])
def setdata():
    if request.method == "POST":
        ret = {}
        try:
            data = json.loads(request.data)
            #logger.info(data)
            ret["retcode"] = 0
            ret["message"] = reportManage.setData(data)

        except Exception as e:
            logger.error(traceback.format_exc(e))
            ret["retcode"] = -1
            ret["message"] = traceback.format_exc(e)
        return ret

@api.route("/reportmanage/pdfGenerate", methods=['GET'])
def pdfGenerate():
    if request.method == "GET":
        ret = {}
        try:
            ret["retcode"] = 0
            ret["message"] = reportManage.pdfGenerate()
        except Exception as e:
            logger.error(traceback.format_exc(e))
            ret["retcode"] = -1
            #ret["message"] = traceback.format_exc(e)
            ret["message"] = "失败"
        return ret



@api.route("/reportmanage/upload/pdf", methods=['POST'])
def upload_pdf():
    if request.method == "POST":
        file = request.files.get('pdf')
        logger.info(file)
        logger.info(file.filename)
        return reportManage.uploadPdf(file)

@api.route("/reportmanage/upload/template", methods=['POST'])
def upload_template():
    if request.method == "POST":
        file = request.files.get('template')
        logger.info(file)
        logger.info(file.filename)
        return reportManage.uploadTemplate(file)

@api.route("/reportmanage/combinePdf", methods=['GET'])
def combinePdf():
    if request.method == "GET":
        ret = {}
        try:
            ret["retcode"] = 0
            ret["message"] = reportManage.combinePdf()
        except Exception as e:
            logger.error(traceback.format_exc(e))
            ret["retcode"] = -1
            ret["message"] = "失败"
        return ret

@api.route("/reportmanage/pdftotext", methods=['POST'])
def pdftotext():
    if request.method == "POST":
        logger.info(json.loads(request.data.decode('utf-8')))
        uploadPath = json.loads(request.data.decode('utf-8'))['uploadPath']
        return reportManage.pdftotext(uploadPath)

@api.route("/reportmanage/downloadText", methods=['POST'])
def downloadText():
    if request.method == "POST":
        logger.info(json.loads(request.data.decode('utf-8')))
        textPath = json.loads(request.data.decode('utf-8'))['textPath']
        textPath = os.path.abspath(textPath)
        directory = os.path.dirname(textPath)
        file_name = os.path.basename(textPath)
        response = make_response(
                send_from_directory(directory, file_name, as_attachment=True))
        return response

@api.route("/reportmanage/clearPdfList", methods=['GET'])
def clearPdfList():
    if request.method == "GET":
        ret = {}
        try:
            ret["retcode"] = 0
            ret["message"] = reportManage.clearPdfList()
        except Exception as e:
            logger.error(traceback.format_exc(e))
            ret["retcode"] = -1
            ret["message"] = "失败"
        return ret

@api.route("/reportmanage/delPdfList", methods=['POST'])
def delPdfList():
    if request.method == "POST":
        ret = {}
        try:
            item = json.loads(request.data)
            logger.info(item)
            ret["retcode"] = 0
            ret["message"] = reportManage.delPdfList(item)
        except Exception as e:
            logger.error(traceback.format_exc(e))
            ret["retcode"] = -1
            ret["message"] = "失败"
        return ret


@api.route("/reportmanage/downloadData", methods=['POST'])
def downloadData():
    if request.method == "POST":
        ret = {}
        data = json.loads(request.data)
        logger.info(data)
        directoryList = data['dataPath'].split(os.sep)[:-1]
        logger.info(directoryList)
        directory = os.sep.join(directoryList)
        filename = data['dataName'] + '.json'

        logger.info(filename)
        file = send_from_directory(directory, filename, as_attachment=True)
        return file

@api.route("/reportmanage/downloadPdf", methods=['POST'])
def downloadPdf():
    if request.method == "POST":
        ret = {}
        dataModel = json.loads(request.data)
        path = dataModel['pdfPath']
        filename = path.split(os.sep)[-1]
        if os.path.exists(path) is False:
            reportManage.savePdf(dataModel)
        with open(path, 'rb') as f:
            content = f.read()
            base64_data  = base64.b64encode(content)
            s  =  base64_data.decode()
        response = make_response(s)
        response.headers["Content-type"] = "application/pdf"
        response.headers["Content-disposition"] = 'inline; filename="{filename}"'.format(
            filename=filename)
        return response

@api.route("/reportmanage/dataList", methods=['GET'])
def getDataList():
    if request.method == "GET":
        ret = {}
        try:
            ret["retcode"] = 0
            ret["message"] = reportManage.getDataList()
        except Exception as e:
            logger.error(traceback.format_exc(e))
            ret["retcode"] = -1
            ret["message"] = "失败"
        return ret

@api.route("/reportmanage/delData", methods=['POST'])
def delData():
    if request.method == "POST":
        ret = {}
        data = json.loads(request.data)
        try:
            ret["retcode"] = 0
            ret["message"] = reportManage.delData(data)
        except Exception as e:
            logger.error(traceback.format_exc(e))
            ret["retcode"] = -1
            ret["message"] = "失败"
        return ret

@api.route("/reportmanage/editData", methods=['POST'])
def editData():
    if request.method == "POST":
        ret = {}
        data = json.loads(request.data)
        try:
            ret["retcode"] = 0
            ret["message"] = reportManage.editData(data)
        except Exception as e:
            logger.error(traceback.format_exc(e))
            ret["retcode"] = -1
            ret["message"] = "失败"
        return ret

@api.route("/reportmanage/saveData", methods=['POST'])
def saveData():
    if request.method == "POST":
        ret = {}
        data = json.loads(request.data)
        try:
            ret["retcode"] = 0
            ret["message"] = reportManage.saveData(data)
        except Exception as e:
            logger.error(traceback.format_exc(e))
            ret["retcode"] = -1
            ret["message"] = "失败"
        return ret

@api.route("/reportmanage/formatData", methods=['POST'])
def formatData():
    if request.method == "POST":
        ret = {}
        data = json.loads(request.data)
        # logger.info(data)
        try:
            ret["retcode"] = 0
            ret["message"] = reportManage.formatData(data)
        except Exception as e:
            logger.error(traceback.format_exc(e))
            ret["retcode"] = -1
            ret["message"] = "失败"
        return ret
        