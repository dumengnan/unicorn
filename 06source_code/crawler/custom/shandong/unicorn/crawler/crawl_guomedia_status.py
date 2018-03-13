#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import guo_media_util
from bs4 import BeautifulSoup


def download_media(request_with_cookie, download_url, output):
    response = request_with_cookie.get(download_url, stream=True)
    if response.status_code == 200:
        with open(output, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)


def crawl_status(input_file, output_dir):
    request_with_cookie = guo_media_util.get_requests_with_cookie()
    param = dict()
    param['get'] = 'posts_profile'
    param['filter'] = 'all'

    offset = 0
    if not os.path.exists("status"):
        os.makedirs("status")

    with open(input_file, 'r') as f_input:
        for line in f_input:
            line_arr = line.strip().split("\t")
            if len(line_arr) < 2:
                continue

            user_name = line_arr[1].strip()
            dirname = os.path.join("status", user_name)
            if not os.path.exists(dirname):
                os.mkdir(dirname)

            f_output = open(os.path.join(dirname, "status_list"), 'w')
            param['id'] = line_arr[2]
            while True:
                param['offset'] = offset
                contents = guo_media_util.request_json_data(request_with_cookie, param)
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
                    data_text = data_text.replace('\n', '')

                    comments_count = post.find('span', id='span-comments-counter_' + data_id).get_text()
                    share_count = post.find('span', id='span-share-counter_' + data_id).get_text()
                    like_count = post.find('span', class_='span-counter_' + data_id).get_text()

                    status_info_list.append(data_id)
                    status_info_list.append(post_time)
                    status_info_list.append(comments_count)
                    status_info_list.append(share_count)
                    status_info_list.append(like_count)
                    status_info_list.append(data_text)

                    video = post.find('video')
                    if video is not None:
                        video_url = video.find('source')['src']
                        print video_url
                        video_name = "video_" + video_url.split("/")[-1]
                        status_info_list.append(video_name)
                        # if not os.path.exists(os.path.join(dirname, video_name)):
                        #     download_media(request_with_cookie, video_url, os.path.join(dirname, video_name))

                    imgs = post.find_all('a', class_='js_lightbox')
                    if imgs is not None:
                        for img in imgs:
                            img_url = img['data-image']
                            print img_url
                            image_name = "image_" + img_url.split("/")[-1]
                            status_info_list.append(image_name)
                            if not os.path.exists(os.path.join(dirname, image_name)):
                                download_media(request_with_cookie, img_url, os.path.join(dirname, image_name))

                    print "\t".join(status_info_list)
                    f_output.write("\t".join(status_info_list) + "\n")

            f_output.close()


def main(args):
    input_file = args.input
    output_dir = args.output

    print input_file, output_dir
    crawl_status(input_file, output_dir)


if __name__ == '__main__':
    crawl_status('follwers_list.txt', '.')
