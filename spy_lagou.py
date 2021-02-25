# -*- coding: utf-8 -*-

import os
from selenium import webdriver
import pymysql
import datetime
from time import sleep
from selenium.webdriver.chrome.options import Options
import pickle
import re
import random


def spy_open_database():
    return pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='spider', charset='utf8')


def spy_clean_process():
    os.system("chcp 65001 && taskkill /F /IM chromedriver.exe")


def get_cards(driver):
    xpath = '//*[@id="root"]/div/div[1]/div[5]/div[2]/div[2]/div[2]/div[1]/div/div'
    cats = driver.find_elements_by_xpath(xpath)
    for cat in cats:
        # 获取失败
        try:
            top = cat.find_element_by_xpath('div[1]/div[1]/div[1]/div')
        except:
            break

        # 不填求职职位
        try:
            salary= top.find_element_by_xpath('span[3]').text
            work_place = top.find_element_by_xpath('span[2]').text
        except:
            salary = top.find_element_by_xpath('span[2]').text
            if re.search("k", salary):
                work_place = top.find_element_by_xpath('span[1]').text
            else:
                work_place = ""
                salary = ""

        cnt = cat.find_element_by_xpath('div[1]/div[2]')
        name = cnt.find_element_by_xpath('div[1]/div[1]/div[2]/div[1]').text
        company = keyword
        experience = cnt.find_element_by_xpath('div[1]/div[1]/div[2]/div[2]/span[1]').text
        education = cnt.find_element_by_xpath('div[1]/div[1]/div[2]/div[2]/span[2]').text

        # 不填性别或年龄
        try:
            age = cnt.find_element_by_xpath('div[1]/div[1]/div[2]/div[2]/span[3]').text
            try:
                gender = cnt.find_element_by_xpath('div[1]/div[1]/div[2]/div[2]/span[4]').text
            except:
                age = ""
                gender = cnt.find_element_by_xpath('div[1]/div[1]/div[2]/div[2]/span[3]').text
        except:
            age = ""
            gender = ""

        competitor_experience = ""
        work_arr = cnt.find_elements_by_xpath('div[3]/div[1]/div[2]/div[2]/div')

        # 匹配竞品公司
        check = 0
        for works in work_arr:
            k = works.find_element_by_xpath('div[1]/span[1]').text
            if re.search(keyword, k):
                work = works.find_element_by_xpath('div[1]/span[2]').text
                insert_data(name, company, work, gender, age, education, work_place, experience, competitor_experience,
                            salary)
                print("匹配到结果")
                print(name, company, work, gender, age, education, work_place, experience, competitor_experience,
                      salary)
                check += 1
            else:
                work = ""
        if check == 0:
            insert_data(name, company, work, gender, age, education, work_place, experience, competitor_experience,
                        salary)
            print("未匹配到")
            print(name, company, work, gender, age, education, work_place, experience, competitor_experience, salary)


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
    driver.execute_script("""
        (function () {
            var y = document.body.scrollTop;
            var step = 100;
            window.scroll(0, y);

            function f() {
                if (y < document.body.scrollHeight) {
                    y += step;
                    window.scroll(0, y);
                    setTimeout(f, 50);
                }
                else {
                    window.scroll(0, y);
                    document.title += "scroll-done";
                }
            }

            setTimeout(f, 1000);
        })();
        """)


# keyword = "稿定"
keyword = "创客贴"
origin = "拉钩"

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
    page = driver.find_elements_by_xpath('//*[@id="root"]/div/div[1]/div[5]/div[2]/div[2]/div[2]/div[2]/ul/li')[
        -2].get_attribute("title")

    for i in range(0, int(page) - 1):
        scroll_to_bottom(driver)
        sleep(3)
        get_cards(driver)
        driver.find_elements_by_class_name("lg-pagination-item-link")[-1].click()
        sleep(3)

    # 清理chrome进程
    driver.close()
    driver.quit()

    # 关闭数据库
    db.close()
