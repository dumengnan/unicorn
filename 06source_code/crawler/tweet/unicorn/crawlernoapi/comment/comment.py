#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from unicorn.crawlernoapi.query import query_single_page
from unicorn.utils.select_useragent import selectUserAgent

"""
推文的评论内容
"""

INIT_URL = "https://twitter.com/{screen_name}/status/{status_id}"
COMMENT_URL = "https://twitter.com/i/{screen_name}/conversation/{status_id}?" \
    "include_available_features=1&include_entities=1&" \
    "max_position={pos}&reset_error_state=false"


def crawl_single_comment(screen_name, status_id):
    logging.info("crawl Comment for %s id %s" % (screen_name, status_id))
    pos = None
    user_agent = selectUserAgent()
    tweets = []
    try:
        while True:
            comment_tweets, pos = query_single_page(
                INIT_URL.format(screen_name=screen_name, status_id=status_id) if pos is None
                else COMMENT_URL.format(screen_name=screen_name, status_id=status_id, pos=pos),
                user_agent, pos is None)

            # 需要跳过第一次爬取的 有重复
            if str(pos).__contains__("TWEET"):
                continue

            tweets.append(comment_tweets)

            if len(comment_tweets) == 0 or pos is None:
                return tweets

    except KeyboardInterrupt:
        logging.info("Program interrupted by user. Returning tweets gathered "
                     "so far...")
    except BaseException:
        logging.exception("An unknown error occurred! Returning tweets "
                      "gathered so far.")
    return tweets


def crawl_all_comment(screen_name, status_id_list):
    comment_list = []
    for status_id in status_id_list:
        comment_list.append(crawl_single_comment(screen_name, status_id))

    return comment_list


if __name__ == '__main__':
    print crawl_single_comment("KwokMiles", "933494092322938880")