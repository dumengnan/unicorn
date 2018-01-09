#!/usr/bin/env python
# -*- coding: utf-8 -*-


import datetime
import time
import logging
from twitter import *
from get_config import get_config

CONSUMER_KEY_INDEX = 0
CONSUMER_SECRET_INDEX = 1
ACCESS_TOKEN_INDEX = 2
ACCESS_SECRET_INDEX = 3

# api 统一间隔时间计量单位15分钟
api_interval_time = 900


def get_twitter_auth_list():
    twitter_auth_list = []
    config = get_config()
    keys_list = config["keys"]

    for i in range(0, len(keys_list)):
        keys_arr = keys_list[i].strip().split(",")
        consumer_key = keys_arr[CONSUMER_KEY_INDEX]
        consumer_secret = keys_arr[CONSUMER_SECRET_INDEX]
        access_key = keys_arr[ACCESS_TOKEN_INDEX]
        access_secret = keys_arr[ACCESS_SECRET_INDEX]

        twitter_auth_list.append(Twitter(auth=OAuth(access_key, access_secret, consumer_key, consumer_secret)))

    return twitter_auth_list


def get_twitter_auth(api_rate_limit, count, key_index):
    twitter_auth_list = get_twitter_auth_list()
    key_length = len(twitter_auth_list)
    start_time = datetime.datetime.now()

    twitter = twitter_auth_list[key_index % key_length]
    if count == 0:
        start_time = datetime.datetime.now()  # 统计api 耗时时间
    count = count + 1
    if count > api_rate_limit - 1:
        total_time = (datetime.datetime.now() - start_time).seconds
        if total_time < (api_interval_time / key_length):
            logging.info("Rate limit is too qucik  sleep " + str((api_interval_time / key_length) - total_time))
            time.sleep((api_interval_time / key_length) - total_time)
        key_index = key_index + 1
        count = 0
        if key_index % key_length == key_length - 1:
            logging.info("In The end sleep " + str(api_interval_time / key_length))
            time.sleep((api_interval_time / key_length))
    logging.info("The count is " + str(count))
    logging.info("The Index is " + str(key_index % key_length))

    return twitter, count, key_index
