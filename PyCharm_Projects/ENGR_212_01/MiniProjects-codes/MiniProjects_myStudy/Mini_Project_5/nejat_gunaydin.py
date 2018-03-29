"""
My references:
* for listbox with scrollbar, i used codes in :
        #http://www.java2s.com/Tutorial/Python/0360__Tkinker/ListBoxwithscrollbar.htm
        #http://stackoverflow.com/questions/12388604/the-horizontal-scrollbar-didnt-work-in-tkinter
* for checkButtons, i used codes in :
        #http://www.tutorialspoint.com/python/tk_checkbutton.htm
        #http://effbot.org/tkinterbook/checkbutton.htm
* for calculation of elapsed time, i used codes in :
        #http://stackoverflow.com/questions/3620943/measuring-elapsed-time-with-the-time-module
* in order to create my warning message boxes, i used this one :
        #http://www.tutorialspoint.com/python/tk_messagebox.htm

* i took some functions (such as separatewords(), and so on...) from mysearchengine.py
*the rest was mostly referenced from LMS files and from lessons.
"""

#-*- coding: utf-8 -*-


from Tkinter import *
import tkMessageBox
import urllib2
import shelve
from bs4 import BeautifulSoup
from urlparse import urljoin
import time
import re


# Separate the words by any non-whitespace character
def separatewords(text):
    splitter = re.compile('\\W*')
    return [s.lower() for s in splitter.split(text) if s != '']

