#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import time
from collections import defaultdict


def stat_community_price(community_dict):
    avg_price_list = list()
    for community in community_dict.keys():
        i = 0
        unit_price = 0
        for line in community_dict[community]:
            i = i + 1
            unit_price = unit_price + int(line.split("|")[4])

        avg_price = unit_price / i
        avg_price_list.append(community + "\t" + str(avg_price))
    return avg_price_list


def get_community_dict(house_info_file):
    record_num = 0
    community_dict = defaultdict(list)
    with open(house_info_file, 'r') as f_input:
        for line in f_input:
            record_num = record_num + 1
            info_arr = line.strip().split("|")
            community = info_arr[1]
            community_dict[community].append(line)

    return record_num, community_dict


def get_format_current_time():
    return time.strftime("%Y-%m-%d", time.localtime())


def write_to_stat(analysis_type, line_list):
    with open("stat_" + get_format_current_time(), 'a+') as f_input:
        f_input.write(analysis_type + "\n")
        for line in line_list:
            f_input.write(get_format_current_time() + "\t" + line + "\n")


def get_all_house_list(house_info_file):
    house_id_list = list()
    with open(house_info_file, 'r') as f_input:
        for line in f_input:
            house_id = line.split("|")[0]
            house_id_list.append(house_id)
    return house_id_list


def find_add_house(new_house_info_file, old_house_info_file):
    """
      找出所有新增的房源
    :return:
    """
    new_add_house_list = list()
    old_house_list = get_all_house_list(old_house_info_file)
    with open(new_house_info_file, 'r') as f_input:
        for line in f_input:
            house_id = line.split("|")[0]
            if house_id not in old_house_list:
                new_add_house_list.append(line)
    return new_add_house_list


def find_sub_house(new_house_info_file, old_house_info_file):
    """
    找出所有减少的房源
    :return:
    """
    sub_house_list = list()
    new_house_list = get_all_house_list(new_house_info_file)
    with open(old_house_info_file, 'r') as f_input:
        for line in f_input:
            house_id = line.split("|")[0]
            if house_id not in new_house_list:
                sub_house_list.append(line)
    return sub_house_list


def analysis_house(options):
    new_house_info_file = options.new
    old_house_info_file = options.old

    record_num, new_community_dict = get_community_dict(new_house_info_file)
    write_to_stat('-------二手房记录--------', str(record_num).split())
    write_to_stat('-------关注小区数--------', str(len(new_community_dict.keys())).split())
    avg_price_list = stat_community_price(new_community_dict)
    write_to_stat('-------实时均价----------', avg_price_list)
    new_add_house = find_add_house(new_house_info_file, old_house_info_file)
    write_to_stat('-------新增房源----------', new_add_house)
    sub_house = find_sub_house(new_house_info_file, old_house_info_file)
    write_to_stat('-------减少房源----------', sub_house)


def main(args):
    parser = argparse.ArgumentParser(description=
                                   "crawl community house info",
                                   usage='--input <community house info>')

    parser.add_argument("--n", "--new", dest="new", type=str,
                      default="new output house info", help="community list")

    parser.add_argument("--o", "--old", dest="old", type=str,
                      help="old output house info")

    options = parser.parse_args()
    analysis_house(options)


if __name__ == '__main__':
  reload(sys)
  sys.setdefaultencoding("utf-8")  # @UndefinedVariable
  main(sys.argv[1:])
