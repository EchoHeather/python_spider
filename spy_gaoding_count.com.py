# -*- coding: utf-8 -*-

import os
from selenium import webdriver
import pymysql
from time import sleep
import schedule
from selenium.webdriver.chrome.options import Options
import re
import urllib.parse
import datetime
import random
import json
import bs4
import requests
import json
import threading


def spy_open_database():
    return pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='spider', charset='utf8')


def get_headers():
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    UserAgent = random.choice(user_agent_list)
    headers = {"User-Agent": UserAgent, 'content-type': "application/json"}
    return headers


def get_cards():
    base_url = "https://www.gaoding.com/graphql"
    num = 0
    for url in urls:
        driver.get(url)
        sleep(3)
        type = cats[num]
        # 分类
        try:
            class_arr = driver.find_elements_by_xpath(
                '//*[@id="app"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/a')  # 分类顶部
            if len(class_arr) > 0:
                for cls in class_arr:
                    cls_text = cls.text
                    k1 = type + '/' + cls_text
                    if cls_text == '全部':
                        continue
                    else:
                        cls.click()
                        sleep(3)
                        clk()

                        # 分类下子类插入
                        try:
                            # 1. 分类下有推荐
                            class_list = []
                            lists = driver.find_elements_by_xpath(
                                '//*[@id="app"]/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/div')  # 分类下推荐
                            if len(lists) > 0:
                                for ls in lists:
                                    ls_a = ls.find_elements_by_xpath('a')
                                    for index_a, a in enumerate(ls_a):
                                        if index_a > 0:
                                            class_list.append(a)

                                # 点击子类开始查询数量
                                for ct in class_list:
                                    sleep(3)
                                    ct.click()
                                    k2 = ct.text
                                    save_data(base_url, k1, k2)
                                    print('类型: ' + k1 + ' 分类：' + k2)
                            else:
                                # 2. 有div且分类无推荐
                                print('类型: ' + k1 + ' 分类推荐：无')
                                save_data(base_url, k1)
                        except:
                            # 2. 无div且分类无推荐
                            print('类型: ' + k1 + ' 分类推荐无')
                            save_data(base_url, k1)
            else:
                print('类型: ' + type + ' 分类及子类：无')
                save_data(base_url, type)
            num += 1
        except:
            print('分类为空')


