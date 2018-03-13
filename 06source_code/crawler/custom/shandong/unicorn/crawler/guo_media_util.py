#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import time

LOAD_DATA_URL = "https://www.guo.media/includes/ajax/data/load.php"
LOGIN_URL = "https://www.guo.media"


def get_cookies():
    options = webdriver.ChromeOptions()

    # options.add_argument('--proxy-server=%s' % 'http://192.168.1.3:8119')
    # options.add_argument('--user-data-dir=C:/Users/Administrator/AppData/Local/Google/Chrome/User Data/Default')
    options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    # options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("window-size=1920*1080")
    browser = webdriver.Chrome(chrome_options=options, executable_path='tools/chromedriver.exe')
    login(browser)

    browser.get("https://www.guo.media/milesguo")
    time.sleep(7)

    cookies = browser.get_cookies()
    return cookies


def login(browser):
    browser.get(LOGIN_URL)

    username = browser.find_element_by_name('username_email')
    password = browser.find_element_by_name('password')

    username.send_keys("demohaha")
    password.send_keys("demohaha")

    browser.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div/div[2]/form/div[1]/div[1]/input[3]").click()


def get_headers():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'x-requested-with': 'XMLHttpRequest',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9'}

    return headers


def get_requests_with_cookie():
    cookies = [
        {u'domain': u'www.guo.media', u'name': u'PHPSESSID', u'value': u'5cvubd4m9ahnaher1n3c20vp1k', u'path': u'/',
         u'httpOnly': False, u'secure': False},
        {u'domain': u'.guo.media', u'secure': True, u'value': u'd7ba8e2d436dfc133accbdfc4682458341520922149',
         u'expiry': 1552458149.639698, u'path': u'/', u'httpOnly': True, u'name': u'__cfduid'},
        {u'domain': u'.guo.media', u'name': u'__cfruid',
         u'value': u'fe7aa52fbfced8f4ff6aa87e4b1dad59188d49ee-1520922149', u'path': u'/', u'httpOnly': True,
         u'secure': False}, {u'domain': u'.guo.media', u'secure': False, u'value': u'66867e17c783d30ffcae9f582a9ac755',
                             u'expiry': 1521008599.678981, u'path': u'/', u'httpOnly': False, u'name': u'srv_id'},
        {u'domain': u'.guo.media', u'secure': False, u'value': u'GA1.2.773077139.1520922165', u'expiry': 1521008596,
         u'path': u'/', u'httpOnly': False, u'name': u'_gid'},
        {u'domain': u'.guo.media', u'secure': False, u'value': u'GA1.2.1320845651.1520922165', u'expiry': 1583994196,
         u'path': u'/', u'httpOnly': False, u'name': u'_ga'},
        {u'domain': u'.guo.media', u'secure': False, u'value': u'1', u'expiry': 1520922225, u'path': u'/',
         u'httpOnly': False, u'name': u'_gat_gtag_UA_111414205_1'},
        {u'domain': u'.guo.media', u'secure': False, u'value': u'c5225f1853dd92a8968978d650d110c4',
         u'expiry': 1523514172.655182, u'path': u'/', u'httpOnly': False, u'name': u'xs'},
        {u'domain': u'.guo.media', u'secure': False, u'value': u'49404', u'expiry': 1523514172.655132, u'path': u'/',
         u'httpOnly': False, u'name': u'c_user'},
        {u'domain': u'www.guo.media', u'secure': False, u'value': u'83690d5b0979ac2cd030ce86579180b0',
         u'expiry': 253402300799L, u'path': u'/', u'httpOnly': False, u'name': u'user_id'}]

    s = requests.Session()
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])
    return s


def get_proxy_dict():
    http_proxy = 'socks5h://127.0.0.1:1080'
    https_proxy = 'socks5h://127.0.0.1:1080'

    proxy_dict = {
        "http": http_proxy,
        "https": https_proxy
    }
    return proxy_dict


def request_data(param):
    # options = webdriver.ChromeOptions()
    #
    # # options.add_argument('--proxy-server=%s' % 'http://192.168.1.3:8119')
    # # options.add_argument('--user-data-dir=C:/Users/Administrator/AppData/Local/Google/Chrome/User Data/Default')
    # options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    # # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    # options.add_argument("window-size=1920*1080")
    # browser = webdriver.Chrome(chrome_options=options, executable_path='tools/chromedriver.exe')
    # browser.get(LOGIN_URL)
    #
    # username = browser.find_element_by_name('username_email')
    # password = browser.find_element_by_name('password')
    #
    # username.send_keys("demohaha")
    # password.send_keys("demohaha")
    #
    # browser.find_element_by_xpath("//input[@type='submit' and @value='登录']").click()
    #
    # cookies = browser.get_cookies()

    contents = get_requests_with_cookie().post(LOAD_DATA_URL, headers=get_headers(), data=param, proxies=get_proxy_dict())
    contents_json = contents.json()

    return contents_json
