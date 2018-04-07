#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import requests
import json
import logging
import urllib
import sys
import re
import time
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36"}


def parse_linajia_content(soup):
    page_content_list = list()
    house_list = soup.find_all('li', class_='clear')
    for house in house_list:
        line_info = list()
        desc = house.find('div', class_='info clear').find('a').text
        house_id = house.find('div', class_='title').find('a')["data-housecode"]
        house_info = house.find('div', class_='houseInfo').text
        position_info = house.find('div', class_='positionInfo').text
        total_price = house.find('div', class_='totalPrice').text
        unit_price = house.find('div', class_='unitPrice').text

        total_price = re.findall(r"\d+\.?\d*", total_price)[0]
        unit_price = re.findall(r"\d+\.?\d*", unit_price)[0]
        area = re.findall(r"\d+\.?\d*", house_info.split("|")[2])[0]

        line_info.append(house_id)
        line_info.append(house_info.split("|")[0])
        line_info.append(house_info.split("|")[1])
        line_info.append(area)
        line_info.append(unit_price)
        line_info.append(total_price)
        line_info.append(position_info)
        line_info.append(desc)
        line_str = "|".join(line_info)
        print line_str
        page_content_list.append(line_str)
    
    return page_content_list


def crawl_lianjia(line):
    content_list = list()
    url = "https://nj.lianjia.com/ershoufang/co32rs" + urllib.quote(line) + "/"
    print "request url is " + url
    lianjia_response = requests.get(url, headers=headers)
    if lianjia_response.status_code != 200:
        logging.info("Crawl Data Have Exception, Status Code : %s" % lianjia_response.status_code)
        return content_list

    contents_html = lianjia_response.text.decode('utf-8').encode('utf-8')
    soup = BeautifulSoup(contents_html, 'lxml')
    page_content_list = parse_linajia_content(soup)
    content_list.extend(page_content_list)
    page_data = soup.find('div', class_='page-box house-lst-page-box')["page-data"]
    page_json = json.loads(page_data)
    print page_json["totalPage"]
    
    i = 2 
    while i <= page_json["totalPage"]:
        next_page_url = "https://nj.lianjia.com/ershoufang/pg" + str(i) + "co32rs" + urllib.quote(line) + "/"
        print "request url is " + next_page_url
        lianjia_response = requests.get(next_page_url, headers=headers)
        soup = BeautifulSoup(lianjia_response.text.decode('utf-8').encode('utf-8'), 'lxml')
        page_content_list = parse_linajia_content(soup)

        content_list.extend(page_content_list)
        i = i + 1

    return content_list


def get_format_current_time():
    return time.strftime("%Y-%m-%d", time.localtime())


def write_house_to_file(house_info_list):
    file_name = "house-info_" + get_format_current_time()
    with open(file_name, 'a+') as f_output:
        for house in house_info_list:
            f_output.write(house + "\n")


def crawl_community_house(options):
    """
       按小区爬取二手房源信息,爬取信息包括以下
       小区    房型    面积    朝向    楼层(年代)    位置    关注人数    带看次数    发布时间    单价    总价    描述
    """
    with open(options.input, "r") as f_input:
        for line in f_input:
            house_info_list = crawl_lianjia(line.strip())
            write_house_to_file(house_info_list)


def main(args):
    parser = argparse.ArgumentParser(description=
                                     "crawl community house info", usage='--input <community house info>')

    parser.add_argument("--i", "--input", dest="input", type=str,
                        default="community_list.txt", help="community list")

    parser.add_argument("--o", "--output", dest="output", type=str,
                    help="output dir")

    options = parser.parse_args()   
    progress_start = time.time()
    crawl_community_house(options)
    progress_end = time.time()
    logging.info("Crawl Cost Time " + str(progress_end - progress_start) + "  s")


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding("utf-8")  # @UndefinedVariable
    main(sys.argv[1:])
