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

# 先清理一次
# spy_clean_process()

#打开数据库
db = spy_open_database()
cursor = db.cursor()

driver = webdriver.Chrome()
driver.implicitly_wait(5)


def get_cards(base_url,cat,pages):
    for page in range(1,pages+1):
        u=base_url
        if page>1:
            u=base_url+"/pn"+str(page)
        driver.get(u)
        cards=driver.find_elements_by_class_name("gdd-material-card")
        for card in cards:
            try:
                a_tag=card.find_element_by_class_name("gdd-material-card__title")
                title=a_tag.text
                href=a_tag.get_attribute("href")
                print(cat,page,pages,href,title)
                # 写数据库
                sql = (
                    "INSERT INTO gaoding (id,cat,url,title,created) "
                    "VALUES ('%s','%s','%s','%s','%s') "
                    "ON DUPLICATE KEY UPDATE "
                    "id=VALUES(id), "
                    "cat=VALUES(cat), "
                    "url=VALUES(url), "
                    "title=VALUES(title), "
                    "created=created " % (href,cat,href,title,datetime.date.today())
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

            


# 采集 第一种分类
urls=[
    "https://www.gaoding.com/s/newmedia/search",
    "https://www.gaoding.com/s/ecommerce/search",
    "https://www.gaoding.com/s/education/search",
    "https://www.gaoding.com/s/h5/search",
    "https://www.gaoding.com/s/video/search",
    "https://www.gaoding.com/s/ppt/search",
    "https://www.gaoding.com/s/perform/search",
    "https://www.gaoding.com/s/business/search",
    "https://www.gaoding.com/s/data/search",
    "https://www.gaoding.com/s/print/search",
    "https://www.gaoding.com/s/financial/search",
    "https://www.gaoding.com/s/cateringservice/search",
]

for url in urls:
    driver.get(url)
    elems=driver.find_elements_by_class_name("g-pagination__number")
    max_page=1
    for e in elems:
        if e.text.isnumeric():
            num=int(e.text)
            if num>max_page:
                max_page=num
    cat=driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[1]/div/div[1]/div/span[2]/a').text
    print("分类:"+cat+" 页数:"+str(num))
    get_cards(url,cat,max_page)
    


# 清理chrome进程
driver.close()
driver.quit()

# 关闭数据库
db.close()


