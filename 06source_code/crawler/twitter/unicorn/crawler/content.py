#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import requests
import json
import logging
import os
import time
import re
import unicorn.utils.select_useragent as select_useragent
import datetime
from logging.config import fileConfig
from unicorn.utils.get_config import get_config


url = "https://www.allmytweets.net/get_tweets.php?include_rts=true&exclude_replies=false&count=200&screen_name="
fileConfig('etc/crawler_log.conf')
logger = logging.getLogger('root')


# 结果写入到文件中
def write_to_file(results, file_name, update_time):
    if update_time:
        file_name = "Twitter_Update.txt"

    with open(file_name, "a+") as f_out:
        for content in results:
            user_id = content["user"]["id_str"]
            status_id = content["id_str"]
            lang = content["lang"]
            geo = content["geo"]
            place = content["place"]
            retweet_count = content["retweet_count"]
            favorite_count = content["favorite_count"]
            device = content["source"]
            text = content["text"].encode("utf-8").replace("\n"," ")
            device_str = r'>(.*?)<'
            device_a_text = re.findall(device_str, device, re.S|re.M)
            for device_content in device_a_text:
                device = device_content
            create_time = datetime.datetime.strptime(content["created_at"], "%a %b %d %H:%M:%S +0000 %Y").strftime('%Y-%m-%d %H:%M:%S')
            if update_time and create_time <= update_time:
                # 在上次更新时间之前的 跳过
                continue
            f_out.write("%s\t%s\t%s\t%s\t%s\t%d\t%d\t%s\t%s\t%s" % (user_id, create_time, status_id, lang, device, retweet_count, favorite_count, geo, place, text) + "\n")


# 抓取所有twitter内容
def crawl_twitter_content(options):
    input_file = options.input
    if not os.path.exists(options.output):
        os.makedirs(options.output)

    headers = {'User-Agent': select_useragent.selectUserAgent()}
    with open(input_file, "r") as input_f:
        for user_name in input_f:
            try:
                user_name = user_name.strip()
                file_name = os.path.join(options.output, user_name)
                user_url = url + user_name
                logger.info(user_url)
                response = requests.get(user_url, headers=headers, verify=False)
                results = json.loads(response.text)
                logger.info("Get Results Num : " + str(len(results)))
                if len(results) > 1:
                    write_to_file(results, file_name, options.update)
                else:
                    continue
                # 不是更新的话 需要爬取所有的
                if not options.update:
                    while len(results) > 1:
                        max_id = results[-1]["id_str"]
                        new_url = user_url + "&max_id=" + max_id
                        logger.info("Request url is " + new_url)
                        response = requests.get(new_url, headers=headers, verify=False)
                        results = json.loads(response.text)
                        write_to_file(results, file_name, options.update)
            except Exception as e:
                print "Have Exception %s" % e


# 记录一下更新时间 下次从这个点开始更新
def write_update_file(output_path):
    output = os.path.join(os.path.dirname(output_path), "last_update")
    with open(output, "w") as update_f:
        update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        update_f.write(update_time + "\n")


def main(args):
    parser = argparse.ArgumentParser(description=
                                     "Simple Twitter Profile Analyzer", usage='--input <twitter_user_input_file>')

    parser.add_argument("--i", "--input", dest="input", type=str,
                        default="twitter_user.txt", help="The input file")

    parser.add_argument("--o", "--output", dest="output", type=str,
                        default="twitter_profile_analyzer.txt", help="analyzer result txt")

    parser.add_argument("--u", "--update_time", dest="update", type=str,
                        help="Last update time")

    config = get_config()
    output_path = config['content']['output']

    options = parser.parse_args()
    options.output = output_path
    crawl_twitter_content(options)
    write_update_file(output_path)


