#!/usr/bin/env python
# encoding: utf-8

import sys
import glob
import json
import chardet
import requests
import argparse
import logging


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
    website = plugin["information"]["website"].encode("utf-8")
    judge_yes_keyword = plugin['status']['judge_yes_keyword'].encode("utf-8")
    judge_no_keyword = plugin['status']['judge_no_keyword'].encode("utf-8")
    headers = {
      'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }
    if plugin['request']['method'] == "GET":
        try:
            url = url.replace('{}', passport)
            content = requests.get(url, headers=headers, timeout=8).content
            if check_response(content, judge_yes_keyword, judge_no_keyword):
                logging.info(u"Find In [{0}] Response Content is {1}" \
                             .format(('%s (%s)' % (app_name, website)), content))
            else:
                logging.info(u"Not Find in {0}".format('%s' % website))
        except Exception:
            logging.exception('\n[-] %s Error \n' % (app_name))
            return

    elif plugin['request']['method'] == "POST":
        post_data = plugin['request']['post_fields']
        if post_data.values().count("") != 1:
            print "[*] The POST field can only leave a null value."
            return
        for k, v in post_data.iteritems():
            if v == "":
                post_data[k] = passport
        try:
            content = requests.post(url, data=post_data, headers=headers,
                                timeout=8).content
            if check_response(content, judge_yes_keyword, judge_no_keyword):
                logging.info(u"Find In [{0}] Response Content is {1}".format(
              ('%s (%s)' % (app_name, website)), content))
            else:
                logging.info(u"Not Find in {0}".format('%s' % website))
        except Exception:
            logging.exception('\n[-] %s Error \n' % (app_name))
            return


def check_response(content, judge_yes_keyword, judge_no_keyword):
  try:
    encoding = chardet.detect(content)["encoding"]
    if encoding is None or encoding == "ascii":
      content = content.encode("utf-8")
    else:
      content = content.decode(encoding).encode("utf-8")

    if judge_yes_keyword in content and judge_no_keyword not in content:
      return True
    else:
      return False

  except Exception as ex:
    logging.exception('\n[-] Check Response Exception : %s\n' % (str(ex)))

  return False


def find_registered(options):
  account_type = options.type
  account_value = options.value

  plugins = glob.glob("plugins/*.json")

  for plugin in plugins:
    with open(plugin) as f:
      try:
        content = json.load(f)
        check(content, account_value, account_type)
      except Exception, e:
        print e, plugin
        continue


def main(args):
  parser = argparse.ArgumentParser(
      description="Check how many Platforms the User registered.")
  parser.add_argument("--type", action="store", dest="type",
                      help="The Check Type Contains (cellphone, email, user(nickname))")
  parser.add_argument("--value", action="store", dest="value",
                      help="The Type Value  youe wille be Check")
  options = parser.parse_args()

  print '[*] Find U In Virtual Worlds [*]'
  print 'Check Type ' + options.type + " Check Value " + options.value

  find_registered(options)


if __name__ == '__main__':
  main(sys.argv[1:])
