import urllib2
from bs4 import BeautifulSoup
from urlparse import urljoin
import shelve

url='http://cs.sehir.edu.tr/en/people/'

url_is_broken=False
response=None

try:
    response = urllib2.urlopen(url)
except:
    print "Could not open %s" % url
    url_is_broken=True

if url_is_broken==False:
    html_doc = response.read()
    soup=BeautifulSoup(html_doc, 'html.parser')
    linksSoup=soup('a')
    dbtable = shelve.open("dbtable.db", writeback=True)
    dbtable.setdefault("names", {})
    links=[]
    str_start=[]
    for link in linksSoup:
        if link.has_attr('href'):
            href=dict(link.attrs)['href']
            if href.find("/")!=-1 and href.find(":")==-1:
                href_splitted=href.split("/")
                for str1 in url.split("/"):
                    for str2 in href_splitted:
                        if str1!="" and str2!="" and str1==str2 and "profile" in href_splitted:
                            url_new = urljoin(url, link['href'])
                            if url_new not in links:
                                nameSplitted=link.text.split()
                                name=" ".join(nameSplitted)
                                dbtable["names"].setdefault(url_new, {})
                                dbtable["names"][url_new]=name

    dbtable.setdefault("publications", {})

    paper_types_all=[]
    for link in dbtable["names"].keys():
        c = urllib2.urlopen(link)
        html_doc2 = c.read()
        soup2 = BeautifulSoup(html_doc2, 'html.parser')
        publications_in_div_tag_list = []
        for part in soup2.find_all("div"):
            if part.text.find(("Publications:")) != -1:
                for a in part.find_all(id="publication"):
                    if a not in publications_in_div_tag_list:
                        publications_in_div_tag_list.append(a)
        print dbtable["names"][link]
        contentlist = []
        for i in publications_in_div_tag_list:
            contentlist = i.contents
        print contentlist
        paper_types = []
        paper_types_dict = {}
        for i in publications_in_div_tag_list:
            for p in i.find_all("p"):
                paper_types_dict[p] = p.text
                paper_types.append(p.text)
                if p.text not in paper_types_all:
                    paper_types_all.append(p.text)

        types_index = []
        for types in paper_types_dict:
            for contentIndex in range(len(contentlist) - 1):
                if contentlist[contentIndex] == types:
                    types_index.append((str(contentIndex), types))
        types_index.sort()
        types_index.append((str(len(contentlist)), "END"))

        dbtable["publications"].setdefault("byPaperTypes", {})
        dbtable["publications"].setdefault("byCitations", {})
        byPublications = {}
        byCitation = {}
        for pub in publications_in_div_tag_list:
            for ul in pub.find_all("ul"):
                n = 0
                while n < (len(types_index) - 1):
                    (index1, type1) = types_index[n]
                    (index2, type2) = types_index[n + 1]
                    byPub={}
                    byPub.setdefault(type1, {})
                    for content in contentlist[int(index1):int(index2)]:
                        if ul == content:
                            for li in ul.find_all("li"):
                                textOnly = li.text
                                splitted = textOnly.split()

                                byPub[type1].setdefault(splitted[0],[])
                                byPub[type1][splitted[0]].append(splitted)
                    byPublications[type1]=byPub

                    for content in contentlist[int(index1):int(index2)]:
                        if ul == content:
                            for li in ul.find_all("li"):
                                textOnly = li.text
                                splitted = textOnly.split()
                                citation_html=li.a
                                if citation_html!=None:
                                    citation=li.a.text.split()[0][1:]
                                    byCitation[citation]=splitted
                    n=n+1
        dbtable["publications"]["byPaperTypes"]=byPublications
        dbtable["publications"]["byCitations"]=byCitation
        print paper_types
        print paper_types_dict
    paper_types_all.sort()
    print paper_types_all

    print dbtable.items()
    dbtable.close()



    #for href in dicti:
    #    print href
    #    print dicti[href]
    #
    print "---------------------------------------"
    url2="http://cs.sehir.edu.tr/en/profile/6/Ahmet-Bulut/"
    c=urllib2.urlopen(url2)
    html_doc2=c.read()
    soup2=BeautifulSoup(html_doc2, 'html.parser')
    publications_htmlDoc_list=[]
    for part in soup2.find_all("div"):
        if part.text.find(("Publications:"))!=-1:
            for a in part.find_all(id="publication"):
                if a not in publications_htmlDoc_list:
                    publications_htmlDoc_list.append(a)
    contentlist=[]
    for i in publications_htmlDoc_list:
        contentlist = i.contents
    paper_types=[]
    paper_types_dict={}
    for i in publications_htmlDoc_list:
        for p in i.find_all("p"):
            paper_types_dict[p]=p.text
            paper_types.append(p.text)
        print contentlist[1]==i.p
    print paper_types
    print paper_types_dict
    types_index=[]
    for types in paper_types_dict:
        for contentIndex in range(len(contentlist)-1):
            if contentlist[contentIndex]==types:
                types_index.append((str(contentIndex), types))
    types_index.sort()
    types_index.append((str(len(contentlist)), "END"))
    print types_index
    print contentlist[9:13]
    for pub in publications_htmlDoc_list:
        for a in pub.find_all("ul"):
            n = 0
            while n<(len(types_index)-1):
                dicti={}
                (index1,type1)=types_index[n]
                (index2,type2)=types_index[n+1]
                dicti.setdefault(type1,[])
                for content in contentlist[int(index1):int(index2)]:
                    if a==content:
                        for li in a.find_all("li"):
                            textOnly=li.text
                            splitted=textOnly.split()
                            textSplitted=splitted
                            if (splitted[len(splitted)-1]=='Citations]' or splitted[len(splitted)-1]=='Citation]'):
                                textSplitted=splitted[:len(splitted)-2]
                            text=" ".join(textSplitted[1:])
                            dicti[type1].append(text)

                print dicti
                n=n+1


            print 111111111111111111111111111111

"""
    paper_type_filter_htmlDoc_list=[]
    paper_type_filter_list=[]
    for i in publications_htmlDoc_list:
        for p in i.find_all("p"):
            paper_type_filter_htmlDoc_list.append(p)
            paper_type_filter_list.append(p.text)
        print i.text.split()
    for i in publications_htmlDoc_list:
        print i.p
        print i.p.next.next.next
    print paper_type_filter_list
    print paper_type_filter_htmlDoc_list
"""