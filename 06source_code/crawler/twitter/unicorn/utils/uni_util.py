#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time


def get_current_time():
    return time.strftime("%Y%m%d%H%M%S", time.localtime())


# 生成文件名
def get_file_name(prefix):
    current_time = get_current_time()

    file_name = prefix + current_time + ".bcp"
    return file_name
