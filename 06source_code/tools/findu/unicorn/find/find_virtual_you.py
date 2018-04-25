#!/usr/bin/env python
# encoding: utf-8

import sys
import glob
import json
import chardet
import requests
import urlparse
import argparse
import multiprocessing


def check(plugin, passport, passport_type):
    """
    plugin: *.json
    passport: username, email, phone
    passport_type: passport type
    """
    if plugin["request"]["{0}_url".format(passport_type)]:
        url = plugin["request"]["{0}_url".format(passport_type)]
    else:
        return
    app_name = plugin['information']['name']
    category = plugin["information"]["category"]
    website = plugin["information"]["website"].encode("utf-8")
    judge_yes_keyword = plugin['status']['judge_yes_keyword'].encode("utf-8")
    judge_no_keyword = plugin['status']['judge_no_keyword'].encode("utf-8")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
        'Host': urlparse.urlparse(url).netloc,
        'Referer': url,
    }
    if plugin['request']['method'] == "GET":
        try:
            url = url.replace('{}', passport)
            content = requests.get(url, headers=headers, timeout=8).content
            encoding = chardet.detect(content)["encoding"]
            if encoding == None or encoding == "ascii":
                content = content.encode("utf-8")
            else:
                content = content.decode(encoding).encode("utf-8")
        except Exception, e:
            print '\n[-] %s Error: %s\n' % (app_name, str(e))
            return
        if judge_yes_keyword in content and judge_no_keyword not in content:
            print u"[{0}] {1}".format(category, ('%s (%s)' % (app_name, website)))
            icon = plugin['information']['icon'].encode("utf-8")
            desc = plugin['information']['desc'].encode("utf-8")

        else:
            pass
    elif plugin['request']['method'] == "POST":
        post_data = plugin['request']['post_fields']
        if post_data.values().count("") != 1:
            print "[*] The POST field can only leave a null value."
            return
        for k, v in post_data.iteritems():
            if v == "":
                post_data[k] = passport
        try:
            content = requests.post(url, data=post_data, headers=headers, timeout=8).content
            encoding = chardet.detect(content)["encoding"]
            if encoding == None or encoding == "ascii":
                content = content.encode("utf-8")
            else:
                content = content.decode(encoding).encode("utf-8")
        except Exception, e:
            return
        if judge_yes_keyword in content and judge_no_keyword not in content:
            print u"[{0}] {1}".format(category, ('%s (%s)' % (app_name, website)))
            icon = plugin['information']['icon'].encode("utf-8")
            desc = plugin['information']['desc'].encode("utf-8")
        else:
            pass


def main(args):
    parser = argparse.ArgumentParser(description="Check how many Platforms the User registered.")
    parser.add_argument("-u", action="store", dest="user")
    parser.add_argument("-e", action="store", dest="email")
    parser.add_argument("-c", action="store", dest="cellphone")
    parser_argument = parser.parse_args()

    plugins = glob.glob("plugins/*.json")
    print '[*] Find U In Virtual Worlds'

    jobs = []
    for plugin in plugins:
        with open(plugin) as f:
            try:
                content = json.load(f)
            except Exception, e:
                print e, plugin
                continue
        if parser_argument.cellphone:
            p = multiprocessing.Process(target=check,
                                        args=(content, unicode(parser_argument.cellphone, "utf-8"), "cellphone"))
        elif parser_argument.user:
            p = multiprocessing.Process(target=check,
                                        args=(content, unicode(parser_argument.user, "utf-8"), "user"))
        elif parser_argument.email:
            p = multiprocessing.Process(target=check,
                                        args=(content, unicode(parser_argument.email, "utf-8"), "email"))
        p.start()
        jobs.append(p)
    while sum([i.is_alive() for i in jobs]) != 0:
        pass
    for i in jobs:
        i.join()

if __name__ == '__main__':
    main(sys.argv[1:])
