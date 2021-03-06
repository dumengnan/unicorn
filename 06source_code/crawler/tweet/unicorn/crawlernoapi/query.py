#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from datetime import timedelta

import requests
from tweet import Tweet
from multiprocessing.pool import Pool
from functools import partial
from unicorn.utils.select_useragent import selectUserAgent
from unicorn.utils.get_random_key import get_proxy_server

INIT_URL = "https://twitter.com/search?f=tweets&q={q}"
RELOAD_URL = "https://twitter.com/i/search/timeline?f=tweets&vertical=" \
             "default&include_available_features=1&include_entities=1&" \
             "reset_error_state=false&src=typd&max_position={pos}&q={q}"


def query_single_page(url, user_agent, html_response=True, retry=3):
    """
    Returns tweets from the given URL.

    :param url: The URL to get the tweets from
    :param user_agent request head
    :param html_response: False, if the HTML is embedded in a JSON
    :param retry: Number of retries if something goes wrong.
    :return: The list of tweets, the pos argument for getting the next page.
    """
    headers = {'User-Agent': user_agent}
    json_resp = {}
    try:
        proxy_server = get_proxy_server()
        proxies = {"http": proxy_server, "https": proxy_server}
        response = requests.get(url, headers=headers, proxies=proxies)
        if response.status_code != 200:
            return [], None
        
        if html_response:
            html = response.text
        else:
            json_resp = response.json()
            html = json_resp['items_html']

        tweets = list(Tweet.from_html(html))

        if not tweets:
            return [], None

        if not html_response:
            return tweets, json_resp['min_position']

        return tweets, "TWEET-{}-{}".format(tweets[-1].status_id, tweets[0].status_id)
    except requests.exceptions.HTTPError as e:
        logging.exception('HTTPError {} while requesting "{}"'.format(
            e, url))
    except requests.exceptions.ConnectionError as e:
        logging.exception('ConnectionError {} while requesting "{}"'.format(
            e, url))
    except requests.exceptions.Timeout as e:
        logging.exception('TimeOut {} while requesting "{}"'.format(
            e, url))
    if retry > 0:
        logging.info("Retrying...")
        return query_single_page(url, user_agent, html_response, retry-1)

    logging.error("Giving up.")
    return [], None


def query_tweets_once(query, limit=None, num_tweets=0):
    """
    Queries twitter for all the tweets you want! It will load all pages it gets
    from twitter. However, twitter might out of a sudden stop serving new pages,
    in that case, use the `query_tweets` method.

    Note that this function catches the KeyboardInterrupt so it can return
    tweets on incomplete queries if the user decides to abort.

    :param query: Any advanced query you want to do! Compile it at
                  https://twitter.com/search-advanced and just copy the query!
    :param limit: Scraping will be stopped when at least ``limit`` number of
                  items are fetched.
    :param num_tweets: Number of tweets fetched outside this function.
    :return:      A list of twitterkeywordsearch.Tweet objects. You will get at least
                  ``limit`` number of items.
    """
    logging.info("Querying {}".format(query))
    query = query.replace(' ', '%20').replace("#", "%23").replace(":", "%3A")
    pos = None
    tweets = []
    user_agent = selectUserAgent()
    try:
        while True:
            new_tweets, pos = query_single_page(
                INIT_URL.format(q=query) if pos is None
                else RELOAD_URL.format(q=query, pos=pos),
                user_agent, pos is None
            )
            if len(new_tweets) == 0:
                logging.info("Got {} tweets for {}.".format(
                    len(tweets), query))
                return tweets

            tweets += new_tweets

            if limit is not None and len(tweets) + num_tweets >= limit:
                return tweets
    except KeyboardInterrupt:
        logging.info("Program interrupted by user. Returning tweets gathered "
                     "so far...")
    except BaseException:
        logging.exception("An unknown error occurred! Returning tweets "
                          "gathered so far.")

    return tweets


def eliminate_duplicates(iterable):
    """
    Yields all unique elements of an iterable sorted. Elements are considered
    non unique if the equality comparison to another element is true. (In those
    cases, the set conversion isn't sufficient as it uses identity comparison.)
    """
    class NoElement: pass

    prev_elem = NoElement
    for elem in sorted(iterable):
        if prev_elem is NoElement:
            prev_elem = elem
            yield elem
            continue

        if prev_elem != elem:
            prev_elem = elem
            yield elem


def query_tweets(query, limit=None):
    tweets = []
    iteration = 1

    while limit is None or len(tweets) < limit:
        logging.info("Running iteration no {}, query is {}".format(
            iteration, repr(query)))
        new_tweets = query_tweets_once(query, limit, len(tweets))
        tweets.extend(new_tweets)

        if not new_tweets:
            break

        mindate = min(map(lambda tweet: tweet.create_time, new_tweets)).date()
        maxdate = max(map(lambda tweet: tweet.create_time, new_tweets)).date()
        logging.info("Got tweets ranging from {} to {}".format(
            mindate.isoformat(), maxdate.isoformat()))

        # Add a day, twitter only searches until excluding that day and we dont
        # have complete results for that one yet. However, we cannot limit the
        # search to less than one day: if all results are from the same day, we
        # want to continue searching further into the past: either there are no
        # further results or twitter stopped serving them and there's nothing
        # we can do.
        if mindate != maxdate:
            mindate += timedelta(days=1)

        # Twitter will always choose the more restrictive until:
        query += ' until:' + mindate.isoformat()
        iteration += 1

    # Eliminate duplicates
    return list(eliminate_duplicates(tweets))


def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta


def query_all_tweets(query, start_date, end_date):
    """
    Queries *all* tweets in the history of twitter for the given query. This
    will run in parallel for each ~30 days.

    :param query: A twitter advanced search query.
    :param start_date: Crawl start Date eg.20170101
    :param end_date: Crawl end Date eg.20171010
    :return: A list of tweets.
    """

    queries = get_all_query(query, start_date, end_date)

    pool = Pool(10)

    all_tweets = []

    try:
        for new_tweets in pool.imap_unordered(partial(query_tweets_once), queries):
            for new_tweet in new_tweets:
                all_tweets.append(new_tweet)

    except KeyboardInterrupt:
        logging.info("Program interrupted by user. Returning all tweets "
                     "gathered so far.")

    return sorted(all_tweets, reverse=True)


def get_all_query(query, start_date, end_date):
    """
    Queries *all* tweets in the history of twitter for the given query. This
    will run in parallel for each ~30 days.

    :param query: A twitter advanced search query.
    :param start_date: Crawl start Date eg.20170101
    :param end_date: Crawl end Date eg.20171010
    :return: A list of query.
    """
    limits = []
    query_start_date = start_date
    delta_day = 10
    for next_date in perdelta(start_date, end_date, timedelta(days=delta_day)):
        if (end_date - next_date).days < delta_day:
            limits.append((next_date, end_date))
        if next_date == query_start_date:
            continue
        limits.append((query_start_date, next_date))
        query_start_date = next_date

    queries = ['{} since:{} until:{}'.format(query, since, until)
               for since, until in reversed(limits)]

    return queries
