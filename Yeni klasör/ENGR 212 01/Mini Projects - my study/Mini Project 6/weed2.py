url1 = "http://www.sehir.edu.tr/en/Pages/Academic/Bolum.aspx?BID=12"
url2 = "http://www.sehir.edu.tr/en/Pages/Academic/Bolum.aspx?BID=13"
url3 = "http://www.sehir.edu.tr/en/Pages/Academic/Bolum.aspx?BID=14"
url4 = "http://www.sehir.edu.tr/en/Pages/Academic/Bolum.aspx?BID=32"



from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re
import docclass

driver = webdriver.Firefox()
driver.get(url4)
time.sleep(2)
html = driver.page_source
element = driver.find_elements_by_tag_name("a")
elm=None
clickCourseDescriptions=False
for i in element:
    if i.text=="Course Descriptions":
        i.click()
        clickCourseDescriptions=True
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

print text

course_names=[]
n=0
for i in soup_div_list:
    if i.p!=None:
        for s in i.find_all("p"):
            text1=" ".join(s.text.split())
            if text1.find("UNI")!=-1:
                course_names.append(text1)
                print text1
                print text1.find("UNI 100")
print len(course_names)
print clickCourseDescriptions
print n