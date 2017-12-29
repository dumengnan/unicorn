#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import requests
import json
import logging
import os
import unicorn.utils.select_useragent as select_useragent
import unicorn.crawlernoapi.main as noapi_main
from unicorn.crawlernoapi.tweet import Tweet
from unicorn.crawlernoapi.comment.comment import crawl_single_comment
from unicorn.utils.get_config import get_config
from unicorn.utils.uni_util import *

URL = "https://www.allmytweets.net/get_tweets.php?include_rts=true& \
       exclude_replies=false&count=200&screen_name={screen_name}"

RELOAD_URL = URL + "&max_id={max_id}"

file_prefix = "uni-twitter_content-"
comment_prefix = "uni-twitter_comment-"


def crawl_content_noapi(screen_name, end_date):
    """
    利用twitter搜索技巧爬取推文
    :param screen_name:
    :param end_date:
    :return:
    """
    logging.info("Crawl %s Tweets no Api to %s" % (screen_name, end_date))
    start_date = datetime.strptime('20130101', "%Y%m%d").date()
    end_date = datetime.strptime(end_date, "%Y%m%d").date()

    return noapi_main.query_content(screen_name, start_date, end_date)


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
    last_tweet_time = get_current_time()

    try:
        while True:
            response = requests.get(
                URL.format(screen_name=screen_name) if max_id is None
                else RELOAD_URL.format(screen_name=screen_name, max_id=max_id),
                headers=headers, verify=False)

            results = json.loads(response.text)
            max_id = results[-1]["id_str"]
            last_tweet_time = format_content_time_to_day(results[-1]["created_at"])
            content_list.append(results)
            if len(results) <= 1 or max_id is None:
                return content_list, last_tweet_time
    except Exception:
        logging.exception("An unknown error occurred! Returning tweets "
                         "gathered so far.")
    return content_list, last_tweet_time


def trans_json_to_tweet(tweet_json_arr):
    """
    将json 字符串解析 转换成twitter instance
    :param tweet_json_arr: json arr for twitter content
    :return:  tweet instance list
    """
    logging.info("Trans Json To Tweet Length {}" .format(str(len(tweet_json_arr))))
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


def write_comment_to_file(source_status_id, file_name, comment_list):
    """
    将所有的评论内容写入到文件
    :param source_status_id:
    :param file_name:
    :param comment_list:
    :return:
    """
    with open(file_name, "a+") as f_comment:
        for comment in comment_list:
            for single_comment in comment:
                line = single_comment.status_id + "\treply\t" + source_status_id
                f_comment.write(line + "\n")


def crawl_comments(options, screen_name, status_id_list, content_file):
    """
    抓取所有的评论内容
    :param options:
    :param screen_name:
    :param status_id_list:
    :param content_file:
    :return:
    """
    comments_file = os.path.join(options.output, get_file_name(comment_prefix))
    for status_id in status_id_list:
        comment_list = crawl_single_comment(screen_name, status_id)
        write_comment_to_file(status_id, comments_file, comment_list)
        write_content_to_file(content_file, comment_list)


def crawl_twitter_content(options):
    """
    crawl All Twitter content
    :param options:
    :return:
    """
    content_file = os.path.join(options.output, get_file_name(file_prefix))
    with open(options.input, "r") as input_f:
        for user_name in input_f:
            try:
                pre_tweets, last_tweet_time = crawl_content_withapi(user_name.strip())
                tweet_list = trans_json_to_tweet(pre_tweets)
                logging.info("Get {} Tweets From Api".format(str(len(tweet_list))))
                write_content_to_file(content_file, tweet_list)

                if options.all and len(tweet_list) >= 3200:
                    new_tweet_list = crawl_content_noapi(user_name.strip(), last_tweet_time)
                    write_content_to_file(content_file, new_tweet_list)
                    logging.info("Get {} Tweets From No Api".format(str(len(tweet_list))))
                    tweet_list.append(new_tweet_list)

                if options.comment:
                    status_id_list = get_status_id_list(tweet_list)
                    crawl_comments(options, user_name.strip(), status_id_list, content_file)

            except Exception as e:
                print "Have Exception %s" % e


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

    parser.add_argument("--o", "--output", dest="output", type=str,
                        default="twitter_profile_analyzer.txt", help="analyzer result txt")

    parser.add_argument("--u", "--update_time", dest="update", type=str,
                        help="Last update time")

    parser.add_argument("--a", "--all", dest="all", type=bool, default=False,
                        help="crawl all tweet no use api")

    parser.add_argument("--c", "--comment", dest="comment", type=bool, default=False,
                        help="crawl all tweet comment no use api")

    options = get_options(parser)
    crawl_twitter_content(options)
