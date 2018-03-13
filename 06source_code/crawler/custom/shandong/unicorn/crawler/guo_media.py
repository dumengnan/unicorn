#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
from time import time
from bs4 import BeautifulSoup
from unicorn.utils.get_config import get_config
from unicorn.utils.uni_util import *
import guo_media_util
import sys


def take_info():
    f = open('follwers_list', 'w')
    f.write("url    昵称   uid    imgurl" + "\n")

    offset = 0
    while offset < 3300:
        data = dict()
        data["get"] = "followers"
        data["uid"] = "356"
        data["offset"] = offset
        contents = guo_media_util.request_data(data)
        if 'data' not in contents:
            continue
        contents_html = contents['data']
        soup = BeautifulSoup(contents_html, 'lxml')
        profile = soup.find_all('div', class_='side_profile')

        time.sleep(0.5)
        for child_ele in profile:
            value_list = []
            pro_thumb = child_ele.find('div', class_='pro_thumb')
            value_list.append(pro_thumb.find('a')['href'])
            value_list.append(pro_thumb.find('img')['alt'])

            uid = child_ele.find('div', class_='admin_detail').find('span', class_='name js_user-popover')['data-uid']
            value_list.append(uid)
            value_list.append(pro_thumb.find('img')['src'])

            f.write("\t".join(value_list) + "\n")

        print "offset is " + str(offset)
        offset = offset + 1


def get_options(parser):
    """
    解析 所有的参数
    :param parser:  arg parser
    :return:  arg map
    """
    config = get_config()
    output_path = config['content']['output']
    screen_size = config['screen_size']
    options = parser.parse_args()
    options.output = output_path
    options.screen_size = screen_size

    return options


def main(args):
    parser = argparse.ArgumentParser(description=
                                     "Simple Twitter Profile Analyzer", usage='--input <twitter_user_input_file>')

    parser.add_argument("--i", "--input", dest="input", type=str,
                        default="twitter_user.txt", help="The input file")

    parser.add_argument("--s", "--start", dest="start", type=str, help="crawl start time")

    parser.add_argument("--e", "--end", dest="end", type=str,
                        help="crawl end time")

    parser.add_argument("--o", "--output", dest="output", type=str,
                        help="output dir")

    # options = get_options(parser)
    progress_start = time.time()
    # crawl_twitter_content(options)
    progress_end = time.time()
    logging.info("Crawl Cost Time " + str(progress_end - progress_start) + "  s")


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    # main(sys.argv[1:])
    take_info()
    # take_screenshot('https://twitter.com/HanaCheney/status/946576449900773376', '1.png')
