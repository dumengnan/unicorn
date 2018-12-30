#!/usr/bin/env python3
# encoding: utf-8


import logging
from flask import request, Blueprint, abort, jsonify

from LanguageModel import ModelLanguage
from SpeechModel251 import ModelSpeech

data_path = 'data/train_data/'
ms = ModelSpeech(data_path)
ms.LoadModel('data/speech_model/speech_model251_e_0_step_12000.model')

ml = ModelLanguage('data/model_language/')
ml.LoadModel()

detect_speech_api = Blueprint('detect_language_api', __name__,
                              template_folder='templates')


@detect_speech_api.route('/language/recognize/chinese/offline',
                         methods=['POST'])
def recognize_chinese_offline():
    if not request.json or 'wav_file' not in request.json:
        abort(400)
    wav_file = request.json.get("wav_file")
    str_pinyin = ms.RecognizeSpeech_FromFile(wav_file)
    str_text = ml.SpeechToText(str_pinyin)

    logging.info(
        "Detect Speech pinyin " + str_pinyin + ", speech text is " + str_text)
    return jsonify({'pinyin': str_pinyin, 'text': str_text})
