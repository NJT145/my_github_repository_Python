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
for i1 in soup.find_all(class_="fakulte_ack"):
    i1.prettify()
soup_div_list=soup.find_all(class_="fakulte_ack")

text_list=[]
for i2 in soup_div_list:
    text_list.append(i2.text.strip())

text=""
for i3 in text_list:
    for n in i3.split():
        text+=" "+n

print text

course_names=[]

for i4 in soup_div_list:
    if clickCourseDescriptions==True:
        if i4.strong!=None:
            for s in i4.find_all("strong"):
                split=s.text.split()
                if split!=[] and len(split)>2:
                    text1=" ".join(split[:3])
                    text2=" ".join(split)
                    warning=False
                    if text1.find("ECTS")!=-1:
                        warning=True
                    if text1.find("credits") != -1:
                        warning = True
                    if warning==False:
                        if text1 not in course_names:
                            course_names.append(text2)
                            print text2
                            print text2.find("EECS")

    else:
        if i4.p != None:
            for s in i4.find_all("p"):
                text1 = " ".join(s.text.split())
                if text1.find("UNI") != -1:
                    course_names.append(text1)

list3=[]
firstStep=text.split(course_names[0])[1]
secondStep=firstStep.split(course_names[1])
list3.extend(secondStep)
list4=list3
for i5 in range(len(course_names)-2):
    x = i5+2
    list5=[]
    list5.extend(list4[:(len(list4)-1)])
    item=list4[len(list4)-1]
    splitItem=item.split(course_names[x])
    list5.extend(splitItem)
    list4=list5
descriptions_list=list4


print len(course_names)
print clickCourseDescriptions

print len(descriptions_list)
print descriptions_list
print len(descriptions_list)