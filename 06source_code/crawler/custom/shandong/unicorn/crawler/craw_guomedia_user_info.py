#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import requests
from bs4 import BeautifulSoup


http_proxy = 'socks5://127.0.0.1:1080'
https_proxy = 'socks5://127.0.0.1:1080'

proxy_dict = {'http': 'socks5h://127.0.0.1:1080', 'https': 'socks5h://127.0.0.1:1080'}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'x-requested-with': 'XMLHttpRequest',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9'}


def crawl_user_info():
    with open("follwers_info.txt", "w") as f_output:
        with open('follwers_list.txt', 'r') as f_input:
            f_output.write("账户名	昵称	郭文	正在关注	关注者	喜欢	直播记录" + "\n")
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
                response = requests.get(url, headers=headers, proxies=proxy_dict)
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

