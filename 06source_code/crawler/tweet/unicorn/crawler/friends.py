#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import time
import os
import datetime
import logging
from unicorn.utils.get_random_key import get_twitter_auth_list
from unicorn.utils.get_random_key import get_twitter_auth
from unicorn.utils.get_config import get_config
from unicorn.utils.uni_util import get_crawl_time
from unicorn.redis.redis_bloom import BloomFilter
from unicorn.utils.file_writer import FileWriter

# api的限制速度 15分钟 15次
api_rate_limit = 15
# 关系类型
relation_type = 'focus'


def get_user_id_str(twitter, username):
    try:
        id_str = twitter.users.show(screen_name=username)["id_str"]
        return id_str
    except Exception as e:
        logging.error(" Get User " + username + " Error : %s " % e)
        return None


def crawl_friends(options):
    count = 0
    key_index = 0

    use_redis = get_config()['redis']['use']
    if use_redis:
        bf = BloomFilter(host=options.redis_host, key='users')
    
    # 记录他们的关注关系
    followers_file_writer = FileWriter(100000, "twitter_relation", options.output)
    info_file_writer = FileWriter(100000, "twitter_info", options.output)
    
    with open(options.input, "r") as f_input:
        for user in f_input:
            cursor = -1
            user = user.strip()
            twitter, count, key_index = get_twitter_auth(api_rate_limit, count, key_index)
            # 所爬取人账号的ID
            parent_id_str = get_user_id_str(twitter, user)
            if parent_id_str is None:
                continue
            while cursor != 0:
                try:
                    twitter, count, key_index = get_twitter_auth(api_rate_limit, count, key_index)

                    query = twitter.friends.list(screen_name=user, cursor=cursor, count=200, skip_status=1, \
                                                   include_user_entities=True)
                    cursor = query["next_cursor"]
                    logging.info("next cursor : " + str(cursor))
                    for follower_user in query["users"]:
                        user_info = []

                        created_at = datetime.datetime.strptime(follower_user["created_at"], "%a %b %d %H:%M:%S +0000 %Y") \
                            .strftime('%Y-%m-%d %H:%M:%S')
                        id_str = follower_user["id_str"]

                        # 对数据进行去重
                        if use_redis:
                            if bf.isContains(id_str):
                                logging.info("The user Profile Exists for " + id_str)
                                continue
                            else:
                                bf.insert(id_str)

                        name = follower_user["name"].encode("utf-8", 'ignore')
                        screen_name = follower_user["screen_name"]
                        desc = follower_user["description"]
                        favourite_count = follower_user["favourites_count"]
                        follower_count = follower_user["followers_count"]
                        friends_count = follower_user["friends_count"]
                        list_count = follower_user["listed_count"]
                        statuses_count = follower_user["statuses_count"]
                        lang = follower_user["lang"]
                        location = follower_user["location"]

                        user_info.append(id_str)
                        user_info.append(screen_name)
                        user_info.append(name)
                        user_info.append(created_at)
                        user_info.append(str(friends_count))
                        user_info.append(str(follower_count))
                        user_info.append(str(statuses_count))
                        user_info.append(str(lang))
                        user_info.append(desc.replace("\n", ""))
                        user_info.append(location)
                        user_info.append(str(list_count))
                        user_info.append(str(favourite_count))
                        
                        user_info.append("twitter")
                        user_info.append(get_crawl_time())

                        info_file_writer.append_line("\t".join(user_info))
                        followers_file_writer.append_line(parent_id_str + "\t" + relation_type + "\t" + id_str + "\t" + "twitter"  + "\t" +  get_crawl_time())

                except Exception as e:
                    count = count + 1
                    key_index = key_index + 1
                    if cursor == -1:
                        cursor = 0
                    time.sleep(api_rate_limit/len(get_twitter_auth_list()))
                    logging.error("Current User" + user + "Get Twitter Friends Error: %s" % e)


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
    options.output = config['friends']['output']
    options.redis_host = config['redis']['host']

    if not os.path.exists(options.output):
        os.makedirs(options.output)
    crawl_friends(options)
