#!/usr/bin/env python
# -*- coding: utf_8 -*-
import os
import json
import codecs # fix the encoding problem at python2.7
from log import logger
from view.wsapi import NotifyHandler,WebsocketResponse
from tornado.web import HTTPError
from reportbro import Report, ReportBroError
import datetime, decimal, json, os, uuid
from flask import make_response
from operator import itemgetter
from PyPDF2 import PdfFileReader, PdfFileWriter
import traceback
import shutil
import time
import pdfplumber
# from .result2data import Result2data

ReportJsons = {}

# class ReportModel(objectDict):

def loadsJson(fpath):
    with codecs.open(fpath, 'r', encoding='utf-8') as f:
        content = json.loads(f.read())
    return content

def formatTimeStamp(timeStamp):
    localTime = time.localtime(timeStamp) 
    strTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)
    return strTime 

def json2Pdf(jsonTemplate, data, output):
    '''
    jsonTemplate 是数据字典
    data 必须是数据字典 
    '''
    logger.info("[%s]" % output)
    report_definition = jsonTemplate
    fontFile = [dict(value='firefly',filename=os.path.join('static', 'fireflysung.ttf'))]
    is_test_data = {}
    report = Report(report_definition, data, is_test_data, additional_fonts=fontFile)
    try:
        report_file = report.generate_pdf(filename=output, add_watermark=False)
    except Exception as e:
        logger.error("======json to pdf Failed!!======")
        logger.error(traceback.format_exc(e))

    return output

def listdirBymtime(dirPath, typeList=['json', 'txt', 'pdf'], isDir=False, ignore=[]):
    # input dirPath 
    # output filenameList order by modified time reversed
    filenameList = os.listdir(dirPath)
    templateList = []
    for filename in filenameList:
        if filename in ignore:
            continue
        if isDir:
            filePath = os.sep.join([dirPath, filename])
            templateList.append({
            "createTime":os.path.getmtime(filePath),
            "filename":filename
            })

        elif filename.split('.')[-1] in typeList:
            filePath = os.sep.join([dirPath, filename])
            templateList.append({
            "createTime":os.path.getmtime(filePath),
            "filename":filename
            })
    templateList = sorted(templateList, key=itemgetter('createTime'), reverse=True) # order by modified time
    filenameList = [template['filename'] for template in templateList ]
        
    return filenameList




class ManageModel(object):
    def __init__(self):
        super(ManageModel, self).__init__()
        self.manageList = []
        self.dataList = []
        self.createDir()
        self.newManageFile()

    def createDir(self):
        self.manageList = []
        templateNameList = listdirBymtime("jsontemplates", typeList=['json'])
        for fname in templateNameList:
            dirPath = os.path.join(os.getcwd(), 'data', fname.split('.')[0])
            if os.path.exists(dirPath) is False:
                os.system('mkdir -p %s' % dirPath)
            self.manageList.append(dirPath)
       
    def newManageFile(self):
        self.dataList = []
        for dirPath in self.manageList:
            # 处理每个模板下的 manage.json的生成
            managePath = os.path.join(dirPath, 'manage.json')
            templateName = dirPath.split(os.sep)[-1]
            manageModel = {
                "templateName": templateName,
                "dataList":[]
            }
            dataList = listdirBymtime(dirPath, typeList=['json'], ignore='manage.json')
            for dataFile in dataList:
                dataPath = os.path.join(dirPath, dataFile)
                pdfPath = os.path.join(dirPath, dataFile.split('.')[0] + '.pdf')
                templatePath = os.path.join(os.getcwd(), 'jsontemplates', templateName + ".json")
                dataModel = {
                    "templateName": templateName,
                    "templatePath": templatePath,
                    "dataName": dataFile.split('.')[0],
                    "modifiedTime": formatTimeStamp(os.path.getmtime(dataPath)),
                    "createTime": formatTimeStamp(os.path.getctime(dataPath)),
                    "dataPath": dataPath,
                    "pdfPath": pdfPath
                }
                manageModel['dataList'].append(dataModel)
                self.dataList.append(dataModel)
            with open(managePath, 'w') as f:
                f.write(json.dumps(manageModel, indent=4))

    def getManageFile(self, templateName):
        if '.' in templateName:
            templateName = templateName.split('.')[0]
        managePath = os.path.join('data', templateName, 'manage.json')
        return loadsJson(managePath)

    def getDataList(self):
        return self.dataList

    def refresh(self):
        self.createDir()
        self.newManageFile()
        return True



