


import logging
from flask import request
from unicorn.language.app import app

from LanguageModel import ModelLanguage
from SpeechModel251 import ModelSpeech

datapath='data/train_data/'
ms = ModelSpeech(datapath)
ms.LoadModel('data/speech_model/speech_model251_e_0_step_12000.model')

ml = ModelLanguage('data/model_language/')
ml.LoadModel()

@app.route('/language/recognize/chinese/offline', methods=['POST'])
def recognize_chinese_offline():
    if not request.json or not 'wav_file' in request.json:
        abort(400)
    wav_file = request.json.get("wav_file")
    str_pinyin = ms.RecognizeSpeech_FromFile(wav_file)
    str_text = ml.SpeechToText(str_pinyin)
    
    logging.info("Detect Speech pinyin " + str_pinyin + ", speech text is " + str_text)
    return jsonify({'pinyin': str_pinyin, 'text': str_text})
  