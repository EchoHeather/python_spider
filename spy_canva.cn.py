# -*- coding: utf-8 -*-

import os
from selenium import webdriver
import pymysql
import datetime
import re
from time import sleep
from selenium.webdriver.chrome.options import Options
import random


def spy_open_database():
    return pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='spider', charset='utf8')


def spy_clean_process():
    os.system("chcp 65001 && taskkill /F /IM chromedriver.exe")


def get_cards(cat, pages):
    for page in range(1, pages + 1):
        if page > 1:
            #  点击下一页
            driver.find_elements_by_class_name('hgkkTA')[-1].click()
            sleep(5)
            scroll_to_bottom(driver)
            sleep(random.randint(6, 10))

        # div有a标签的才是可以爬取的元素
        # 遍历该元素下面所有的信息并入库 class="tL7E2g"
        tg = driver.find_element_by_class_name('tL7E2g')
        card_div = tg.find_elements_by_xpath('div')
        for cards in card_div:
            content = cards.find_elements_by_xpath("div")
            for ct in content:
                # 跳过创建空白简历
                cnt_div = ct.find_element_by_xpath('div')
                cnt_class = cnt_div.get_attribute('class')
                if cnt_class == 'mX1XqA':
                    continue
                try:
                    tag_a = cnt_div.find_element_by_xpath("div[1]/a")
                    url = tag_a.get_attribute('href')
                    title = tag_a.find_element_by_xpath("div/div/div/img").get_attribute("alt")
                    print(title, url, page, pages)
                    sql = (
                            "INSERT INTO canva (id,cat,url,title,created) "
                            "VALUES ('%s','%s','%s','%s','%s') "
                            % (url, cat, url, title, datetime.date.today())
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
                    print(cat, page, pages, "未定位到元素")


#  防止懒加载
def scroll_to_bottom(driver):
    driver.execute_script("""
        var height = document.body.scrollHeight
        var num = 1200
        window.scroll(0,height - num)
    """)


# 采集 第一种分类
urls = [
    "https://www.canva.cn/templates/search/566A5Y6GX64/",
    "https://www.canva.cn/templates/search/Logo/",
    "https://www.canva.cn/templates/search/5ZCN54mHX64/",
    "https://www.canva.cn/templates/search/5ryU56S65paH56i_X64/",
    "https://www.canva.cn/templates/search/566A5oqlX64/",
    "https://www.canva.cn/templates/search/5YWs5ZGKX64/",
    "https://www.canva.cn/templates/search/5bel5L2c6K--BX64/",
    "https://www.canva.cn/templates/search/5bel5L2c6KGoX64/",
    "https://www.canva.cn/templates/search/5b6u5L--h5YWs5LyX5Y--35bCB6Z2iX64/",
    "https://www.canva.cn/templates/search/5b6u5L--h5YWs5LyX5Y--35bCP5Zu--X64/",
    "https://www.canva.cn/templates/search/5b6u5L--h5YWs5LyX5Y--35LqM57u056CBX64/",
    "https://www.canva.cn/templates/search/5L.h5oGv5Zu.6KGoX64/",
    "https://www.canva.cn/templates/search/6KeG6aKR5bCB6Z2iX64/",
    "https://www.canva.cn/templates/search/5rS75Yqo5bCB6Z2iX64/",
    "https://www.canva.cn/templates/search/5ou85Zu--X64/",
    "https://www.canva.cn/templates/search/5o--S55S7X64/",
    "https://www.canva.cn/templates/search/5rW35oqlX64/",
    "https://www.canva.cn/templates/search/5Lyg5Y2VX64/",
    "https://www.canva.cn/templates/search/5piT5ouJ5a6dX64/",
    "https://www.canva.cn/templates/search/6YKA6K--35Ye9X64/",
    "https://www.canva.cn/templates/search/5LiJ5oqY6aG1X64/",
    "https://www.canva.cn/templates/search/5Lya5ZGY5Y2hX64/",
    "https://www.canva.cn/templates/search/6Zeo56WoX64/",
    "https://www.canva.cn/templates/search/6I--c5Y2VX64/",
    "https://www.canva.cn/templates/search/55S15ZWGYmFubmVyX64/",
    "https://www.canva.cn/templates/search/5Li75Zu--5Zu--5qCHX64/",
    "https://www.canva.cn/templates/search/5omL5py655S15ZWG6K--m5oOF6aG1X64/",
    "https://www.canva.cn/templates/search/5omL5py65rW35oqlX64/",
    "https://www.canva.cn/templates/search/5b6u5L--h5pyL5Y--L5ZyIX64/",
    "https://www.canva.cn/templates/search/55S15a2Q5ZCN54mHX64/",
    "https://www.canva.cn/templates/search/5LyY5oOg5Yi4X64/",
    "https://www.canva.cn/templates/search/5o6I5p2D5LmmX64/",
    "https://www.canva.cn/templates/search/5omL5oqE5oqlX64/",
    "https://www.canva.cn/templates/search/5aWW54q2X64/",
    "https://www.canva.cn/templates/search/5L.h57q4X64",
    "https://www.canva.cn/templates/search/6K..56iL6KGoX64/",
    "https://www.canva.cn/templates/search/6K6h5YiS6KGoX64/",
    "https://www.canva.cn/templates/search/5bqn5qyh6KGoX64/",
    "https://www.canva.cn/templates/search/5Lmm57GN5bCB6Z2iX64/",
    "https://www.canva.cn/templates/search/5Lmm562--X64/",
    "https://www.canva.cn/templates/search/5omL5py65ou85Zu--X64/",
    "https://www.canva.cn/templates/search/6KeG6aKR55u45qGGX64/",
    "https://www.canva.cn/templates/search/6LS65Y2hX64/",
    "https://www.canva.cn/templates/search/5pel562--X64/",
    "https://www.canva.cn/templates/search/5b6u5L--h5aS05YOPX64/",
    "https://www.canva.cn/templates/search/55S16ISR5qGM6Z2iX64/",
    "https://www.canva.cn/templates/search/5omL5py65aOB57q4X64/",
    "https://www.canva.cn/templates/search/6aOf6LCxX64/",
    "https://www.canva.cn/templates/search/54Ot6ZeoX64/",
    "https://www.canva.cn/templates/search/5LuK5pel5o6o6I2QX64/"

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

    # driver = webdriver.Chrome()
    # driver.maximize_window() # 懒加载(页面无法全部读取 会丢失数据)
    # driver.implicitly_wait(5)

    # cmd开启chrome窗口，直接用webdriver控制打开过的窗口(模拟手动打开，绕过反爬虫js检测)
    # chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\Users\HCKJ\chromeconfig"

    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    for url in urls:
        driver.get(url)
        # 滑动到底部
        scroll_to_bottom(driver)
        sleep(3)

        # 不同页面自行修改xpath(不同分类有不同的xpath)
        max_click = driver.find_elements_by_class_name('_5Slmcw')[-1].text
        try:
            cat = driver.find_element_by_xpath('//*[@id="__a11yId5"]/div/div/div[2]/h1/span').text # 每个分类页都不同
        except:
            cat = driver.find_element_by_xpath('//*[@id="__a11yId5"]/div/div/div[1]/div/div[1]/div[2]/h1').text
        print("分类:" + cat)
        get_cards(cat, int(max_click))
    # 清理chrome进程
    driver.close()
    driver.quit()

    # 关闭数据库
    db.close()