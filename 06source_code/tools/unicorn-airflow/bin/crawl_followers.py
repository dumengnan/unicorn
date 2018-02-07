#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _load_lib
import logging
import sys
import os
import unicorn.crawler.followers as followers_main


if __name__ == '__main__':
    try:
        reload(sys)
        # unicode 转换成utf-8必须设置
        sys.setdefaultencoding("utf-8")  # @UndefinedVariable
        followers_main.main(sys.argv[1:])
    except Exception:
        logging.exception("main except")
        os._exit(1)