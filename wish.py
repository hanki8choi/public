# -*- coding:utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome()

driver.get('https://www.wishket.com/project/#')
driver.implicitly_wait(3)

soup = BeautifulSoup(driver.page_source, 'html.parser');

#show source
#print( soup.prettify().encode('utf-8', errors='ignore') )
#exit()

section = soup.find_all('section', class_='project-unit')

#string 과 get_text() 의 차이는?

for sec in section:
    #print(sec.div.h4.string )
    heading = sec.find('div', class_='project-unit-heading')
    strName = heading.find('a').get_text().strip()
    
    body = sec.find('div', class_='project-unit-body')
    basic_info = body.find('div', class_='project-unit-basic-info')

    #print( basic_info.prettify() )

    price = basic_info.find('span')
    strPrice = price.get_text().replace(u'예상금액','').replace(u'원','').replace(',','').strip()
    duration = price.findNext('span')
    strDuration = duration.get_text().replace(u'예상기간','').replace(u'일','').strip()
    date_recruit = duration.findNext('span')
    strDateRecruit = date_recruit.get_text().replace(u'등록일자','').strip()
    print( "%s  :  '%s' won   '%s' days   '%s'" % ( strName, strPrice, strDuration, strDateRecruit ) )


    #body = heading.findNext('div'
    #print( head.prettify() )
    #print( head.h4.string )
    #print( sec.div.find_next_siblings('div') )
    #body = sec.div.find_next_siblings('div')
    #print( body.prettify() )
    #body2 = body.find_next_siblings('div')
    #print( body2 )
    #new_div = section.div.next_sibling
    #print(new_div)



#for num in range(len(section)):
#    print( num )
#    print( section[num].get_text())

#elem = driver.find_element_by_class_name("partners-unit")
#elem = driver.find_element_by_class_name("content-inner")

#print(elem)

driver.close();

