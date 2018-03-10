#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import selenium
import json
import logging
import os
import sys
import unicorn.utils.select_useragent as select_useragent
from time import time
from unicorn.crawlernoapi.tweet import Tweet
from unicorn.utils.get_config import get_config
from unicorn.utils.uni_util import *
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests

url = "https://www.guo.media/"

http_proxy = 'http://192.168.1.3:8119'
https_proxy = 'http://192.168.1.3:8119'

proxy_dict = {
    "http": http_proxy,
    "https": https_proxy
}


def crawl_media_info(options):
    """
    crawl All Twitter content
    :param options:
    :return:
    """
    output_dir = options.output
    current_outputdir = os.path.join(output_dir, get_current_time())
    stat_file = os.path.join(output_dir, "stat.csv")

    start_time = options.start
    end_time = options.end

    with open(options.input, "r") as input_f:
        for user_name in input_f:
            try: 
                user_name = user_name.strip()
                take_info(url, user_name, options.screen_size)

            except Exception as e:
                print "Have Exception %s" % e


def take_info(screen_size):
    options = webdriver.ChromeOptions()

    options.add_argument('--proxy-server=%s' % '192.168.1.3:8119')
    # options.add_argument('--user-data-dir=C:/Users/Administrator/AppData/Local/Google/Chrome/User Data/Default')
    options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    # options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("window-size="+screen_size)
    browser = webdriver.Chrome(chrome_options=options, executable_path='tools/chromedriver.exe')

    browser.get(url)
    
    username = browser.find_element_by_name('username_email')
    password = browser.find_element_by_name('password')

    username.send_keys("demohaha")
    password.send_keys("demohaha")

    browser.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div/div[2]/form/div[1]/div[1]/input[3]").click()
    browser.get("https://www.guo.media/followers.php?username=milesguo")

    time.sleep(7)
    elements = browser.find_elements_by_class_name("pro_thumb")
    for element in elements:
        a = element.find_element_by_tag_name("a")
        img = element.find_element_by_tag_name("img")
        print a.get_attribute('href') + "\t" + img.get_attribute("src") + "\t" + img.get_attribute('alt')

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
               'content-type':'application/x-www-form-urlencoded; charset=UTF-8',
               'accept': 'application/json, text/javascript, */*; q=0.01',
               'x-requested-with': 'XMLHttpRequest',
               'accept-encoding':'gzip, deflate, br',
               'accept-language':'zh-CN,zh;q=0.9'}

    s = requests.Session()
    for cookie in browser.get_cookies():
        s.cookies.set(cookie['name'], cookie['value'])

    offset = 1
    while offset<200:
        data = {}
        data["get"] = "followers"
        data["uid"] = "356"
        data["offset"] = offset
        print s.post("https://www.guo.media/includes/ajax/data/load.php", headers=headers,
                      data=data, proxies=proxy_dict).text
        offset = offset+1



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

    #options = get_options(parser)
    progress_start = time.time()
    #crawl_twitter_content(options)
    progress_end = time.time()
    logging.info("Crawl Cost Time " + str(progress_end - progress_start) + "  s")


if __name__ == '__main__':
    # main(sys.argv[1:])
    take_info("1920*1080")
    # take_screenshot('https://twitter.com/HanaCheney/status/946576449900773376', '1.png')
