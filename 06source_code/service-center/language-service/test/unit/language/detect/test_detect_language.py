#!/usr/bin/env python
# encoding: utf-8


'''
Created on 2018

@author: Administrator
'''
import unittest
from langdetect import detect,DetectorFactory
import speech_recognition as sr

from os import path
AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "english.wav")
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "french.aiff")
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "chinese.flac")

# use the audio file as the audio source
r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)  # read the entire audio file

# recognize speech using Sphinx
try:
    print("Sphinx thinks you said " + r.recognize_sphinx(audio))
except sr.UnknownValueError:
    print("Sphinx could not understand audio")
except sr.RequestError as e:
    print("Sphinx error; {0}".format(e))
    

class Test(unittest.TestCase):
    
    def testDetectLanguage(self):
        DetectorFactory.seed = 0
        lang = detect(u"这是一个最好的世界")
        self.assertEqual("zh-cn", lang)
        
        ja_lang = detect(u"今一はお前さん")
        self.assertEqual("ja", ja_lang)
        
        ar_lang = detect(u"العَرَبِيَّة‎")
        self.assertEqual("ar", ar_lang)
        
        lang2 = detect(u"ئئۇيغۇر كومپيۇتېر يېزىقى")
        print lang2
        
        

if __name__ == "__main__":
    unittest.main()