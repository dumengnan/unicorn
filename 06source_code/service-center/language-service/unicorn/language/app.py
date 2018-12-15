#!/usr/bin/env python
# encoding: utf-8

from flask import Flask
from unicorn.language.detect.detect_language import detect_language_api


app = Flask(__name__)
app.register_blueprint(detect_language_api)



def main():
    app.run(host='0.0.0.0', port=8001, debug=True)
    

if __name__ == '__main__':
    main()
