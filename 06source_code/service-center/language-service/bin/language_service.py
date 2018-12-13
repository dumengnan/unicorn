#!/usr/bin/env python
# encoding: utf-8

import _load_lib
import sys
import logging
import os

from unicorn.language.app\
    import main as languae_main

if __name__ == '__main__':
    try:
        languae_main()
    except Exception as ex:
        logging.exception("main except")
        os._exit(1)
