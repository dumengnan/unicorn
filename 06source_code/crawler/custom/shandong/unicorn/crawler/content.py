#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import requests
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

URL = "https://www.allmytweets.net/get_tweets.php?include_rts=true& \
       exclude_replies=false&count=200&screen_name={screen_name}"

RELOAD_URL = URL + "&max_id={max_id}"

file_prefix = "uni-twitter_content-"
comment_prefix = "uni-twitter_comment-"


def crawl_content_withapi(screen_name):
    """
    使用API 爬取推文内容
    :param screen_name: user screen name
    :return: twitter list
    """
    logging.info("Crawl %s Tweets  with Api" % screen_name)
    headers = {'User-Agent': select_useragent.selectUserAgent()}
    max_id = None
    content_list = []

    try:
        while True:
            response = requests.get(
                URL.format(screen_name=screen_name) if max_id is None
                else RELOAD_URL.format(screen_name=screen_name, max_id=max_id),
                headers=headers, verify=False)

            results = json.loads(response.text)
            max_id = results[-1]["id_str"]
            content_list.append(results)
            if len(results) <= 1 or max_id is None:
                return content_list
    except Exception:
        logging.exception("An unknown error occurred! Returning tweets "
                          "gathered so far.")
    return content_list


def get_tweet_between_time(tweet_json_arr, start_time, end_time):
    """
    将json 字符串解析 转换成twitter instance
    :param tweet_json_arr: json arr for twitter content
    :return:  tweet instance list
    """
    logging.info("Trans Json To Tweet Length {}".format(str(len(tweet_json_arr))))
    tweet_list = []
    for tweet_json in tweet_json_arr:
        for content in tweet_json:
            user_id = content["user"]["id_str"]
            status_id = content["id_str"]
            lang = content["lang"]
            geo = content["geo"]
            place = content["place"]
            retweet_count = str(content["retweet_count"])
            favorite_count = str(content["favorite_count"])
            source = content["source"]
            device = parse_device_from_str(source)
            create_time = format_content_time_to_minute(content["created_at"])

            text = content["text"].encode("utf-8").replace("\n", " ")

            tweet = Tweet(user_id, create_time, status_id, \
                          lang, device, retweet_count, favorite_count, geo, place, text)
            # 根据时间段筛选推文
            if create_time > start_time and create_time < end_time:
                tweet_list.append(tweet)

    return tweet_list


def get_status_id_list(tweet_list):
    """
    获得所有的推文id
    :param tweet_list:
    :return:
    """
    id_list = []
    for content in tweet_list:
        id_list.append(content.status_id)
    return id_list


def write_content_to_file(content_file, tweet_list):
    """
    将所有的推文内容写入到文件
    :param content_file:
    :param tweet_list:
    :return:
    """
    with open(content_file, "a+") as f_out:
        for content in tweet_list:
            f_out.write(repr(content) + "\n")


def crawl_twitter_content(options):
    """
    crawl All Twitter content
    :param options:
    :return:
    """
    content_file = os.path.join(options.output, get_file_name(file_prefix))
    start_time = options.start
    end_time = options.end

    with open(options.input, "r") as input_f:
        for user_name in input_f:
            try:
                pre_tweets = crawl_content_withapi(user_name.strip())
                tweet_list = get_tweet_between_time(pre_tweets, start_time, end_time)
                write_content_to_file(content_file, tweet_list)

                status_id_list = get_status_id_list(tweet_list)

                # 截图
                for status_id in status_id_list:
                    url = "https://twitter.com/" + user_name.strip() + "/status/" + status_id
                    take_screenshot(url, status_id + ".png")

            except Exception as e:
                print "Have Exception %s" % e


def take_screenshot(url, file_name):
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=%s' % '127.0.0.1:1080')
    options.add_argument('--user-data-dir=C:/Users/Administrator/AppData/Local/Google/Chrome/User Data/Default')
    options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    browser = webdriver.Chrome(chrome_options=options)

    browser.set_window_size(1920, 1440)
    browser.get(url)

    browser.save_screenshot(file_name)

    browser.close()


def get_options(parser):
    """
    解析 所有的参数
    :param parser:  arg parser
    :return:  arg map
    """
    config = get_config()
    output_path = config['content']['output']
    options = parser.parse_args()
    options.output = output_path

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

    options = get_options(parser)
    progress_start = time.time()
    crawl_twitter_content(options)
    progress_end = time.time()
    logging.info("Crawl Cost Time " + str(progress_end - progress_start) + "  s")


if __name__ == '__main__':
    main(sys.argv[1:])
    # take_screenshot('https://twitter.com/HanaCheney/status/946576449900773376', '1.png')