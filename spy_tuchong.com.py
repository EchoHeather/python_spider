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


# import getheaders

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
    headers = {"User-Agent": UserAgent}
    return headers


def get_cards():
    base_url = "https://sheji.tuchong.com/api/v1/template/search?_t="
    for url in urls:
        driver.get(url)
        sleep(3)

        # 点击更多
        driver.find_element_by_xpath('//*[@id="root"]/div/main/div[1]/div[1]/div[2]/div[1]/div[16]').click()

        # 合并分类
        cnt_class = driver.find_elements_by_xpath('//*[@id="root"]/div/main/div[1]/div[1]/div[2]/div[1]/div')
        bnt_class = driver.find_elements_by_xpath('//*[@id="root"]/div/main/div[1]/div[1]/div[2]/div[2]/div')
        for bnt in bnt_class:
            cnt_class.append(bnt)

        # 采集
        for i, cnt in enumerate(cnt_class):
            k1 = cnt.find_element_by_xpath('span').text
            if k1 == "更多":
                continue

            if i > 0:           # 翻页
                cnt.click()
                sleep(3)

            # 入库
            classify = driver.find_elements_by_xpath('//*[@id="root"]/div/main/div[1]/div[2]/div[2]/div[1]/div')
            for index, v in enumerate(classify):
                # 入库
                k2 = v.find_element_by_xpath('span').text
                if index > 0:
                    v.click()
                    sleep(3)

                url_data = driver.current_url  # current_url 方法可以得到当前页面的URL
                result = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url_data).query))
                if 'categoryIds' in result:
                    result = result['categoryIds']
                else:
                    result = None

                save_data(base_url, k1, k2, result)


def save_data(base_url, k1, k2, result = None):
    """
    获取数据并插入
    """
    # 拼接参数

    all_url = get_api(base_url, result)
    print(all_url)
    head = get_headers()
    url_get = requests.get(all_url, headers=head, timeout=20)
    soup = bs4.BeautifulSoup(url_get.text, 'html5lib')
    count = json.loads(soup.text)['data']['totalCount']
    time = datetime.date.today()
    sql = 'select count from ips_tuchong where k1 = \'' + k1 + '\' and k2 = \'' + k2 + '\' order by id desc limit 1'
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
                    "INSERT INTO ips_tuchong (k1, k2, count, diff, time) "
                    "VALUES ('%s','%s','%s','%s','%s') "
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


def get_api(base_url, result):
    term = ""
    t = str(int(datetime.datetime.now().timestamp()))
    themeColor = ""
    page = "1"
    size = "100"
    total = "100"
    if result != None:
        categoryIds = result
    else:
        categoryIds = ""

    all_url = base_url + t + str(random.randint(100, 999)) + '&term=' + term + '&themeColor=' + \
              themeColor + '&page=' + page + '&size=' + size + '&total=' + total + '&categoryIds=' + categoryIds
    return all_url


# 采集 第一种分类
urls = [
    "https://sheji.tuchong.com/templates?page=1"
]

'''
表结构
CREATE TABLE `ips_tuchong` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `k1` varchar(50) NOT NULL DEFAULT '0' COMMENT '一级分类',
  `k2` varchar(50) NOT NULL DEFAULT '0' COMMENT '二级分类',
  `count` int(11) NOT NULL DEFAULT '0' COMMENT '总量',
  `diff` int(11) NOT NULL DEFAULT '0' COMMENT '相对上周差集',
  `time` date NOT NULL COMMENT '时间',
  PRIMARY KEY (`id`),
  KEY `kid` (`k1`,`k2`),
  KEY `date` (`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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
    schedule.every().sunday.at("20:00").do(run_threaded, get_cards)

    while True:
        schedule.run_pending()

    # 清理chrome进程
    driver.close()
    driver.quit()

    # 关闭数据库
    db.close()
