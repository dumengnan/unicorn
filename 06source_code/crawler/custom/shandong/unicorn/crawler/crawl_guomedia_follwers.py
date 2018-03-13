#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import time
from bs4 import BeautifulSoup
from unicorn.utils.get_config import get_config
from unicorn.utils.uni_util import *
import guo_media_util


def take_info(output_file, uid):
    f = open(output_file, 'w')
    f.write("url    昵称   uid    imgurl" + "\n")

    offset = 0
    while offset < 3300:
        data = dict()
        data["get"] = "followers"
        data["uid"] = uid
        data["offset"] = offset
        request_with_cookie = guo_media_util.get_requests_with_cookie()
        contents = guo_media_util.request_json_data(request_with_cookie, data)
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
    print "hello "
    print args
    crawl_uid = args.uid
    output_file = args.output

    print crawl_uid, output_file
    take_info(output_file, crawl_uid)

if __name__ == '__main__':
    take_info('follwers.txt', '356')
