# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup
import time
import sqlite3
import math
import sys, traceback

# note
# 1. string 과 get_text() 의 차이는?
# 2. soup.prettify()

driver = webdriver.Chrome()
db = sqlite3.connect("./wishket.sqlite")
dbCur = db.cursor()

class WishProject:
    skills = ""   # 사용스킬
    subCat = ""   # 분야
    inhouse = ""  # 상주여부
    applied = ""  # 지원자
    desc = ""
    name = ""
    price = ""
    duration = "" # 예상기간 
    date = ""     # 등록일
    sec = None    # sector 

    def __init__(self, sector):
        self.sec = sector

    def analyze(self):
        _heading = self.sec.find('div', class_='project-unit-heading')
        _name = _heading.find('a').get_text().strip()
    
        self.name = _name.replace("'","''")

        print(self.name)

        _body = self.sec.find('div', class_='project-unit-body')
        _basic_info = _body.find('div', class_='project-unit-basic-info')

        _price = _basic_info.find('span')
        self.price = _price.get_text().replace(u'예상금액','').replace(u'원','').replace(',','').strip()

        print(self.price)

        _duration = _price.findNext('span')
        self.duration = _duration.get_text().replace(u'예상기간','').replace(u'일','').strip()
        print(self.duration)

        _date = _duration.findNext('span')
        self.date = _date.get_text().replace(u'등록일자','').strip()

        print(self.date)

        _skills = self.sec.find_all('span', class_='skills-tag')
        for _sk in _skills:
            self.skills += _sk.get_text().lower() + ' '
            #self.skills += _sk.get_text()

        print(self.skills)

        try :
            self.inhouse = self.sec.find('div', class_='inhouse-status').get_text()
        except :
            self.inhouse = ""
            pass
        print(self.inhouse)

        self.subCat = self.sec.find('span', class_='project-subcategory').get_text()

        print(self.subCat )

        try :
            _applied = self.sec.find('span', class_='applied').get_text()
            self.applied = _applied.replace(u'총','').replace(u'명','').replace(u'지원','').strip()
        except:
            # 지원자 없음.
            self.applied = '0'
            pass

        print(self.applied)

        _desc = self.sec.find('div', class_='project-unit-desc').p.get_text()
        self.desc = _desc.replace("'","''")
        print(self.desc)

    def insertDb(self):
        print( "----- insert DB ----" )
        _pay = int(self.price) * 30 / int(self.duration)
        print( _pay )
        _pay = math.trunc( round ( _pay, -3 ) )
        print( "DB PAY : %d" % (_pay)  )

        dbCur.execute("REPLACE INTO project VALUES(" + 
                "'" + self.name + "'," +
                      self.price + "," +
                      self.duration + "," +
                      str(_pay) + "," +
                "'" + self.date + "'," +
                "'" + self.skills + "'," +
                "'" + self.subCat + "'," +
                "'" + self.applied + "'," +
                "'" + self.inhouse + "'," +
                "'" + self.desc + "');"  )

        print( "----- execute success ----" )

        db.commit()
        print( "----- COMMIT DB ----" )

def page_loop( searchType ):
    # next page click
    while True:
        try:
            nextBtn = driver.find_element_by_class_name('next')
            # just for implicit waits
            driver.find_element_by_class_name('project-unit-heading')
            #time.sleep(5)

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            if searchType == 'all' :
                sections = soup.find_all('section', class_='project-unit')
            elif searchType == 'new' :
                sections = soup.find_all('section', class_='opened-project')
                if len(sections) == 0 :
                    return 1

            for sec in sections:
                _project = WishProject(sec)
                _project.analyze()
                _project.insertDb()

            nextBtn.click()
            time.sleep(30)
        except:
            traceback.print_exc( file=sys.stdout )
            #driver.close();
            while True:
                pass
            pass

    return 0

def show_html_source():
    # just for implicit waits
    driver.find_element_by_class_name('project-unit-heading')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print( soup.prettify().encode('utf-8', errors='ignore') )
    driver.close()
    exit()


if __name__== "__main__":
    driver.get('https://www.wishket.com/project/#')
    driver.implicitly_wait(10)

    #개발 filter click
    driver.find_element_by_id('dev').click()

    #최신 등록순??? TODO
    #print( driver.find_element_by_class_name("sort-item").text )

    exit()
    #show_html_source()

    # DB init  Create Table
    dbCur.execute("CREATE TABLE IF NOT EXISTS project( name text primary key, price int, duration int, pay int, date text, skill text, category text, applied int, inhouse text,desc text);")

    page_loop('new')

    db.close()
    #driver.close()     #의도적으로 close 안시킴 마지막 상태 디버깅용



