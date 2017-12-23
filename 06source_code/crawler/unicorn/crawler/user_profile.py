#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import time
import os
import datetime
import logging
from logging.config import fileConfig
from unicorn.utils.get_random_key import get_twitter_auth
from unicorn.utils.get_random_key import get_twitter_auth_list
from unicorn.utils.get_config import get_config

fileConfig('etc/crawler_log.conf')
logger = logging.getLogger('root')

# api的限制速度 15分钟 900次
api_rate_limit = 900


def crawl_user_profile(options):
    count = 0
    key_index = 0
    with open(options.input, "r") as f_input:
        with open(os.path.join(options.output, "user_profile.txt"), "w") as f_output:
            for user in f_input:
                try:
                    user_info = []
                    user = user.strip()
                    twitter, count, key_index = get_twitter_auth(api_rate_limit, count, key_index)
                    results = twitter.users.show(screen_name=user)
                    created_at = datetime.datetime.strptime(results["created_at"], "%a %b %d %H:%M:%S +0000 %Y") \
                                                  .strftime('%Y-%m-%d %H:%M:%S')
                    id_str = results["id_str"]
                    name = results["name"].encode("utf-8", 'ignore')
                    screen_name = results["screen_name"]
                    desc = results["description"]
                    favourite_count = results["favourites_count"]
                    follower_count = results["followers_count"]
                    friends_count = results["friends_count"]
                    list_count = results["listed_count"]
                    statuses_count = results["statuses_count"]

                    user_info.append(id_str)
                    user_info.append(name)
                    user_info.append(screen_name)
                    user_info.append(created_at)
                    user_info.append(desc.replace("\n", ""))
                    user_info.append(str(favourite_count))
                    user_info.append(str(follower_count))
                    user_info.append(str(friends_count))
                    user_info.append(str(list_count))
                    user_info.append(str(statuses_count))

                    f_output.write("\t".join(user_info) + "\n")

                except Exception as e:
                    count = count + 1
                    key_index = key_index + 1
                    time.sleep(api_rate_limit/len(get_twitter_auth_list()))
                    logger.error("Get Twitter Account Error: %s" % e)


def main(args):
    parser = argparse.ArgumentParser(description=
                                     "Get Twitter account detail info",
                                     usage='--input <twitter_user_input_file> --output <output_file_name>')

    parser.add_argument("--i", "--input", dest="input", type=str,
                        default="twitter_user.txt", help="The input file")

    parser.add_argument("--o", "--output", dest="output", type=str,
                        help="The output file")

    options = parser.parse_args()
    config = get_config()
    options.output = config['profile']['output']

    if not os.path.exists(options.output):
        os.makedirs(options.output)

    crawl_user_profile(options)
