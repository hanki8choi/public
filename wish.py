# -*- coding:utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import time

# note
# 1. string 과 get_text() 의 차이는?
# 2. soup.prettify()

driver = webdriver.Chrome()

def parse_skill_tag(sec):
    skills = sec.find_all('span', class_='skills-tag')
    for sk in skills:
        print( sk.get_text() )

def parse_cat(sec):
    print( sec.find('span', class_='project-subcategory').get_text() )

def parse_applied(sec):
    try :
        text = sec.find('span', class_='applied').get_text()
        strApplied = text.replace(u'총','').replace(u'명','').replace(u'지원','').strip()
    except:
        # 지원자 없음.
        strApplied = 0
    finally:
        print( strApplied  )

def parse_desc(sec):
    text = sec.find('div', class_='project-unit-desc').p.get_text()
    print( text )

def page_analyzer():
    soup = BeautifulSoup(driver.page_source, 'html.parser');

    #print(soup)
    sections = soup.find_all('section', class_='project-unit')
    for sec in sections:
        heading = sec.find('div', class_='project-unit-heading')
        strName = heading.find('a').get_text().strip()
    
        body = sec.find('div', class_='project-unit-body')
        basic_info = body.find('div', class_='project-unit-basic-info')

        price = basic_info.find('span')
        strPrice = price.get_text().replace(u'예상금액','').replace(u'원','').replace(',','').strip()
        duration = price.findNext('span')
        strDuration = duration.get_text().replace(u'예상기간','').replace(u'일','').strip()
        date_recruit = duration.findNext('span')
        strDateRecruit = date_recruit.get_text().replace(u'등록일자','').strip()


        print( "%s  :  '%s' won   '%s' days   '%s'" % ( strName, strPrice, strDuration, strDateRecruit ) )

        parse_skill_tag(sec)
        parse_cat(sec)
        parse_applied(sec)
        parse_desc(sec)


def page_loop():
    # next page click
    while True:
        try:
            nextBtn = driver.find_element_by_class_name('next')
            # just for implicit waits
            driver.find_element_by_class_name('project-unit-heading')
            page_analyzer()
            nextBtn.click()
        except:
            print ( 'except' )
            driver.close();

if __name__== "__main__":
    driver.get('https://www.wishket.com/project/#')
    driver.implicitly_wait(10)

    #개발 filter click
    driver.find_element_by_id('dev').click()

    page_loop()

driver.close();

