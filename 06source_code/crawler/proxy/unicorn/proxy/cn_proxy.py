#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
from bs4 import BeautifulSoup
from urlparse import urljoin

from util.select_useragent import selectUserAgent
from util.url_request import reqByHttpProxy
from util.proxy_item import ProxyItem
from util.data_storage import DataSaveToMongo

#目标网页对端口号进行了混淆,需要自行解析
def get_matchup_port(htmlcontent):
    get_content = htmlcontent.find('script').get_text()
    content_dict = {}
    for content in get_content.strip('\n').split(';'):
        content_list = content.split('=')
        if len(content_list) >= 2:
            content_dict[content_list[0]] = content_list[1].split('"')[1]  #去除获得的字符串中多余的双引号
    return content_dict

#将ip地址和解析得到的端口号进行组装
def get_ip(ip_and_port,port_content):
        ip = ip_and_port[0]
        port_list = ip_and_port[1].strip(')').split('+')
        
        port = ""
        for port_data in port_list:
            if len(port_data) == 0:
                continue
            port = port + port_content[port_data]
        
        return ip + ":" + port 

#解析网页
def request_url(url_address):
    url_content = reqByHttpProxy(url_address)
    soup = BeautifulSoup(url_content)
    port_matchup = get_matchup_port(soup) # 获取网页中制定的端口数字对应关系,将得到的字符串转换为字典
        
    rows = soup.find_all('tr')
    i = 1

    for row in rows:
        i = i + 1
        if i <= 3:
            continue
        data = row.find_all('td')
        ip_content = data[0].get_text().split('document.write(":"')
        ip_and_port = get_ip(ip_content,port_matchup)
        
        proxy_type = data[1].get_text()
        proxy_locate = data[2].get_text()

        print 'url: ' + ip_and_port 
        print 'type: ' + data[1].get_text()
        print 'locate: ' + data[2].get_text()
        print data[3].get_text()

        proxy = ProxyItem(ip_and_port, data[2].get_text(), data[1].get_text())
        #data_save.saveToDb(proxy)
        


#从初始网页获取所有的连接,并依次访问
def get_next_page(url_address):
    page_content = reqByHttpProxy(url_address)
    soup = BeautifulSoup(page_content)

    next_page = soup.select('div#plist')
    for i in next_page[0].find_all('a'):
        next_url = urljoin(url_address,i['href'])
        request_url(next_url)

def main():
    start_url = 'http://www.cnproxy.com'
    get_next_page(start_url)

if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()

    print 'Cost time %d'%(end_time-start_time)
