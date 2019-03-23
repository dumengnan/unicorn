#!/usr/bin/env python3
# encoding: utf-8


import logging
import os
from flask import request, Blueprint, abort, jsonify
from werkzeug import secure_filename

from LanguageModel import ModelLanguage
from SpeechModel251 import ModelSpeech

data_path = 'data/train_data/'
ms = ModelSpeech(data_path)
ms.LoadModel('data/speech_model/speech_model251_e_0_step_12000.model')

ml = ModelLanguage('data/model_language/')
ml.LoadModel()

detect_speech_api = Blueprint('detect_language_api', __name__,
                              template_folder='templates')

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@detect_speech_api.route('/language/recognize/chinese/offline',
                         methods=['POST'])
def recognize_chinese_offline():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join('data/upload', filename))
        str_pinyin = ms.RecognizeSpeech_FromFile(
            os.path.join('data/upload', filename))
        str_text = ml.SpeechToText(str_pinyin)

        logging.info(
            "Detect Speech pinyin " + str_pinyin + ", speech text is " + str_text)
        return jsonify({'pinyin': str_pinyin, 'te  xt': str_text})
