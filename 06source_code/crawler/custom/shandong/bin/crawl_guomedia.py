#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _load_lib
import logging
import sys
import os
import argparse
from unicorn.crawler.crawl_guomedia_follwers import main as followers_main
from unicorn.crawler.crawl_guomedia_status import main as status_main
from unicorn.crawler.crawl_guomedia_user_info import main as userinfo_main


def get_parser():
    parser = argparse.ArgumentParser(description="crawl guo media")
    subparsers = parser.add_subparsers(title='subcommands', help='crawl follwer sub command')
    parser_follower = subparsers.add_parser('follower')
    parser_follower.add_argument("--o", "--output", dest="output", type=str, help="output file")
    parser_follower.add_argument("--u", "--uid", dest="uid", type=str, help="crawl user uid")

    parser_follower.set_defaults(func=followers_main)
    parser_status = subparsers.add_parser('status')
    parser_status.add_argument("--i", "--input", dest="input", type=str, help="input file")
    parser_status.add_argument("--o", "--output", dest="output", type=str, help="status output dir")
    parser_status.set_defaults(func=status_main)

    parser_userinfo = subparsers.add_parser('userinfo')
    parser_userinfo.add_argument("--i", "--input", dest="input", type=str, help="input file")
    parser_userinfo.add_argument("--o", "--output", dest="output", type=str, help="user info output file")
    parser_userinfo.set_defaults(func=userinfo_main)

    return parser

if __name__ == '__main__':
    try:
        reload(sys)
        # unicode 转换成utf-8必须设置
        sys.setdefaultencoding("utf-8")  # @UndefinedVariable
        parser = get_parser()
        args = parser.parse_args(sys.argv[1:])
        args.func(args)
    except Exception:
        logging.exception("main except")
        os._exit(1)
