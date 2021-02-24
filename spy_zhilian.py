# -*- coding: utf-8 -*-

import os
from selenium import webdriver
import pymysql
import datetime
from time import sleep
from selenium.webdriver.chrome.options import Options
import pickle
import re


def spy_open_database():
    return pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='spider', charset='utf8')


def spy_clean_process():
    os.system("chcp 65001 && taskkill /F /IM chromedriver.exe")


def get_cards(driver):
    """
    1.找到父类div
    2.循环获取信息并存入
    3.获取完毕后下滑滚动条到底部
    4.继续读取信息并存入
    5.结束
    """
    # cats = 2
    # xpath = '//*[@id="root"]/div[3]/div[1]/div[1]/div[8]/div[1]/div[' + str(cats) + ']'
    # cnt = driver.find_element_by_xpath(xpath)
    # save_data(cnt, cats)
    # return

    # scroll_to_bottom(driver)
    # # sleep(10)
    # # scroll_to_bottom(driver)
    # return

    cats = 1
    debug_dist = {}
    while True:
        try:
            if debug_dist.get(cats, 0) >= 2:
                break
            xpath = '//*[@id="root"]/div[3]/div[1]/div[1]/div[8]/div[1]/div[' + str(cats) + ']'
            cnt = driver.find_element_by_xpath(xpath)
            if cnt:
                save_data(cnt, cats)
                cats += 1
        except:
            scroll_to_bottom(driver)
            if debug_dist.get(cats):
                debug_dist[cats] += 1
            else:
                debug_dist[cats] = 1
            sleep(10)
            continue


def save_data(element, cats):
    """
    获取数据并插入
    """
    # 拼接参数
    if cats == 1:
        # xpath = "div/div[2]/div[1]" #稿定
        xpath = "div[1]/div/div[1]"  #创客贴
    else:
        xpath = "div/div/div[1]"
    contents = element.find_element_by_xpath(xpath)

    lf_cnt = contents.find_element_by_xpath('div[1]/div[2]/div')
    name = lf_cnt.find_element_by_xpath('div[1]/div/div').text
    company = keyword
    gender = lf_cnt.find_element_by_xpath('div[2]/span[1]').text
    age = lf_cnt.find_element_by_xpath('div[2]/span[2]').text
    # 有人没填工作时间
    experience = lf_cnt.find_element_by_xpath('div[2]/span[3]').text
    try:
        education = lf_cnt.find_element_by_xpath('div[2]/span[4]').text
        status = ["考虑机会", "正在找工作", "暂不换工作"]
        if education in status:
            education = lf_cnt.find_element_by_xpath('div[2]/span[3]').text
            experience= ""
    except:
        experience = ""
        education = lf_cnt.find_element_by_xpath('div[2]/span[3]').text


    work_place = lf_cnt.find_element_by_xpath('div[3]/span[1]').text

    #有人没填期望职位
    try:
        salary = lf_cnt.find_element_by_xpath('div[3]/span[3]').text
    except:
        salary = lf_cnt.find_element_by_xpath('div[3]/span[2]').text

    rg_cnt = contents.find_elements_by_xpath("div[2]/div/div/div[1]/div[3]/div")

    # 匹配到就插入，如果一条没有匹配到就只插入一条
    i = 0
    for cnt in rg_cnt:
        k = cnt.find_element_by_xpath('div[2]/div[1]').get_attribute("title")
        if re.search(keyword, k):
            work = cnt.find_element_by_xpath('div[2]/div[2]').get_attribute("title")
            competitor_experience = cnt.find_element_by_xpath('div[1]').text
            insert_data(name, company, work, gender, age, education, work_place, experience, competitor_experience,
                        salary)
            i += 1
            print(name, company, work, gender, age, education, work_place, experience, competitor_experience, salary)
    if i == 0:
        insert_data(name, company, "", gender, age, education, work_place, experience, "", salary)
        print(name, company, gender, age, education, work_place, experience, salary)



def insert_data(name, company, work, gender, age, education, work_place, experience, competitor_experience, salary):
    try:
        sql = (
                "INSERT INTO recruitment (name,company,work,gender,age,education,work_place,experience,competitor_experience,salary,origin) "
                "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') "
                "ON DUPLICATE KEY UPDATE "
                "name=VALUES(name), "
                "company=VALUES(company), "
                "work=VALUES(work), "
                "gender=VALUES(gender), "
                "age=VALUES(age), "
                "education=VALUES(education), "
                "work_place=VALUES(work_place), "
                "experience=VALUES(experience), "
                "competitor_experience=VALUES(competitor_experience), "
                "salary=VALUES(salary), "
                "origin=origin " % (
                    name, company, work, gender, age, education, work_place, experience, competitor_experience, salary,
                    origin)
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
        print("未定位到元素")


#  滚动条下滑到底部
def scroll_to_bottom(driver):
    for y in range(30):
        js = 'window.scrollBy(0,600)'
        driver.execute_script(js)
        sleep(0.5)

    # driver.execute_script("""
    #     (function () {
    #         var y = document.body.scrollTop;
    #         var step = 100;
    #         window.scroll(0, y);
    #
    #         function f() {
    #             if (y < document.body.scrollHeight) {
    #                 y += step;
    #                 window.scroll(0, y);
    #                 setTimeout(f, 50);
    #             }
    #             else {
    #                 window.scroll(0, y);
    #                 document.title += "scroll-done";
    #             }
    #         }
    #
    #         setTimeout(f, 1000);
    #     })();
    #     """)


# 采集 第一种分类
urls = [
    "https://rd6.zhaopin.com/talent/search?jobNumber=CC454400980J40101285516"
]

# keyword = "稿定"
keyword = "创客贴"
origin = "智联"

'''
表结构
CREATE TABLE `recruitment` (
  `name` varchar(255) DEFAULT NULL,
  `company` varchar(255) DEFAULT NULL,
  `work` varchar(255) DEFAULT NULL,
  `gender` varchar(255) DEFAULT NULL,
  `age` varchar(255) DEFAULT NULL,
  `education` varchar(255) DEFAULT NULL,
  `work_place` varchar(255) DEFAULT NULL,
  `experience` varchar(255) DEFAULT NULL,
  `competitor_experience` varchar(255) DEFAULT NULL,
  `salary` varchar(255) DEFAULT NULL,
  `origin` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''

if __name__ == '__main__':
    # 先清理一次
    # spy_clean_process()

    # 打开数据库
    db = spy_open_database()
    cursor = db.cursor()

    # cmd开启chrome窗口，直接用webdriver控制打开过的窗口(模拟手动打开，绕过智联反爬虫js检测)
    # chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\Users\HCKJ\chromeconfig"

    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    # sleep(50)  # 手动登陆

    # pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
    # driver.get(url)  # 加载网页
    # cookies = pickle.load(open("cookies.pkl", "rb"))
    # print(cookies)
    # for cookie in cookies:
    #     self.driver.add_cookie(cookie)  # 加载Cookies

    # 爬取
    get_cards(driver)

    # 清理chrome进程
    driver.close()
    driver.quit()

    # 关闭数据库
    db.close()