class ReportManage(object):
    def __init__(self):
        super(ReportManage, self).__init__()
        self.model = {
            "templateName": "",
            "templateJson": {},
            "dataJson": {},
            "dataModel":{}
        }
        self.pdfList = []
        self.manageModel = ManageModel()

    def json2report_file(self, jsonTemplate, data):
        '''        
        type(jsonTemplate): dict
        type(data): dict 
        '''
        report_definition = jsonTemplate
        fontFile = [dict(value='firefly',filename=os.path.join('static', 'fireflysung.ttf'))]
        is_test_data = {}
        report = Report(report_definition, data, is_test_data, additional_fonts=fontFile)
        report_file = None
        try:
            report_file = report.generate_pdf()
            logger.info("type(report_file):%s" % type(report_file))
        except Exception as e:
            logger.error(traceback.format_exc(e))
        return report_file

    def saveByKey(self, report_file):
        global ReportJsons
        key = str(uuid.uuid4())
        ReportJsons[key] = report_file
        
        return key

    def getData(self):
        return self.model

    def setData(self, data):
        NotifyHandler.boardcastMessage(WebsocketResponse(
            "reportData", 0, "successs", data=data))
        self.model['dataJson'] = data
        return True
    
    def templatesList(self):
        templatedir =  os.sep.join([os.getcwd(), 'jsontemplates'])
        filenameList = listdirBymtime(templatedir, typeList=['json'])
        ret = {'templatesList': filenameList}
        NotifyHandler.boardcastMessage(WebsocketResponse(
            "templatesList", 0, "successs", data=ret))
        #logger.info(ret)
        return ret

    def setTemplate(self, templateName):
        templatePath = os.sep.join([os.getcwd(), "jsontemplates", templateName])
        with codecs.open(templatePath, "r", encoding="utf-8") as f:
           template = json.loads(f.read())
           
        dirPath = os.path.join(os.getcwd(), 'data', templateName.split('.')[0], '') # 为了从模板出发可以保存data, 用于记录data存放的位置
        self.model = {
            "templateName": templateName,
            "templateJson": template,
            "dataJson": {},
            "dataModel":{
            "dirPath": dirPath
            }
        }
        return self.model
    
    def newTemplate(self, data):
        templateName = data['templateName']
        sample = data['sample']
        templatePath = os.sep.join([os.getcwd(), "jsontemplates", templateName])
        if sample is "":
            self.model["templateJson"] = {}
        else:
            samplePath = os.sep.join([os.getcwd(), "jsontemplates", sample])
            self.model["templateJson"] = loadsJson(samplePath)

        with codecs.open(templatePath, "w", encoding='utf-8') as f:
           f.write(json.dumps(self.model["templateJson"], indent=4))
        self.templatesList() # update template List
        return "new template success"


    def delTemplate(self, templateName):
        templatePath = os.sep.join([os.getcwd(), "jsontemplates", templateName])
        logger.info(templatePath)
        os.remove(templatePath)
        self.templatesList()
        logger.info('已经做了删除操作！')

    def loadTemplate(self):
        return self.model['templateJson']
                
    def save(self, json_data):
        self.model['templateJson'] = json_data
        templatePath = os.sep.join([os.getcwd(), 'jsontemplates', self.model['templateName']])
        with codecs.open(templatePath, "w", encoding='utf-8') as f:
            f.write(json.dumps(self.model['templateJson'], indent=4))
        return templatePath
    
    def renderReport(self, json_data):
        self.additional_fonts = [dict(value='firefly',filename=os.path.join('static','fireflysung.ttf'))]
        report_definition = json_data.get('report')
        output_format = json_data.get('output_format')
        data = json_data.get('data')
        
        is_test_data = bool(json_data.get('isTestData'))
        reprot_file = self.json2report_file(report_definition, data)
        key = self.saveByKey(reprot_file)
        return "key:" + key
    
    def getReportPdf(self, key):
        global ReportJsons
        logger.info(key)
        report_file = ReportJsons[key]
        responsePdf = make_response(report_file)
        now = datetime.datetime.now()
        responsePdf.headers['Content-Type'] = 'application/pdf'
        responsePdf.headers['Content-Disposition'] = "inline; filename='{filename}'".format(filename='report-' + str(now) + '.pdf')
        return responsePdf

    def pdfGenerate(self):
        global ReportJsons
        reprot_file = self.json2report_file(self.model['templateJson'], self.model['dataJson'])
        key = self.saveByKey(reprot_file)
        logger.info(key)
        
        return key

    def uploadPdf(self, file):
        filename = file.filename
        uploadDir = os.sep.join([os.getcwd(), "uploadfiles"])
        if not os.path.exists(uploadDir):
            os.makedirs(uploadDir)
        uploadPath = os.path.join(uploadDir, filename)
        file.save(uploadPath)
        self.pdfList.append(uploadPath)
        
        nameList = [pdfPath.split(os.sep)[-1] for pdfPath in self.pdfList]
        NotifyHandler.boardcastMessage(WebsocketResponse(
            "pdfList", 0, "success", data=nameList))
        
        return uploadPath

    def uploadTemplate(self, file):
        filename = file.filename
        uploadDir = os.sep.join([os.getcwd(), "jsontemplates"])
        if not os.path.exists(uploadDir):
            os.makedirs(uploadDir)
        uploadPath = os.path.join(uploadDir, filename)
        file.save(uploadPath)
        
        return uploadPath


    def pdftotext(self, uploadPath):
        pdf = pdfplumber.open(uploadPath)
        text = ""
        for page in pdf.pages:
            content = page.extract_text()
            text += content
            # print(content)
        pdf.close()
        with open(uploadPath.replace("pdf", "txt"), "w", encoding="utf-8") as f:
            f.write(text)
        return text


    def combinePdf(self):
        #merge the file.
        logger.info(self.pdfList)
        pdf_writer = PdfFileWriter()
        for path in self.pdfList:
            pdf_reader = PdfFileReader(path)
            for page in range(pdf_reader.getNumPages()):
                pdf_writer.addPage(pdf_reader.getPage(page))       
        # 写入合并的pdf
        output = os.path.join(os.getcwd(), "uploadfiles", "combine.pdf")
        with open(output, 'wb') as f:
            pdf_writer.write(f)
                
        # get combined report_file and save by Key
        with open(output, 'rb') as f:
            report_file = f.read()
        key = self.saveByKey(report_file)
        #os.remove(output)
        
        return key
    
    def clearPdfList(self):
        self.pdfList = []
        nameList = [pdfPath.split(os.sep)[-1] for pdfPath in self.pdfList]
        NotifyHandler.boardcastMessage(WebsocketResponse(
            "pdfList", 0, "successs", data=nameList))
        return "clear pdf list ok"

    def delPdfList(self, pdfName):
        pdfPath = os.path.join(os.getcwd(), "uploadfiles", pdfName)
        index = self.pdfList.index(pdfPath)
        self.pdfList.pop(index)
        nameList = [pdfPath.split(os.sep)[-1] for pdfPath in self.pdfList]
        NotifyHandler.boardcastMessage(WebsocketResponse(
            "pdfList", 0, "successs", data=nameList))
        return pdfPath
        
    def getDataList(self):
        return self.manageModel.getDataList()

    def delData(self, dataModel):
        os.remove(dataModel["dataPath"])
        self.manageModel.refresh()
        NotifyHandler.boardcastMessage(WebsocketResponse(
            "dataList", 0, "successs", data={"dataList": self.getDataList()}))
        return "xxx is already delete"
        
        
    def editData(self, dataModel):
        self.model['templateJson'] = loadsJson(dataModel['templatePath'])
        self.model['dataJson'] = loadsJson(dataModel["dataPath"])
        self.model['templateName'] = dataModel['templateName'].split('.')[0]
        self.model['dataModel'] = dataModel
        return "editData ok"

    def saveData(self, model):
        #logger.info(model['dataJson'])
        with open(model['dataModel']['dataPath'], 'w') as f:
            f.write(json.dumps(model['dataJson'], indent=4))
        if model['createPdf'] is True:
            logger.info("model['createPdf'] is True:'")
            if os.path.exists(model['dataModel']['pdfPath']) is False:
                json2Pdf(model['templateJson'], model['dataJson'], model['dataModel']['pdfPath'])
                
        self.manageModel.refresh()
        NotifyHandler.boardcastMessage(WebsocketResponse(
            "dataList", 0, "successs", data={"dataList": self.getDataList()}))
        return "save data ok"

    def formatData(self, model):
        result2data = Result2data(model)
        return result2data.formatData()

    def savePdf(self, dataModel):
        logger.info(dataModel)
        dataJson = loadsJson(dataModel["dataPath"])
        templateJson = loadsJson(dataModel["templatePath"])
        pdfPath = dataModel["pdfPath"]
        logger.info(dataJson)
        json2Pdf(templateJson, dataJson, pdfPath)
        logger.info("pdf ok")



reportManage = ReportManage()