import csv
from math import *
import feedparser
import re
import os

i = 0


def getwords(html):
    # Remove all the HTML tags. Only words remain
    txt = re.compile(r'<[^>]+>').sub('', html)
    stripped = txt.strip()
    return stripped


#txt=name of the file that is saved="sportnews.txt" or "healthnews.txt"
#txt1 = name of the file that is opened="sport.txt" or "health.txt"
def getnews(txt, txt1):
    #Put the all entries in RSS to a txt file.
    for line in open(txt1):
        print 'processing ', line
        url = line
        d = feedparser.parse(url)
        for e in d.entries:
            #globalize local variable i
            global i
            i += 1
            title = getwords(e.title)
            if "summary" in e:
                summary = getwords(e.summary)
            elif "description" in e:
                summary = getwords(e.description)
            elif ("summary" in e) and ("description" in e):
                summary = getwords(e.description)
            else:
                summary = "N/A"
            save = open(txt, "a+")
            save.write(str(i) + ")\n")
            save.write("Title: " + title.encode("utf-8") + "\n")
            save.write("Description: " + summary.encode("utf-8") + "\n")
            save.write("\n")
            save.close()


def getnews2(text, name_of_file):
    count = 0
    with open(text) as txt:
        for url in txt:
            print 'processing2 ', url
            d = feedparser.parse(url)
            for e in d.entries:
                count += 1
                title = getwords(e.title)
                summary = "N/A"
                if "description" in e: summary = getwords(e.description)
                elif "summary" in e: summary = getwords(e.summary)
                save = open(name_of_file, "a+")
                save.write(str(count) + ")\n")
                save.write("Title: " + title.encode("utf-8") + "\n")
                save.write("Description: " + summary.encode("utf-8").strip() + "\n\n")
                save.close()


#getnews2("sport.txt", "getNews1234.txt")



# for this function, there is an alternative solution in book. It can be also used.
def most_frequent(txt):
    feedlist = []
    dictionary = {}
    for line in open(txt):
        feedlist.append(line)
        for word in line.strip().split(' '):
            #print re.sub(r'\W+', '', i)
            if word.lower() not in dictionary:
                dictionary[word.lower()] = 1
            else:
                dictionary[word.lower()] += 1

    #wordlist = dictionary.keys()
    wordlist = []
    for word, count in dictionary.items():
        frac = float(count) / len(feedlist)
        if 0.01 < frac < 0.2:
            if word not in wordlist:
                wordlist.append(word)
    return wordlist


def getWords_commonlyUsed(txt1, txt2):
    _list = list()
    list1 = most_frequent(txt1)
    list2 = most_frequent(txt2)
    for element in list1:
        if element in list2:
            _list.append(element)
    #some turkish characters can not be read, so if you want to see the word print the
    #element of the list3
    return _list

def getWords_commonlyUsed2(txt1, txt2):
    list1 = most_frequent(txt1)
    list2 = most_frequent(txt2)
    list1, list2 = set(list1), set(list2)
    return list1.intersection(list2)