class SEHIRResearchProjectsAnalyzer(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.url = None
        self.url_broken=False
        self.no_click_to_BuilIndex=False
        self.keyword=""
        self.paperTypes=None
        self.weight1=""
        self.weight2=""
        self.PublicationsResultsFrame=None
        self.startTime1=None
        self.elapsed1=None
        self.startTime2=None
        self.elapsed2=None
        self.initUI()

    def initUI(self):
        self.pack(fill=BOTH, expand=True)

        #title line
        var = StringVar()
        var.set("SEHIR Scholar")
        title = Label(self, textvariable=var, bg="blue", fg="white", font='Verdana 14 bold')
        title.pack(fill=X)

        buildIndexframe=Frame(self)

        Label(buildIndexframe, text="URL for faculty list:").pack(side=LEFT)

        self.urlbox = Entry(buildIndexframe, width=50)
        self.urlbox.insert(0, "http://cs.sehir.edu.tr/en/people/")
        self.urlbox.pack(side=LEFT, padx=60)

        Button(buildIndexframe, text="Build Index", relief=RIDGE, font="Verdana 8",
               command=self.onClickBuildIndex).pack(side=LEFT)

        buildIndexframe.pack(pady=10)

        searchSettingsFrame=Frame(self)

        self.keywordsBox=Entry(searchSettingsFrame, width=100)
        self.keywordsBox.pack()

        settingsANDsearchButtonFrame=Frame(searchSettingsFrame)

        rankingCriteriaFrame=Frame(settingsANDsearchButtonFrame)
        Label(rankingCriteriaFrame, text="Ranking Criteria", font="Verdana 9 bold").pack()
        self.CheckVar1 = IntVar()
        self.CheckVar1.set(1)
        self.CheckVar2 = IntVar()
        self.CheckVar2.set(1)
        Checkbutton(rankingCriteriaFrame, text="Word Frequency", variable = self.CheckVar1,
                                        onvalue = 1, offvalue = 0).pack(pady=5)
        Checkbutton(rankingCriteriaFrame, text="Citation Count", variable = self.CheckVar2,
                                        onvalue = 1, offvalue = 0).pack(pady=5)
        rankingCriteriaFrame.pack(side=LEFT, padx=5)

        weightFrame = Frame(settingsANDsearchButtonFrame)
        Label(weightFrame, text="Weight", font="Verdana 9 bold").pack()
        self.weight1BoxVar=StringVar()
        self.weight1Box=Entry(weightFrame, textvariable=self.weight1BoxVar, width=5)
        self.weight1BoxVar.set("1")
        self.weight1Box.pack(pady=8)
        self.weight2BoxVar=StringVar()
        self.weight2Box = Entry(weightFrame, textvariable=self.weight2BoxVar, width=5)
        self.weight2BoxVar.set("1")
        self.weight2Box.pack(pady=8)
        weightFrame.pack(side=LEFT, padx=10)

        paperTypeFilterFrame=Frame(settingsANDsearchButtonFrame)
        Label(paperTypeFilterFrame, text="Filter Papers", font="Verdana 9 bold").pack()
        listBoxWithScrollbarXY = Frame(paperTypeFilterFrame)
        scrollbarX = Scrollbar(listBoxWithScrollbarXY, orient=HORIZONTAL)
        listBoxWithScrollbar=Frame(listBoxWithScrollbarXY)
        scrollbarY = Scrollbar(listBoxWithScrollbar)
        self.mylist = Listbox(listBoxWithScrollbar, height=5, width=50, selectmode=MULTIPLE,
                              xscrollcommand=scrollbarX.set, yscrollcommand=scrollbarY.set)
        self.mylist.bind("<<ListboxSelect>>", self.OnClick)
        scrollbarY.config(command=self.mylist.yview)
        scrollbarX.config(command=self.mylist.xview)
        self.mylist.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbarY.pack(side=LEFT, fill=Y)
        listBoxWithScrollbar.pack()
        scrollbarX.pack(fill=X)
        listBoxWithScrollbarXY.pack()
        paperTypeFilterFrame.pack(side=LEFT, padx=5)

        Button(settingsANDsearchButtonFrame, text="Search", relief=RIDGE, font="Verdana 8",
               command=self.onClickSearch).pack(side=LEFT, padx=20)

        settingsANDsearchButtonFrame.pack(pady=10)

        searchSettingsFrame.pack(pady=10)

        self.searchResultsFrame=Frame(self)

        self.searchResultsFrame.pack(pady=10)

    def onClickBuildIndex(self):
        self.url = self.urlbox.get()
        self.buildTheShelveDb(self.url)
        self.mylist.delete(0, END)  # we need to reflesh self.mylist
        if self.paperTypes==None or self.paperTypes==[]:
            self.url_broken=True
        if self.url_broken==True:
            tkMessageBox.showinfo("Warning!","This is not a valid url.")
        else:
            for i in range(len(self.paperTypes)):
                self.mylist.insert(END, self.paperTypes[i])
                self.mylist.select_set(0,END)
            self.value=[]
            selection=self.mylist.curselection()
            for select in selection:
                value = self.mylist.get(select)
                self.value.append(value)  # insert our selection into our selection list self.value
        self.url_broken=False

    def buildTheShelveDb(self, url):

        #let's start timer for that
        self.startTime1=time.time()

        pageInfo = None

        try:
            pageInfo = urllib2.urlopen(url).read()
        except:
            self.url_broken = True

        if self.url_broken == False:
            soup = BeautifulSoup(pageInfo, "html.parser")
            linksSoup = soup('a')
            dbtable = shelve.open("dbtable.db",flag="n", writeback=True)
            """
            dbtable["names"][url_new]=name
            dbtable["publications"][paperType][citationNo]=PubTextList
            """
            dbtable.setdefault("names", {})
            links = []
            for link in linksSoup:
                if link.has_attr('href'):
                    href = dict(link.attrs)['href']
                    if href.find("/") != -1 and href.find(":") == -1:
                        href_splitted = href.split("/")
                        for str1 in url.split("/"):
                            for str2 in href_splitted:
                                if str1 != "" and str2 != "" and str1 == str2 and "profile" in href_splitted:
                                    url_new = urljoin(url, link['href'])
                                    if url_new not in links:
                                        nameSplitted = link.text.split()
                                        name = " ".join(nameSplitted)
                                        dbtable["names"].setdefault(url_new, {})
                                        dbtable["names"][url_new] = name

            dbtable.setdefault("publications", {})
            paper_types_all = []
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
                contentlist = []
                for i in publications_in_div_tag_list:
                    contentlist = i.contents
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

                for pub in publications_in_div_tag_list:
                    for ul in pub.find_all("ul"):
                        n = 0
                        while n < (len(types_index) - 1):
                            (index1, type1) = types_index[n]
                            (index2, type2) = types_index[n + 1]
                            dbtable["publications"].setdefault(type1.text, {})
                            for content in contentlist[int(index1):int(index2)]:
                                if ul == content:
                                    for li in ul.find_all("li"):
                                        textOnly = li.text
                                        splitted = textOnly.split()
                                        textSplitted = splitted
                                        if (splitted[len(splitted) - 1] == 'Citations]' or splitted[
                                                len(splitted) - 1] == 'Citation]'):
                                            textSplitted = splitted[:len(splitted) - 2]
                                        text = " ".join(textSplitted[1:])

                                        citation_html = li.a
                                        citation = "0"
                                        if citation_html != None:
                                            citation = li.a.text.split()[0][1:]
                                        else:
                                            citation="0"
                                        dbtable["publications"][type1.text].setdefault(citation, [])

                                        if text not in dbtable["publications"][type1.text][citation]:
                                            dbtable["publications"][type1.text][citation].append(text)

                            n = n + 1

            paper_types_all.sort()
            self.paperTypes=paper_types_all
            dbtable.close()
        self.elapsed1=time.time()-self.startTime1

    def OnClick(self, event):
        widget = event.widget
        selection = widget.curselection()
        self.value = []
        for i in selection:
            value = widget.get(i)
            self.value.append(value)  # insert our selection into our selection list self.value

    def onClickSearch(self):

        self.keyword=self.keywordsBox.get()
        self.weight1=self.weight1Box.get()
        self.weight2=self.weight2Box.get()

        if self.PublicationsResultsFrame != None:
            self.PublicationsResultsFrame.destroy()

        if self.paperTypes == None or self.paperTypes == []:
            tkMessageBox.showinfo("Warning!", "What? You need to click to 'Built Index' button at first!")
            self.no_click_to_BuilIndex = True

        if self.no_click_to_BuilIndex==True:
            pass
        else:
            if self.keyword=="":
                tkMessageBox.showinfo("Warning!", "Please enter a keyword.")
            else:
                if (self.CheckVar1.get()==1 and self.CheckVar2.get()==1):
                    if (self.weight1=="" or self.weight2==""):
                        tkMessageBox.showinfo("Warning!", "Hey mate, if you select both of two ranking criteria, "+
                                                          "you need to tell me their weights.")
                    else:
                        if self.value==[]:
                            tkMessageBox.showinfo("Warning!", "Without any choice for paper type? What do you mean?" +
                                                  "Just choose some of theeeem!!!!!!!.")
                        else:
                            try:
                                self.startTime2=time.time()
                                combinationScoreList=self.combinationScoreBasedList(self.keyword,int(self.weight1),int(self.weight2))
                                combinationScoreList.sort(reverse=True)
                                self.elapsed2 = time.time() - self.startTime2
                                self.functionPublicationsResultsFrame(combinationScoreList)
                            except:
                                tkMessageBox.showinfo("Warning!", "Are you kidding me? ENTER INTEGER FOR WEIGHTS!!!!")
                elif (self.CheckVar1.get()==0 and self.CheckVar2.get()==0):
                    tkMessageBox.showinfo("Warning!", "Please select a ranking criteria, brooo :-) .")
                else:
                    if self.value == []:
                        tkMessageBox.showinfo("Warning!", "Without any choice for paper type? What do you mean?" +
                                              "Just choose some of theeeem!!!!!!!.")
                    else:
                        if (self.CheckVar1.get()==1):
                            self.startTime2 = time.time()
                            frequencyScoreList=self.frequencyScoreBasedList(self.keyword)
                            frequencyScoreList.sort(reverse=True)
                            self.elapsed2 = time.time() - self.startTime2
                            self.functionPublicationsResultsFrame(frequencyScoreList)
                        else:
                            self.startTime2 = time.time()
                            citationScoreList=self.citationNumBasedList(self.keyword)
                            citationScoreList.sort(reverse=True)
                            self.elapsed2 = time.time() - self.startTime2
                            self.functionPublicationsResultsFrame(citationScoreList)

    def functionPublicationsResultsFrame(self, results):
        self.PublicationsResultsFrame = Frame(self.searchResultsFrame)
        text="%d Publications found (in %f seconds at total) " % ((len(results)),(self.elapsed1+self.elapsed2))
        Label(self.PublicationsResultsFrame, text=text+" "*108, fg="red", font='Verdana 10 bold').pack()
        #self.pagesDict=self.pagination(results)
        print results
        TextBoxWithScrollbar = Frame(self.PublicationsResultsFrame)
        scrollbar = Scrollbar(TextBoxWithScrollbar)
        self.TextBox = Text(TextBoxWithScrollbar, height=15, width=100,
                              yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.TextBox.yview)
        self.TextBox.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=LEFT, fill=Y)
        self.TextBox.insert(END, "agxsaclsa"*500+"\n\n")
        self.TextBox.configure(state="disabled")
        TextBoxWithScrollbar.pack()
        paginationFrame=Frame(self.PublicationsResultsFrame)
        Label(paginationFrame, text=(" "*190)+"Page:"+" "*10).pack(side=LEFT)
        Button(paginationFrame, text="Previous", relief=RIDGE, font="Verdana 7",
               command=self.onClickPrevious).pack(side=LEFT, padx=5)
        self.pageNoEntry=Entry(paginationFrame, width=5)
        self.pageNoEntry.insert(0,"1")
        self.pageNoEntry.configure(state="disabled")
        self.pageNoEntry.pack(side=LEFT)
        Button(paginationFrame, text="Next", relief=RIDGE, font="Verdana 7",
               command=self.onClickNext).pack(side=LEFT, padx=5)
        paginationFrame.pack(pady=5)
        self.PublicationsResultsFrame.pack()

    def pagination(self, results):
        pageNoMax =(len(results)/10)+(len(results)%10)
        pagesDict={}
        pageNo=1
        pubNo=1
        while pubNo<=len(results):
            while pageNo<=pageNoMax:
                text_page = ""
                for Num in range(10):
                    for num in range(len(results)):
                        for (score,texT) in results[num]:
                            text="\n"+str(pubNo)+".\t\t"+texT+"\t"+(score)
                            text_page+=text
                        pubNo+=1
                pagesDict[pageNo]=text_page
                pageNo+=1

        return results

    def onClickPrevious(self):
        print self.pageNoEntry.get()

    def onClickNext(self):
        print self.pageNoEntry.get()

    #this is an adaptation of frequencyscore() in mysearchengine.py
    def frequencyScoreBasedList(self, keyword):
        resultsDict={}
        keywordSplitted=separatewords(keyword)
        dbtable = shelve.open("dbtable.db", flag="c", writeback=True)
        for paperType in dbtable["publications"]:
            for citationNo in dbtable["publications"][paperType]:
                for text in dbtable["publications"][paperType][citationNo]:
                    for keywords in keywordSplitted:
                        frequency = 0
                        textSplitted = separatewords(text)
                        for no in range(len(textSplitted)):
                            if keywords==textSplitted[no]:
                                frequency+=1
                        if frequency!=0:
                            resultsDict.setdefault(text, [])
                            resultsDict[text].append(frequency)
        dbtable.close()

        results = []
        for TeXT in resultsDict:
            score = 1
            for No in resultsDict[TeXT]:
                score = score * No
            results.append((score, TeXT))

        if results==[]:
            return []
        else:
            frequencies = []
            for (Frequency, Text) in results:
                frequencies.append(Frequency)
            frequencies.sort(reverse=True)
            maxscore = frequencies[0]
            totalscore=float(FRequency)/maxscore
            return [(str(totalscore), TexT) for (FRequency, TexT) in results]

    #here, i used codes of normalizescores() in mysearchengine.py
    def citationNumBasedList(self, keyword):
        resultsDict={}
        keywordSplitted=separatewords(keyword)
        dbtable = shelve.open("dbtable.db", flag="c", writeback=True)
        for paperType in dbtable["publications"]:
            for citationNo in dbtable["publications"][paperType]:
                for text in dbtable["publications"][paperType][citationNo]:
                    for keywords in keywordSplitted:
                        keywordFound=False
                        textSplitted=separatewords(text)
                        for no in range(len(textSplitted)):
                            if keywords == textSplitted[no]:
                                keywordFound=True
                        if keywordFound==True:
                            resultsDict.setdefault(text, [])
                            resultsDict[text].append(int(citationNo))
        dbtable.close()

        results=[]
        for TeXT in resultsDict:
            score=1
            for No in resultsDict[TeXT]:
                score=score*No
            results.append((score, TeXT))

        if results == []:
            return []
        else:
            vsmall = 0.00001  # Avoid division by zero errors
            citationNos = []
            for (CitationNo, Text) in results:
                citationNos.append(CitationNo)
                citationNos.sort(reverse=True)
            maxscore = citationNos[0]
            if maxscore == 0:
                maxscore = vsmall
            return [(str(float(CitationNo) / maxscore), TexT) for (CitationNo, TexT) in results]

    #this is an adaptation of getscoredlist() in mysearchengine.py
    def combinationScoreBasedList(self, keyword, weight1, weight2):
        frequencyScoreResult = self.frequencyScoreBasedList(keyword)
        citationScoreResult = self.citationNumBasedList(keyword)

        textList=[]
        for (Score1,Text1) in frequencyScoreResult:
            if Text1 not in textList:
                textList.append(Text1)
        for (Score2, Text2) in citationScoreResult:
            if Text2 not in textList:
                textList.append(Text2)

        results=[]
        for TExt in textList:
            totalScore=0
            for (score1, text1) in frequencyScoreResult:
                if TExt==text1:
                    totalScore=totalScore+weight1*float(score1)
            for (score2, text2) in citationScoreResult:
                if TExt == text2:
                    totalScore = totalScore + weight2 * float(score2)
            results.append((str(totalScore), TExt))

        if results == []:
            return []
        else:
            vsmall = 0.00001  # Avoid division by zero errors
            totalScores = []
            for (totalScore, Text) in results:
                totalScores.append(totalScore)
                totalScores.sort(reverse=True)
            maxscore = totalScores[0]
            if maxscore == 0:
                maxscore = vsmall
            return [((float(TotalScore) / maxscore), TexT) for (TotalScore, TexT) in results]

def main():
    root = Tk()
    root.wm_title("SEHIR Scholar")
    root.geometry("1010x620+150+30")
    app = SEHIRResearchProjectsAnalyzer(root)
    root.mainloop()

if __name__ == '__main__':
    main()

