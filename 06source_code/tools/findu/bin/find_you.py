#!/usr/bin/env python
# encoding: utf-8

import _load_lib
import sys
import logging
import os

from unicorn.find.find_virtual_you import main as find_u_main

if __name__ == '__main__':
    try:
        reload(sys)
        # unicode 转换成utf-8必须设置
        sys.setdefaultencoding("utf-8")  # @UndefinedVariable
        find_u_main.main(sys.argv[1:])
    except Exception, ex:
        logging.exception("main except", ex)
        os._exit(1)
