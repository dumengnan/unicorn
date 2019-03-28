#!/usr/bin/env python3
# encoding: utf-8


'''
Created on 2018

@author: Administrator
'''
import unittest
from langdetect import detect, DetectorFactory


class Test(unittest.TestCase):

    def testDetectLanguage(self):
        DetectorFactory.seed = 0
        lang = detect(u"这是一个最好的世界")
        self.assertEqual("zh-cn", lang)

        ja_lang = detect(u"今一はお前さん")
        self.assertEqual("ja", ja_lang)

        ar_lang = detect(u"العَرَبِيَّة‎")
        self.assertEqual("ar", ar_lang)

        ar_lang2 = detect(u"ئئۇيغۇر كومپيۇتېر يېزىقى")
        self.assertEqual("ar", ar_lang2)


if __name__ == "__main__":
    unittest.main()