def save_data(base_url, k1, k2=None):
    """
    拼接参数并插入
    """
    jsons = {
        "operationName": "FetchSearchMaterials",
        "variables": {
            "page_num": 1,
            "page_size": 120,
            "widthChannel": False,
            "q": "",
            "design_cid": "",
            "channel_cid": "",
            "industry_cid": "",
            "tag_id": "",
            "filter_id": "",
            "type_filter_id": "",
            "channel_filter_id": "",
            "channel_children_filter_id": "",
            "sort": "",
            "styles": "",
            "colors": "",
            "ratios": ""
        },
        "query": "query FetchSearchMaterials($design_cid: ID, $filter_id: ID, $industry_cid: ID, $channel_cid: ID, $page_num: Int = 1, $page_size: Int = 50, $q: String, $tag_id: String, $sort: String, $styles: String, $ratios: String, $colors: String, $userId: Int, $widthChannel: Boolean = false) {\n materialCategory(id: $channel_cid) @include(if: $widthChannel) {\n extra {\n lineCount\n __typename\n }\n __typename\n }\n searchMaterials(design_category_id: $design_cid, filter_id: $filter_id, industry_category_id: $industry_cid, tag_ids: $tag_id, channel_category_id: $channel_cid, page_num: $page_num, page_size: $page_size, q: $q, sort: $sort, styles: $styles, ratios: $ratios, colors: $colors, user_id: $userId) {\n nodes {\n id\n title\n isVip\n userOverRole\n itemPrice\n type\n channelCategory {\n id\n extra {\n width\n height\n flags\n __typename\n }\n __typename\n }\n preview {\n url\n height\n partialVideo\n video\n width\n hex\n __typename\n }\n compositePreview {\n url\n width\n height\n hex\n __typename\n }\n channelCategory {\n id\n extra {\n flags\n __typename\n }\n __typename\n }\n ext {\n distCode\n materialLocation\n __typename\n }\n __typename\n }\n pageInfo {\n num\n size\n total\n __typename\n }\n __typename\n }\n}\n"
    }

    url_data = driver.current_url.replace('https://www.gaoding.com/templates/', '').split('-')
    url_data_len = len(url_data)
    if url_data_len == 3:
        jsons['variables']['channel_children_filter_id'] = str(url_data[2].replace('f', ''))
        jsons['variables']['channel_filter_id'] = str(url_data[1].replace('fc', ''))
        jsons['variables']['type_filter_id'] = str(url_data[0].replace('fcc', ''))
        jsons['variables']['filter_id'] = jsons['variables']['type_filter_id'] + ',' + jsons['variables'][
            'channel_filter_id'] + ',' + jsons['variables']['channel_children_filter_id']
    elif url_data_len == 2:
        jsons['variables']['type_filter_id'] = str(url_data[1].replace('f', ''))
        jsons['variables']['channel_filter_id'] = str(url_data[0].replace('fc', ''))
        jsons['variables']['filter_id'] = jsons['variables']['type_filter_id'] + ',' + jsons['variables'][
            'channel_filter_id']
    elif url_data_len == 1:
        jsons['variables']['filter_id'] = jsons['variables']['type_filter_id'] = str(url_data[0].replace('f', ''))
    else:
        return False
    head = get_headers()
    r_json = requests.post(base_url, data=json.dumps(jsons), headers=head, timeout=20)
    count = r_json.json()['data']['searchMaterials']['pageInfo']['total']
    if k2 == None:
        k2 = "\'\'"
    else:
        k2 = "'" + k2 + "'"

    time = datetime.date.today()
    sql = 'select count from ips_spider_py where k1 = \'' + k1 + '\' and k2 = ' + k2 + ' and type = 2 order by id desc limit 1'
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        if result != None:
            diff = int(count) - int(result[0])
        else:
            diff = 0

        try:
            print(k1, k2, count, diff, time)
            sql = (
                    "INSERT INTO ips_spider_py (type, k1, k2, count, diff, time) "
                    "VALUES (2 ,'%s',%s,'%s','%s','%s') "
                    % (k1, k2, count, diff, time)
            )
            # 执行SQL语句
            cursor.execute(sql)
            # 提交修改
            db.commit()
        except pymysql.Error as e:
            print(e.args[0], e.args[1])
            db.rollback()
    except pymysql.Error as e:
        print(e.args[0], e.args[1])


def clk():
    # 点击更多
    try:
        span_clk = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/span')
        if span_clk.text == '更多':
            span_clk.click()
    except:
        print("无需点击更多")


cats = ['图片', '手机网页(H5)', 'PPT 16:9', '视频', '电视屏', '网店装修']

# 采集 第一种分类
urls = [
    "https://www.gaoding.com/templates/f1612532",
    "https://www.gaoding.com/templates/f1612601",
    "https://www.gaoding.com/templates/f1612595",
    "https://www.gaoding.com/templates/f1612597",
    "https://www.gaoding.com/templates/f4789004",
    "https://www.gaoding.com/templates/f1612596"
]

'''
表结构
CREATE TABLE `ips_spider_py` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` tinyint(1) NOT NULL DEFAULT '1' COMMENT '1图虫2稿定3创客贴',
  `k1` varchar(50) NOT NULL DEFAULT '' COMMENT '一级分类',
  `k2` varchar(50) NOT NULL DEFAULT '' COMMENT '二级分类',
  `count` int(11) NOT NULL DEFAULT '0' COMMENT '总量',
  `diff` int(11) NOT NULL DEFAULT '0' COMMENT '相对上周差集',
  `time` date NOT NULL COMMENT '时间',
  PRIMARY KEY (`id`),
  KEY `date` (`time`),
  KEY `kid` (`k1`,`k2`,`type`) 
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;


'''


def run_threaded(obj_func):
    job_thread = threading.Thread(target=obj_func)
    job_thread.start()


driver = None

if __name__ == '__main__':
    # 打开数据库
    db = spy_open_database()
    cursor = db.cursor()

    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('window-size=1200x600')
    chrome_options.add_argument('log-level=3')
    driver = webdriver.Chrome(chrome_options=chrome_options)

    # 爬取
    print(datetime.datetime.now())
    schedule.every().sunday.at("21:00").do(run_threaded, get_cards)

    while True:
        schedule.run_pending()

    # 清理chrome进程
    driver.close()
    driver.quit()

    # 关闭数据库
    db.close()
