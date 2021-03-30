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
    headers = {"User-Agent": UserAgent, 'content-type': "application/x-www-form-urlencoded; charset=UTF-8"}
    return headers


def get_cards():
    base_url = "https://api.chuangkit.com/designtemplate/getAllTemplates.do?_dataType=json"
    num = 0
    for url in urls:
        driver.get(url)
        sleep(3)
        k1 = cats[num]

        # 分类
        class_arr = driver.find_elements_by_xpath(
            '//*[@id="__layout"]/div/main/div[2]/div[2]/div/div/div[1]/div[1]/div/div/a')  # 分类顶部
        for cls in range(len(class_arr)):
            strs = '//*[@id="__layout"]/div/main/div[2]/div[2]/div/div/div[1]/div[1]/div/div/a[' + str(
                cls + 1) + ']'
            cls_a = driver.find_element_by_xpath(strs)
            k2 = cls_a.text
            if cls == 0:
                continue
            cls_a.click()
            sleep(3)
            save_data(base_url, k1, k2)
        num += 1


def save_data(base_url, k1, k2):
    """
    拼接参数并插入
    """
    jsons = {
        "pageNo": 1,
        "pageSize": "",
        "isShowMyCollectedTemplates": "",
        "parentKindId": 20,
        "secondKindId": 166,
        "tagId": "",
        "themeId": "",
        "isOfficial": "",
        "keywords": "",
        "timeOrder": 0,
        "useTimesOrder": 0,
        "collectionTimesOrder": 0,
        "stickOrder": 1,
        "priceType": "",
        "usage": "",
        "time": "",
        "copyright": 0,
        "id": "",
        "accurate_search": 1,
        "effect_search": 1,
        "_dataClientType": 0,
        "client_type": 0,
    }

    url_data = driver.current_url.replace('https://www.chuangkit.com/', '').replace('.html', '').split('-')
    parentKindId = int(url_data[1].replace('pi', ''))
    secondKindId = int(url_data[2].replace('si', ''))
    jsons['parentKindId'] = parentKindId
    jsons['secondKindId'] = secondKindId
    head = get_headers()
    r_json = requests.post(base_url, data=jsons, headers=head, timeout=20)
    count = r_json.json()['body']['totalCount']
    if k2 == None:
        k2 = "\'\'"
    else:
        k2 = "'" + k2 + "'"

    time = datetime.date.today()
    sql = 'select count from ips_spider_py where k1 = \'' + k1 + '\' and k2 = ' + k2 + ' and type = 3 order by id desc limit 1'
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
                    "VALUES (3 ,'%s',%s,'%s','%s','%s') "
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


cats = ['营销海报', '新媒体配', '印刷物料', '办公文档', '个性定制', '社交生活', '电商设计', '原创插画']

# 采集 第一种分类
urls = [
    "https://www.chuangkit.com/templatecenter/sjhaibao.html",
    "https://www.chuangkit.com/templatecenter/wxtu.html",
    "https://www.chuangkit.com/templatecenter/yinshua.html",
    "https://www.chuangkit.com/templatecenter/work.html",
    "https://www.chuangkit.com/templatecenter/dingzhi.html",
    "https://www.chuangkit.com/templatecenter/life.html",
    "https://www.chuangkit.com/templatecenter/dstb.html",
    "https://www.chuangkit.com/templatecenter/chahua.html",
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
    schedule.every().sunday.at("22:00").do(run_threaded, get_cards)

    while True:
        schedule.run_pending()

    # 清理chrome进程
    driver.close()
    driver.quit()

    # 关闭数据库
    db.close()
