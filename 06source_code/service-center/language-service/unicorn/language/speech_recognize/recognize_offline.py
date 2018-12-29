


import logging
from flask import request
from unicorn.language.app import app


@app.route('/language/recognize/chinese/offline', methods=['POST'])
def recognize_chinese_offline():
  if not request.json or not 'wav_file' in request.json:
    abort(400)