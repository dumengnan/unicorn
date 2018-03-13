#!/usr/bin/env python
# -*- coding: utf-8 -*-

import guo_media_util
from bs4 import BeautifulSoup


def crawl_user_info(input_file, output_file):
    with open(input_file, "a+") as f_output:
        with open(output_file, 'r') as f_input:
            for line in f_input:
                i = 0
                line_arr = line.strip().split("\t")
                url = line_arr[0]
                user_name = url.split("/")[-1]
                nick_name = ""
                if len(line_arr) == 2:
                    nick_name = line_arr[1]
                else:
                    nick_name = user_name
                response = guo_media_util.request_with_retry(url)
                if response.status_code != 200:
                    print "request failed " + url
                    continue
                soup = BeautifulSoup(response.text, 'lxml')
                profile = soup.find('div', class_='profile-tabs-wrapper')
                value_list = list()
                value_list.append(user_name)
                value_list.append(nick_name)
                if profile is None:
                    print "profile is None " + url
                    continue
                for child_li in profile.find_all('li'):
                    if i > 4:
                        break
                    i = i + 1
                    value = child_li.find('span', class_='text-underline')
                    value_list.append(value.get_text())
                print value_list
                f_output.write("\t".join(value_list) + "\n")


def main(args):
    input_file = args.input
    output_file = args.output

    print input_file, output_file
    crawl_user_info(input_file, output_file)

if __name__ == '__main__':
    crawl_user_info("follwers_info.txt", 'follwers_list.txt')

