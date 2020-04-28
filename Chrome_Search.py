#coding = utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pymysql
import time

#提取数据
class driver_1(object):
    def __init__(self):
        self.driver = webdriver.Chrome('D:\chromedriver_win32\chromedriver.exe')

    #访问谷歌，搜索信息
    def logload_Chrome(self,search):
        self.driver.get('https://www.google.com/')
        #定位搜索栏位置
        Search = self.driver.find_element_by_name('q')
        self.driver.implicitly_wait(30)
        Search.send_keys(search)
        Search.send_keys(Keys.ENTER)

    #提取站点信息
    def Search_site(self,site,num):
        dict_name_url = {}
        now_site = 'site:' + '\'' + site + '\''
        self.logload_Chrome(now_site)
        #提取url和name
        for a in range(0,num):
            if a > 0 and a < num:
                self.driver.implicitly_wait(30)
                self.driver.find_element_by_css_selector('[valign=top] td:nth-last-child(1)').click()
                Result_name = self.driver.find_elements_by_css_selector('#search .g .r h3')
                Result_url = self.driver.find_elements_by_css_selector('#search .g .r>a[href]')
                i = 0
                while i < len(Result_name):
                    dict_name_url[str(Result_name[i].text)] = str(Result_url[i].get_attribute('href'))
                    i += 1
            else:
                for handle in self.driver.window_handles:
                    self.driver.switch_to.window(handle)
                    if str(site) in self.driver.title:
                        self.driver.implicitly_wait(30)
                        Result_name = self.driver.find_elements_by_css_selector('#search .g .r h3')
                        Result_url = self.driver.find_elements_by_css_selector('#search .g .r>a[href]')
                        i = 0
                        while i < len(Result_name):
                            dict_name_url[str(Result_name[i].text)] = str(Result_url[i].get_attribute('href'))
                            i += 1
        return dict_name_url

#保存数据信息
class Save_to_DB(object):
    #链接出入数据
    def connect(self,i,key,value):
        conn = pymysql.connect(
            host = 'localhost',
            user = 'root',
            password = 'Password@2020',
            database = 'suda'
        )
        #创建游标对象
        cursor = conn.cursor()
        try:
            cursor.execute("insert into information_site_suda values(%s,'%s','%s');" %(int(i),key,value))
            conn.commit()
            conn.close()
        except:
            conn.ping()
            cursor = conn.cursor()
            cursor.execute("insert into information_site values(%s,'%s','%s');" % (int(i), key, value))
            conn.commit()
            conn.close()


if __name__ == "__main__":
    site = '*suda.edu.cn'
    num = int(50)
    i = 1
    a = driver_1()
    b = Save_to_DB()
    dict = a.Search_site(site,num)
    print('数据提取完成')
    print('收集数据总共%s条信息' %(len(dict)))
    for key,value in dict.items():
        if i <= len(dict):
            b.connect(i,key,value)
            i += 1
            time.sleep(2)
        else:
            print('信息存储完成')
