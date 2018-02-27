#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import time
from datetime import datetime


def get_current_time():
    return time.strftime("%Y%m%d%H%M%S", time.localtime())


# 生成文件名
def get_file_name(prefix):
    current_time = get_current_time()

    file_name = prefix + current_time + ".bcp"
    return file_name


def format_content_time_to_day(time_str):
    """
    格式化时间到天
    :param time_str:  eg.Thu Nov 23 16:30:46 +0000 2017
    :return: 20171223
    """
    return datetime.strptime(time_str, "%a %b %d %H:%M:%S +0000 %Y").strftime(
        '%Y%m%d')


def format_content_time_to_minute(time_str):
    """
    格式化推文时间
    :param time_str:  eg.Thu Nov 23 16:30:46 +0000 2017
    :return: 20171223
    """
    return datetime.strptime(time_str, "%a %b %d %H:%M:%S +0000 %Y")


def parse_device_from_str(source_str):
    """
    解析设备名称 从字符串中
    :param source_str: <a>Twitter for iPhone</a>
    :return:  Twitter for iPhone
    """
    device = ""
    device_str = r'>(.*?)<'
    device_a_text = re.findall(device_str, source_str, re.S | re.M)
    for device_content in device_a_text:
        device = device_content

    return device


def xstr(string):
    return '' if string is None else str(string)