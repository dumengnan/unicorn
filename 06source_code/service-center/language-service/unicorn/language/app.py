#!/usr/bin/env python
# encoding: utf-8

from flask import Flask
from flask_restful import Api
from detect.detect_language import DetectLanguage

app = Flask(__name__)
api = Api(app)


api.add_resource(DetectLanguage, '/language/detect')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001 , debug=True)