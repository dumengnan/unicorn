#!/usr/bin/env python
# encoding: utf-8


'''
Created on 2018

@author: Administrator
'''
import logging
from flask import request, Blueprint, abort, jsonify
from langdetect import detect

detect_language_api = Blueprint('detect_language_api', __name__, template_folder='templates')

@detect_language_api.route('/language/detect', methods=['POST'])
def detect_text():
    if not request.json or not 'text' in request.json:
        abort(400)

    input_text = request.json.get("text", "")
    lang = detect(input_text)
    logging.info("Detect Text " + input_text + ", Lang is " + lang)
    return jsonify({'lang': lang})

