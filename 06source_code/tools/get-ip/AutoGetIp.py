#!/usr/bin/env python

import requests 
import logging
import smtplib
import sys
import json 

from email.mime.text import MIMEText
 

def get_current_ip():
    try:
        response = requests.get('https://api.ipify.org/?format=json')
        if response.status_code != 200:
            return None 
        
        latest_ip = json.loads(response.text)['ip']
        return latest_ip
    except Exception as e:
        print e 
    return None 


def send_email(new_ip):
    sender = 'xxxx@163.com'
    receivers = ['xxxxx@126.com', 'xxxxxx@qq.com']

    msg = MIMEText('Welcome Get NetWork, You Are The Best One!', 'plain', 'utf-8')
    msg['Subject'] = 'New Ip Is %s' % new_ip
    msg['From'] = '{}'.format(sender)
    msg['To'] = ','.join(receivers)

    try:
        smtpObj = smtplib.SMTP_SSL('smtp.163.com', 465)
        smtpObj.login('xxxxx@163.com', 'xxxxxxxx')
        smtpObj.sendmail(sender, receivers, msg.as_string())
        smtpObj.quit()
    except smtplib.SMTPException as e:
        print e

   
def main():
   
   current_ip = get_current_ip()
   with open('/opt/get-ip/ipinfo', 'r+') as f_input:
        last_ip = f_input.readline().strip()
        if last_ip == current_ip or current_ip == None:
            print 'The Ip Is Not Change, Not Send Email'
        else:
            print 'Ip Has Change old Id is %s New IP is %s, Will Send Email!'%(last_ip, current_ip)
            f_input.seek(0)
            f_input.writelines(current_ip)
            f_input.truncate()
            send_email(current_ip)
   
   
if __name__ == '__main__':
    try:
        reload(sys)
        sys.setdefaultencoding('utf-8')
        main()
    except Exception as e:
        print e
