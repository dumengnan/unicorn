#!/usr/bin/env python
# encoding: utf-8


'''
Created on 2018

@author: Administrator
'''
import logging
from flask import request
from flask_restful import Resource
from langdetect import detect

class DetectLanguage(Resource):
    '''
    classdocs
    '''


    def post(self):
        '''
        Constructor
        '''
        param = request.get_json(force=True)
        text = param["text"]
        text = "u\"" + text + "\""
        logging.info("Detect Text " + text)
        lang = detect(text)
        return {'lang': lang}