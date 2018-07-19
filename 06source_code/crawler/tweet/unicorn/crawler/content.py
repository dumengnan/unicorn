#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import requests
import json
import logging
import unicorn.utils.select_useragent as select_useragent
import unicorn.crawlernoapi.main as noapi_main
from unicorn.crawlernoapi.tweet import Tweet
from unicorn.crawlernoapi.comment.comment import crawl_single_comment
from unicorn.utils.get_config import get_config
from unicorn.utils.uni_util import *
from unicorn.redis.redis_bloom import BloomFilter
from unicorn.utils.get_random_key import get_twitter_auth
from file_writer import FileWriter


URL = "https://www.allmytweets.net/get_tweets.php?include_rts=true& \
       exclude_replies=false&count=200&screen_name={screen_name}"

RELOAD_URL = URL + "&max_id={max_id}"

file_prefix = "uni-twitter_content-"
comment_prefix = "uni-twitter_comment-"


lines_num = 0

def get_user_register_time(username):
    try:
        twitter, count, key_index = get_twitter_auth(15, 0, 0)

        results = twitter.users.show(screen_name=username)
        created_at = datetime.strptime(results["created_at"], "%a %b %d %H:%M:%S +0000 %Y") \
            .strftime('%Y%m%d')

        return created_at
    except Exception as e:
        logging.error(" Get User " + username + " Error : %s " % e)
        return None


def crawl_content_noapi(screen_name, end_date):
    """
    利用twitter搜索技巧爬取推文
    :param screen_name:
    :param end_date:
    :return:
    """
    logging.info("Crawl %s Tweets no Api to %s" % (screen_name, end_date))
    register_time = get_user_register_time(screen_name)
    if register_time is None or register_time < '20130101':
        register_time = '20130101'
    start_date = datetime.strptime(register_time, "%Y%m%d").date()
    end_date = datetime.strptime(end_date, "%Y%m%d").date()

    return noapi_main.query_content(screen_name, start_date, end_date)


def crawl_content_withapi(screen_name, options):
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

            if options.update and last_tweet_time < options.update:
                    return content_list, last_tweet_time
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


def write_content_to_file(content_file_writer, tweet_list, screen_name):
    """
    将所有的推文内容写入到文件
    :param content_file:
    :param tweet_list:
    :return:
    """
    social_type = "twitter"
    redis_host = get_config()['redis']['host']
    bf = BloomFilter(host=redis_host, key='status')
    for content in tweet_list:
        # 对数据进行去重
        if bf.isContains(content.status_id):
            logging.info("The status Exists for " + content.status_id)
            continue
        else:
            bf.insert(content.status_id)
            content_file_writer.append_line(repr(content) + "\t" + screen_name + "\t" + social_type + "\t" + \
                            get_crawl_time())


def write_comment_to_file(source_status_id, comments_file_writer, comment_list):
    """
    将所有的评论内容写入到文件
    :param source_status_id:
    :param file_name:
    :param comment_list:
    :return:
    """
    for comment in comment_list:
        for single_comment in comment:
            line = single_comment.status_id + "\treply\t" + source_status_id
            comments_file_writer.append_line(line)


def crawl_comments(options, screen_name, status_id_list, content_file_writer):
    """
    抓取所有的评论内容
    :param options:
    :param screen_name:
    :param status_id_list:
    :param content_file:
    :return:
    """
    comments_file_writer =  FileWriter(100000, "twitter_comments", options.output)
    for status_id in status_id_list:
        comment_list = crawl_single_comment(screen_name, status_id)
        write_comment_to_file(status_id, comments_file_writer, comment_list)
        for comm_list in comment_list:
            write_content_to_file(content_file_writer, comm_list, screen_name)


def crawl_twitter_content(options):
    """
    crawl All Twitter content
    :param options:
    :return:
    """
    content_file_writer = FileWriter(100000, "twitter_content", options.output) 
    with open(options.input, "r") as input_f:
        for user_name in input_f:
            try:
                pre_tweets, last_tweet_time = crawl_content_withapi(user_name.strip(), options)
                tweet_list = trans_json_to_tweet(pre_tweets)
                logging.info("Get {} Tweets From Api".format(str(len(tweet_list))))
                write_content_to_file(content_file_writer, tweet_list, user_name)

                if options.all and len(tweet_list) >= 3200:
                    logging.info("Start Crawl Status Not Use Api!")
                    new_tweet_list = crawl_content_noapi(user_name.strip(), last_tweet_time)
                    write_content_to_file(content_file_writer, new_tweet_list, user_name)
                    logging.info("Get {} Tweets From No Api".format(str(len(new_tweet_list))))
                    tweet_list.append(new_tweet_list)

                if options.comment:
                    status_id_list = get_status_id_list(tweet_list)
                    logging.info("Start Crawl Comment" + str(len(status_id_list)))
                    crawl_comments(options, user_name.strip(), status_id_list, content_file_writer)

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

    parser.add_argument("--i", "--input-file", dest="input", type=str, help="The input file")

    parser.add_argument("--u", "--update_time", dest="update", type=str,
                        help="Last update time %Y%m%d%H%M%S")

    parser.add_argument("--a", "--all", dest="all", type=bool, default=False,
                        help="crawl all tweet no use api")

    parser.add_argument("--c", "--comment", dest="comment", type=bool, default=False,
                        help="crawl all tweet comment no use api")

    options = get_options(parser)
    progress_start = time.time()
    crawl_twitter_content(options)
    progress_end = time.time()
    logging.info("Crawl Cost Time " + str(progress_end - progress_start) + "  s")
