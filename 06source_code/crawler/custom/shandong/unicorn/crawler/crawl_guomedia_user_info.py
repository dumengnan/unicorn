#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import requests
import guo_media_util
from bs4 import BeautifulSoup


def crawl_user_info():
    with open("follwers_info.txt", "a+") as f_output:
        with open('follwers_list.txt', 'r') as f_input:
            for line in f_input:
                i = 0
                line_arr = line.strip().split("\t")
                url = line_arr[0]
                user_name = url.split("/")[-1]
                nick_name = ""
                if len(line_arr) == 2:
                    nick_name = line_arr[1]
                else:
                    nick_name = user_name
                response = guo_media_util.request_with_retry(url)
                if response.status_code != 200:
                    print "request failed " + url
                    continue
                soup = BeautifulSoup(response.text, 'lxml')
                profile = soup.find('div', class_='profile-tabs-wrapper')
                value_list = list()
                value_list.append(user_name)
                value_list.append(nick_name)
                if profile is None:
                    print "profile is None " + url
                    continue
                for child_li in profile.find_all('li'):
                    if i > 4:
                        break
                    i = i + 1
                    value = child_li.find('span', class_='text-underline')
                    value_list.append(value.get_text())
                print value_list
                f_output.write("\t".join(value_list) + "\n")


def main(args):
    parser = argparse.ArgumentParser(description=
                                     "Simple Twitter Profile Analyzer", usage='--input <twitter_user_input_file>')

    parser.add_argument("--i", "--input", dest="input", type=str,
                        default="twitter_user.txt", help="The input file")

    options = parser.parse_args()


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    crawl_user_info()

