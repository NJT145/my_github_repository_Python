import urllib2
from bs4 import BeautifulSoup
from urlparse import urljoin
import re
import shelve
from django.utils.encoding import smart_str

# Create a list of words to ignore
ignorewords = set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it'])


class crawler:
    # Initialize the crawler with the name of database tabs
    def __init__(self, dbtables):
        self.dbtables = dbtables

    def __del__(self):
        self.close()

    def close(self):
        self.urllist.close()
        self.wordlocation.close()
        self.link.close()
        self.linkwords.close()

    # Index an individual page
    def addtoindex(self, url, soup):
        if self.isindexed(url):
            print 'skip', url + ' already indexed'
            return False

        print 'Indexing ' + url

        # Get the individual words
        text = self.gettextonly(soup)
        words = self.separatewords(text)

        # Record each word found on this page
        for i in range(len(words)):
            word = smart_str(words[i])

            if word in ignorewords:
                continue

            if not self.wordlocation.has_key(word):
                self.wordlocation[word] = {}

            self.wordlocation[word].setdefault(url, [])
            self.wordlocation[word][url].append(i)

        return True

    # Extract the text from an HTML page (no tags)
    def gettextonly(self, soup):
        v = soup.string
        if v == None:
            c = soup.contents
            resulttext = ''
            for t in c:
                subtext = self.gettextonly(t)
                resulttext += subtext + '\n'
            return resulttext
        else:
            return v.strip()

    # Separate the words by any non-whitespace character
    def separatewords(self, text):
        splitter = re.compile('\\W*')
        return [s.lower() for s in splitter.split(text) if s != '']

    # Return true if this url is already indexed
    def isindexed(self, url):
        # urllist = {url:outgoing_link_count}
        if not self.urllist.has_key(smart_str(url)):
            return False
        else:
            return True


    # Add a link between two pages
    def addlinkref(self, urlFrom, urlTo, linkText):
        fromUrl = smart_str(urlFrom)
        toUrl = smart_str(urlTo)

        if fromUrl == toUrl: return False

        if not self.link.has_key(toUrl):
            self.link[toUrl] = {}

        self.link[toUrl][fromUrl] = None

        words=self.separatewords(linkText)
        for word in words:
            word = smart_str(word)

            if word in ignorewords: continue

            if not self.linkwords.has_key(word):
                self.linkwords[word] = []

            self.linkwords[word] = [(fromUrl, toUrl)]

        return True

    # Starting with a list of pages, do a breadth
    # first search to the given depth, indexing pages
    # as we go
    def crawl(self, pages, depth=2):
        for i in range(depth):
            newpages = set()
            for page in pages:
                try:
                    c = urllib2.urlopen(page)
                except:
                    print "Could not open %s" % page
                    continue
                soup = BeautifulSoup(c.read(), 'html.parser')
                added = self.addtoindex(page, soup)

                if not added:
                    continue

                outgoingLinkCount = 0
                links = soup('a')
                for link in links:
                    if 'href' in dict(link.attrs):
                        url = urljoin(page, link['href'])
                        if url.find("'") != -1:
                            continue
                            # The fragment identifier introduced
                            # by a hash mark (#) is the optional last
                            # part of a URL for a document. It is typically
                            # used to identify a portion of that document.
                        url = url.split('#')[0]  # remove location portion
                        if url[0:4] == 'http' and not self.isindexed(url):
                            newpages.add(url)
                        linkText = self.gettextonly(link)
                        added = self.addlinkref(page, url, linkText)
                        if added:
                            outgoingLinkCount += 1

                self.urllist[smart_str(page)] = outgoingLinkCount
            pages = newpages


    # Create the database tables
    def createindextables(self):
        # {url:outgoing_link_count}
        self.urllist = shelve.open(self.dbtables['urllist'], writeback=True, flag='c')
        #{word:{url:[loc1, loc2, ..., locN]}}
        self.wordlocation = shelve.open(self.dbtables['wordlocation'], writeback=True, flag='c')
        #{tourl:{fromUrl:None}}
        self.link = shelve.open(self.dbtables['link'], writeback=True, flag='c')
        #{word:[(urlFrom, urlTo), (urlFrom, urlTo), ..., (urlFrom, urlTo)]}
        self.linkwords = shelve.open(self.dbtables['linkwords'], writeback=True, flag='c')
