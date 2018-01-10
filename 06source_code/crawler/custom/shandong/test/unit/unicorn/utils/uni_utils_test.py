#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest as unittest
from unicorn.utils.uni_util import *


class UtilTest(unittest.TestCase):
    def test_parse_device_from_str(self):
        source_str = "<a>Twitter for iPhone</a>"
        device = parse_device_from_str(source_str)
        self.assertEqual("Twitter for iPhone", device)

    def test_format_tweet_content_time_to_day(self):
        create_time = "Thu Nov 23 16:30:46 +0000 2017"
        time_str = format_content_time_to_day(create_time)
        self.assertEqual("20171123", time_str)

    def test_format_tweet_time_to_minute(self):
        create_time = "Thu Nov 23 16:30:46 +0000 2017"
        minute_date = format_content_time_to_seconds(create_time)
        self.assertEqual("2017-11-23 16:30:46", minute_date.strftime("%Y-%m-%d %H:%M:%S"))
