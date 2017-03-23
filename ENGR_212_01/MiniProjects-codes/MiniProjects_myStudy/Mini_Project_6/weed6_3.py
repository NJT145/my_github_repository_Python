url1 = "http://www.sehir.edu.tr/en/Pages/Academic/Bolum.aspx?BID=12"
url2 = "http://www.sehir.edu.tr/en/Pages/Academic/Bolum.aspx?BID=13"
url3 = "http://www.sehir.edu.tr/en/Pages/Academic/Bolum.aspx?BID=14"
url4 = "http://www.sehir.edu.tr/en/Pages/Academic/Bolum.aspx?BID=32"

import time
from bs4 import BeautifulSoup
from selenium import webdriver

import docclass

driver = webdriver.Firefox()
driver.get(url2)
html = driver.page_source
element = driver.find_elements_by_tag_name("a")
elm=None
strong_or_span__strong=True
for i in element:
    if i.text=="Course Descriptions":
        i.click()
    else:
        strong_or_span__strong=False
time.sleep(2)
html_doc= driver.page_source
driver.close()
soup=BeautifulSoup(html_doc, "html.parser")
soup.prettify()
for i in soup.find_all(class_="fakulte_ack"):
    i.prettify()
soup_div_list=soup.find_all(class_="fakulte_ack")

text_list=[]
for i in soup_div_list:
    text_list.append(i.text.strip())

text=""
for i in text_list:
    for n in i.split():
        text+=" "+n

print text.strip()

course_names=[]


for i in soup_div_list:
    for s in i.find_all("strong"):
        texti = s.text
        print s.text.split()
        if len(s.text.split())>1:
            no_ECTS=True
            for t in s.text.split()[0:3]:
                if ("ECTS") in docclass.getwords(t) or ("credits") in docclass.getwords(t):
                    no_ECTS=False
            if no_ECTS==True:
                if s.text not in course_names:
                    course_names.append(s.text)
                    print 111, s.text
                    print s.text.split()

print len(course_names)
n=0
for i in course_names:
    if i.find("ECTS")!=-1:
        n+=1
print n