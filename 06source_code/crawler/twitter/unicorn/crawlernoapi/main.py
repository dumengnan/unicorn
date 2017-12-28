#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is a command line application that allows you to scrape twitter!
"""

from argparse import ArgumentParser
import logging
import time
import os
from datetime import datetime, date

from query import query_all_tweets


def create_condition(user_name):
    base_condition = "from:" + user_name
    return base_condition


def write_to_file(file_path, tweet_contents):
    if len(tweet_contents) > 0:
        f_out = open(file_path, "w")
        for tweet in tweet_contents:
            # only record the newer twitter content
            f_out.write(tweet.to_bcp_line() + "\n")


def query_content(user_name, start_date, end_date):
    """
    一次性查询在时间段内的所有推文
    :param user_name: screen_name
    :param start_date:  eg.20170101
    :param end_date:    eg.20170909
    :return:  list of tweets
    """
    query_condition = create_condition(user_name)
    query_result_tweets = query_all_tweets(query_condition, start_date, end_date)
    return query_result_tweets


def get_user_list(accounts_file):
    user_list = []
    with open(accounts_file, "r") as input_user_f:
        for line in input_user_f:
            user_name = line.strip()
            user_list.append(user_name)

    return user_list


def get_output_folder():
    current_time = time.strftime("%Y%m%d", time.localtime())
    if not os.path.exists(current_time):
        os.mkdir(current_time)
    return current_time


def get_start_end_date(args):
    start_date = datetime.strptime(args.start, "%Y%m%d").date()
    end_date = date.today()
    if args.end is not None:
        end_date = datetime.strptime(args.end, "%Y%m%d").date()

    print start_date, end_date
    return start_date, end_date


def crawl_content(args):
    user_list = get_user_list(args.input_file)
    folder_name = get_output_folder()
    start_date, end_date = get_start_end_date(args)

    for user_name in user_list:
        tweet_content = query_content(user_name, start_date, end_date)
        write_to_file(os.path.join(folder_name, user_name), tweet_content)


def main():
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
    try:
        parser = ArgumentParser(
            description=__doc__
        )

        parser.add_argument("-i", "--input_file", type=str, default="twitter_user.txt",
                            help="All Twitter user read From txt  ")

        parser.add_argument("-k", "--keyword_file", type=str,
                            help="The all you want search keyword from this user")

        parser.add_argument("-s", "--start", type=str, default="20100101", help="Query start time")

        parser.add_argument("-e", "--end", type=str, help="Query end time")

        parser.add_argument("-l", "--limit", type=int, default=None,
                            help="Number of minimum tweets to gather.")

        args = parser.parse_args()

        crawl_content(args)

    except KeyboardInterrupt:
        logging.info("Program interrupted by user. Quitting...")

