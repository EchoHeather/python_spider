# -*- coding: utf-8 -*-

import pymysql
import os
from selenium import webdriver
import pymysql
import datetime
import re
from time import sleep


def spy_open_database():
	return pymysql.connect("127.0.0.1","root","root","spider" )

def spy_clean_process():
	os.system("chcp 65001 && taskkill /F /IM chromedriver.exe")

def get_cards(base_url,cat,pages):
    for page in range(1,pages+1):
        if page > 1:
            continuation = (page - 1) * 50
            u = base_url + "?continuation=" + str(continuation)
            driver.get(u)

        scroll_to_bottom(driver)

        card_div = driver.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div/div/div[3]/div/div[2]/div/div[2]/div/div')  #class="tL7E2g"

        # div有a标签的才是可以爬取的元素
        # 遍历该元素下面所有的信息并入库
        for cards in card_div:
            content = cards.find_elements_by_xpath("div")
            for ct in content:
                try:
                    tag_a = ct.find_element_by_xpath("a")
                    title = tag_a.find_element_by_xpath("div/div[1]/div/div[1]/img").get_attribute("alt")
                    url = tag_a.find_element_by_xpath("div/div[1]/div/div[1]/img").get_attribute("src")
                    print(title, url, page, pages)
                    sql = (
                            "INSERT INTO canva (id,cat,url,title,created) "
                            "VALUES ('%s','%s','%s','%s','%s') "
                            "ON DUPLICATE KEY UPDATE "
                            "id=VALUES(id), "
                            "cat=VALUES(cat), "
                            "url=VALUES(url), "
                            "title=VALUES(title), "
                            "created=created " % (url, cat, url, title, datetime.date.today())
                    )
                    try:
                        # 执行SQL语句
                        cursor.execute(sql)
                        # 提交修改
                        db.commit()
                    except pymysql.Error as e:
                        print(e.args[0], e.args[1])
                        db.rollback()
                except:
                    print(cat,page,pages,"未定位到元素")

#  防止懒加载
def scroll_to_bottom(driver):
    for y in range(30):
        js = 'window.scrollBy(0,600)'
        driver.execute_script(js)
        sleep(0.5)


# 采集 第一种分类
urls=[
    "https://www.canva.cn/templates/search/566A5Y6GX64/",
    "https://www.canva.cn/templates/search/Logo/",
]


'''
表结构
CREATE TABLE `canva` (
  `id` varchar(500) NOT NULL,
  `cat` varchar(255) DEFAULT NULL,
  `url` varchar(500) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `created` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''

if __name__ == '__main__':
    # 先清理一次
    # spy_clean_process()

    # 打开数据库
    db = spy_open_database()
    cursor = db.cursor()

    driver = webdriver.Chrome()
    driver.maximize_window() # 懒加载(页面无法全部读取 会丢失数据)
    driver.implicitly_wait(5)

    for url in urls:
        driver.get(url)
        elems = driver.find_elements_by_class_name("xehbrg")
        max_page = 1
        for e in elems:
            if e.text.isnumeric():
                num = int(e.text)
                if num > max_page:
                    max_page = num
        cat = driver.find_element_by_xpath('//*[@class="AMSf0g"]/h1').text
        print("分类:" + cat + " 页数:" + str(num))
        get_cards(url, cat, max_page)

    # 清理chrome进程
    driver.close()
    driver.quit()

    # 关闭数据库
    db.close()