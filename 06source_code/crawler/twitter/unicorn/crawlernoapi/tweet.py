#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from bs4 import BeautifulSoup
from coala_utils.decorators import generate_ordering


@generate_ordering('user_id', 'create_time', 'status_id', 'lang', 'device', 'retweet_count', 'favorite_count', 'geo',
                   'place', 'text')
class Tweet:
    def __init__(self, user_id, create_time, status_id, lang, device, retweet_count, favorite_count, geo, place, text):
        self.user_id = user_id
        self.create_time = create_time
        self.status_id = status_id
        self.lang = lang
        self.device = device
        self.retweet_count = retweet_count
        self.favorite_count = favorite_count
        self.geo = geo
        self.place = place
        self.text = text

    def __repr__(self):
        line_list = []
        line_list.append(self.user_id)
        line_list.append(self.create_time.strftime("%Y-%m-%d %H:%M:%S"))
        line_list.append(self.status_id)
        line_list.append(self.lang)
        line_list.append(self.device)
        line_list.append(self.retweet_count)
        line_list.append(self.favorite_count)
        line_list.append(self.geo)
        line_list.append(self.place)
        line_list.append(self.text)
        return "\t".join(line_list)


    @classmethod
    def from_soup(cls, tweet):
        user_id = tweet.find('div')['data-user-id']
        create_time = datetime.utcfromtimestamp(
            int(tweet.find('span', '_timestamp')['data-time']))
        status_id = tweet['data-item-id']
        lang = tweet.find('p', 'tweet-text')['lang']
        device = ""
        retweet_count = tweet.find('div', 'ProfileTweet-action--retweet'). \
                             find('span', 'ProfileTweet-actionCountForPresentation').text or '0'
        favorite_count = tweet.find('div', 'ProfileTweet-action--favorite'). \
                             find('span', 'ProfileTweet-actionCountForPresentation').text or '0'
        geo = ""
        place = ""
        text = tweet.find('p', 'tweet-text').text or ""

        return cls(user_id, create_time, status_id, lang, device, \
                   retweet_count, favorite_count, geo, place, text.replace("\n", ""))

    @classmethod
    def from_html(cls, html):
        soup = BeautifulSoup(html, "lxml")
        tweets = soup.find_all('li', 'js-stream-item')
        if tweets:
            for tweet in tweets:
                try:
                    yield cls.from_soup(tweet)
                except AttributeError:
                    pass  # Incomplete info? Discard!


