#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
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
    s = requests.Session()
    for cookie in get_cookies():
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
    options = webdriver.ChromeOptions()

    # options.add_argument('--proxy-server=%s' % 'http://192.168.1.3:8119')
    # options.add_argument('--user-data-dir=C:/Users/Administrator/AppData/Local/Google/Chrome/User Data/Default')
    options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    # options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("window-size=1920*1080")
    browser = webdriver.Chrome(chrome_options=options, executable_path='tools/chromedriver.exe')
    browser.get(LOGIN_URL)

    username = browser.find_element_by_name('username_email')
    password = browser.find_element_by_name('password')

    username.send_keys("demohaha")
    password.send_keys("demohaha")

    browser.find_element_by_xpath("//input[@type='submit' and @value='登录']").click()

    s = requests.Session()
    for cookie in browser.get_cookies():
        s.cookies.set(cookie['name'], cookie['value'])

    contents = s.post(LOAD_DATA_URL, headers=get_headers(), data=param, proxies=get_proxy_dict())
    contents_json = contents.json()

    return contents_json
