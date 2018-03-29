import urllib2
response=urllib2.urlopen("http://www.sehir.edu.tr/Pages/anasayfa.aspx")
html_doc=response.read()
print html_doc

from bs4 import BeautifulSoup
soup=BeautifulSoup(html_doc,"html.parser")
print soup.title
print soup.title.name
print soup.title.string
