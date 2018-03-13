#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import guo_media_util
from bs4 import BeautifulSoup


def crawl_status():
    #request_with_cookie = guo_media_util.get_requests_with_cookie()
    param = dict()
    param['get'] = 'posts_profile'
    param['filter'] = 'all'

    offset = 0
    with open('follwers_list.txt', 'r') as f_input:
        with open('status_list.txt', 'w')as f_output:
            for line in f_input:
                line_arr = line.strip().split("\t")
                if len(line_arr) < 2:
                    continue

                param['id'] = line_arr[2]
                while True:
                    param['offset'] = offset
                    contents = guo_media_util.request_data(param)
                    if 'append' not in contents or contents['append'] is not \
                            True or 'data' not in contents:
                        break

                    data_content_html = contents['data']

                    soup = BeautifulSoup(data_content_html, 'lxml')
                    post_list = soup.find_all('div', class_='post')
                    offset = offset + 1
                    for post in post_list:
                        status_info_list = list()
                        data_id = post.attrs['data-id']
                        post_time = post.find('div', class_='post-time').find('a')['data-time']
                        data_text = post.find('div', class_='post-text-plain hidden').get_text()

                        comments_count = post.find('span', id='span-comments-counter_' + data_id).get_text()
                        share_count = post.find('span', id='span-share-counter_' + data_id).get_text()
                        like_count = post.find('span', class_='span-counter_' + data_id).get_text()

                        status_info_list.append(data_id)
                        status_info_list.append(post_time)
                        status_info_list.append(comments_count)
                        status_info_list.append(share_count)
                        status_info_list.append(like_count)
                        status_info_list.append(data_text)

                        print "\t".join(status_info_list)
                        f_output.write("\t".join(status_info_list) + "\n")




if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    crawl_status()
