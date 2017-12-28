#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import requests
import json
import logging
import os
import re
import unicorn.utils.select_useragent as select_useragent
import unicorn.crawlernoapi.crawl_content_noapi as crawl_content_noapi
import unicorn.crawlernoapi.query as tweet_query
from datetime import datetime
from logging.config import fileConfig
from unicorn.utils.get_config import get_config
from unicorn.utils.uni_util import get_file_name, get_current_time

url = "https://www.allmytweets.net/get_tweets.php?include_rts=true&exclude_replies=false&count=200&screen_name="
fileConfig('etc/crawler_log.conf')
logger = logging.getLogger('root')
file_prefix = "uni-twitter_content-"


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
            text = content["text"].encode("utf-8").replace("\n", " ")
            device_str = r'>(.*?)<'
            device_a_text = re.findall(device_str, device, re.S | re.M)
            for device_content in device_a_text:
                device = device_content
            create_time = datetime.strptime(content["created_at"], "%a %b %d %H:%M:%S +0000 %Y").strftime(
                '%Y-%m-%d %H:%M:%S')
            if update_time and create_time <= update_time:
                # 在上次更新时间之前的 跳过
                continue

            line_data = "%s\t%s\t%s\t%s\t%s\t%d\t%d\t%s\t%s\t%s" % (
                user_id, create_time, status_id, lang, device, retweet_count, favorite_count, geo, place, text)

            f_out.write(line_data.replace("None", "") + "\n")


def crawl_oldcontent_noapi(file_name, user_name, end_date):
    print "Start Crawl  " + file_name + "   " + user_name + "  " + end_date
    start_date = datetime.strptime('20130101', "%Y%m%d").date()
    end_date = datetime.strptime(end_date, "%Y%m%d").date()

    query_condition = crawl_content_noapi.create_condition(user_name)
    all_quires = tweet_query.get_all_query(query_condition, start_date, end_date)

    with open(file_name, "a+") as f_out:
        for query in all_quires:
            for new_tweets in tweet_query.query_tweets_once(query):
                logger.info("Get Twitter " + str(len(new_tweets)))
                for tweet_content in new_tweets:
                    f_out.write(repr(tweet_content) + "\n")


# 抓取所有twitter内容
def crawl_twitter_content(options):
    input_file = options.input
    if not os.path.exists(options.output):
        os.makedirs(options.output)

    headers = {'User-Agent': select_useragent.selectUserAgent()}
    output_file = os.path.join(options.output, get_file_name(file_prefix))
    with open(input_file, "r") as input_f:
        for user_name in input_f:
            try:
                user_name = user_name.strip()
                user_url = url + user_name
                logger.info(user_url)
                response = requests.get(user_url, headers=headers, verify=False)
                results = json.loads(response.text)

                logger.info("Get Results Num : " + str(len(results)))
                if len(results) > 1:
                    write_to_file(results, output_file, options.update)
                else:
                    continue

                last_content_time = None
                # 不是更新的话 需要爬取所有的
                if not options.update:
                    while len(results) > 1:
                        max_id = results[-1]["id_str"]
                        new_url = user_url + "&max_id=" + max_id
                        logger.info("Request url is " + new_url)
                        response = requests.get(new_url, headers=headers, verify=False)
                        results = json.loads(response.text)

                        last_content_time = datetime.strptime(results[-1]["created_at"], "%a %b %d %H:%M:%S +0000 %Y").strftime(
                            '%Y%m%d')
                        write_to_file(results, output_file, options.update)

                    print last_content_time
                    # 使用直接访问的方式  爬取直接的所有twitter 内容
                    crawl_oldcontent_noapi(output_file, user_name, last_content_time)
            except Exception as e:
                print "Have Exception %s" % e


# 记录一下更新时间 下次从这个点开始更新
def write_update_file(output_path):
    output = os.path.join(os.path.dirname(output_path), "last_update")
    with open(output, "w") as update_f:
        update_time = get_current_time()
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
