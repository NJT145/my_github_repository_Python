from bs4 import BeautifulSoup
import urllib2

def make_soup(link):
    response = urllib2.urlopen(link)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    return soup


def get_awards(soup):
    data = {}
    base = "http://sehir.edu.tr"
    content = soup.find(id="icsayfa_sag")
    awards = soup.find_all(class_="ogr_ymetin")
    for a in awards:
        title = a.find("h1").text.strip()
        data.setdefault(title, {})
        info = a.find_next("div")
        try:
            date = info.find("em").text.strip()
        except AttributeError:
            date = info.find("i").text.strip()
        if len(date) > 10:
            date = date[3:]
        data[title]["date"] = date
        link = info.find("a")["href"]
        data[title]["link"] = base + link
    #print data
    return data


def print_awards(data):
    for key in data:
        print "Title :", key
        print "Date :", data[key]["date"]
        print "Link :", data[key]["link"]
        print "*"*50

soup = make_soup("http://www.sehir.edu.tr/en/Pages/NewsAndAnnouncements/AwardsandAchievements.aspx")
awards = get_awards(soup)
print_awards(awards)
