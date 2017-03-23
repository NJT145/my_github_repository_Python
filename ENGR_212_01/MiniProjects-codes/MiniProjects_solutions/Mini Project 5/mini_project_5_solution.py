# -*- coding: utf-8 -*-

"""
ENGR 212 Spring 2016 Mini Project 5 Solution File
Doğukan Kotan <dogukankotan@std.sehir.edu.tr>

Starting '_<method_name>' functions are related to GUI.
"""
from Tkinter import *  # Python 2
from tkMessageBox import showerror, showwarning  # Python 2
from bs4 import BeautifulSoup
import urllib2
from urlparse import urljoin
import re
import shelve
import time


class SehirScholar(Frame):
    def __init__(self, master, db_tables):
        """

        :param master: initial window object of tkinter
        :return: None

        """
        """ Variables """
        Frame.__init__(self, master)
        self.root = master
        self.root.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.db_tables = db_tables
        self.ignore_words = ['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it']

        self.first_time = None
        self.last_time = None

        self.page_number = 1
        self.results = None

        # Frames
        self.top_frame = Frame(self.root)
        self.middle_frame = Frame(self.root)
        self.bottom_frame = Frame(self.root)

        # Labels
        self.title = Label(self.top_frame, text="SEHIR Scholar", bg="blue", fg="white",
                           font=("Comic Sans", 18), height=2)
        self.url_label = Label(self.middle_frame, text="Url for faculty list :", font=("Comic Sans", 10))
        self.ranking_label = Label(self.middle_frame, text="Ranking Criteria")
        self.weight_label = Label(self.middle_frame, text="Weight")
        self.filter_label = Label(self.middle_frame, text="Filter Papers")
        self.info_label = Label(self.bottom_frame, fg="red")
        self.page_label = Label(self.bottom_frame, text="Page:")
        self.page_number_label = Label(self.bottom_frame, text=self.page_number, relief=SUNKEN, bd=2, width=3,
                                       bg="blue", fg="white")

        # Entry
        self.link_entry = Entry(self.middle_frame, width=40, font=("Comic Sans", 10))
        self.link_entry.insert(0, "http://cs.sehir.edu.tr/en/people/")
        self.search_entry = Entry(self.middle_frame, width=50, font=("Comic Sans", 15))
        self.word_freq_entry = Entry(self.middle_frame, width=3, font=("Comic Sans", 8))
        self.word_freq_entry.insert(0, "1")
        self.cite_count_entry = Entry(self.middle_frame, width=3, font=("Comic Sans", 8))
        self.cite_count_entry.insert(0, "1")

        # Buttons
        self.build_button = Button(self.middle_frame, text="Build Index", font=("Comic Sans", 10),
                                   command=self._build_index)
        self.search_button = Button(self.middle_frame, text="Search", font=("Comic Sans", 10), command=self._search)
        self.pre_button = Button(self.bottom_frame, text="Previous", font=("Comic Sans", 10), state=DISABLED,
                                 command=self._previous_page)
        self.next_button = Button(self.bottom_frame, text="Next", font=("Comic Sans", 10), state=DISABLED,
                                  command=self._next_page)

        # Checkboxes
        self.check_var_word = IntVar()
        self.check_var_cite = IntVar()

        self.word_freq_check = Checkbutton(self.middle_frame, text="Word Frequency", variable=self.check_var_word,
                                           onvalue=1, offvalue=0)
        self.cite_count_check = Checkbutton(self.middle_frame, text="Citation Count", variable=self.check_var_cite,
                                            onvalue=1, offvalue=0)
        self.check_var_word.set(1)
        self.check_var_cite.set(1)

        # Listbox
        self.listbox = Listbox(self.middle_frame, height=5, width=15, selectmode='multiple')

        # Scrollbar
        self.listhbar = Scrollbar(self.middle_frame, orient=VERTICAL, command=self.listbox.yview)
        self.listwbar = Scrollbar(self.middle_frame, orient=HORIZONTAL, command=self.listbox.xview)
        self.listbox.config(yscrollcommand=self.listhbar.set)
        self.listbox.config(xscrollcommand=self.listwbar.set)

        # Text
        self.textw = Text(self.bottom_frame, width=110, height=24, font=("Comis Sans", 9))
        self.texthbar = Scrollbar(self.bottom_frame, orient=VERTICAL, command=self.textw.yview)
        self.textw.config(yscrollcommand=self.texthbar.set)

        self._customize()

    def _customize(self):
        # Frames
        self.top_frame.grid(row=0, sticky=W + E)
        self.top_frame.columnconfigure(0, weight=1)
        self.middle_frame.grid(row=1, pady=10)
        self.bottom_frame.grid(row=2, pady=10)

        # Top Frame
        self.title.grid(sticky=W + E)

        # Middle Frame
        self.url_label.grid(row=0, column=1)
        self.link_entry.grid(row=0, column=2, padx=10, columnspan=3)
        self.build_button.grid(row=0, column=7, padx=10)
        self.search_entry.grid(row=1, column=0, padx=10, columnspan=10, pady=10)

        self.ranking_label.grid(row=2, column=2, sticky=W)
        self.word_freq_check.grid(row=3, column=2, sticky=W)
        self.cite_count_check.grid(row=4, column=2, sticky=W)
        self.weight_label.grid(row=2, column=3, sticky=W)
        self.word_freq_entry.grid(row=3, column=3, sticky=W)
        self.cite_count_entry.grid(row=4, column=3, sticky=W)
        self.filter_label.grid(row=2, column=4, sticky=W, padx=20)
        self.listbox.grid(row=3, column=4, sticky=W + E, rowspan=2, columnspan=2)
        self.listwbar.grid(row=5, column=4, sticky=E + W, columnspan=2)
        self.search_button.grid(row=3, column=7)

        # Bottom frame
        self.info_label.grid(row=0, column=0)
        self.textw.grid(row=1, column=0, columnspan=20)
        self.texthbar.grid(row=1, column=21, sticky=N + S)
        self.page_label.grid(row=2, column=16, sticky=E)
        self.pre_button.grid(row=2, column=17, sticky=E)
        self.page_number_label.grid(row=2, column=18, sticky=E)
        self.next_button.grid(row=2, column=19, sticky=E)

    def __del__(self):
        """
        This method runs when the application ends.
        :return:
        """
        self.close_dbs()

    def close_dbs(self):
        if hasattr(self, 'publication_type'):
            self.publication_type.close()
        if hasattr(self, 'word_location'):
            self.word_location.close()
        if hasattr(self, 'citation_count'):
            self.citation_count.close()

    @staticmethod
    def make_soup(url):
        """

        :param url: page that wanted to convert soup object
        :return: soup object of that page
        """
        response = urllib2.urlopen(url)  # get html response
        html = response.read()  # read it
        soup = BeautifulSoup(html, "html.parser")  # create soup object
        return soup

    def _build_index(self):
        self.create_index_tables()
        gui_link = self.link_entry.get()
        creator_list = []
        try:
            soup = self.make_soup(gui_link)
        except urllib2.URLError:
            showerror("Error", "Could not open %s" % gui_link)
        else:
            for member in soup.find_all("div", {"class": "member"}):
                link_class = member.find("a")
                if 'href' in dict(link_class.attrs):
                    url = urljoin(gui_link, link_class['href'])
                    creator_list.append(url)
        for link in creator_list:
            try:
                soup = self.make_soup(link)
            except urllib2.URLError:
                showerror("Error", "Could not open %s" % link)
            else:
                self.add_to_index(soup)
                self.listbox.select_set(0, END)

    def _search(self):
        self.query(self.search_entry.get())

    def is_indexed(self, publication, citation):
        if publication in self.citation_count:
            if self.citation_count[publication] == citation:
                return True
            else:
                return False
        else:
            return False

    def add_to_index(self, s):
        pub_table = s.find("div", {"id": "publication"})
        types = pub_table.find_all("p")
        pubs_types = pub_table.find_all("ul")
        for i in range(len(types)):
            type_ = types[i].text.strip()
            if type_ not in self.listbox.get(0, END):
                self.listbox.insert(END, type_)
            pubs = pubs_types[i].find_all("li")
            for pub in pubs:
                p = pub.text.strip().replace("\n", "")[3:].strip()
                if p[0] == ".":
                    p = p[1:].strip()
                p = p.encode("utf-8")
                cite = pub.find("a")
                if cite is None:
                    cite = 0
                else:
                    cite = cite.text.replace("\n", "").strip().split(" ")[0][1:]
                    cite = int(cite)
                if self.is_indexed(p, cite):
                    continue
                self.add_to_types_dict(p, type_)
                self.add_to_cites_dict(p, cite)
                self.add_to_word_location(p)

    def add_to_word_location(self, publication):
        words = self.separate_words(publication)
        # Record each word found on this page
        for i, word in enumerate(words):
            if word in self.ignore_words:
                continue
            self.word_location.setdefault(word, {})

            self.word_location[word].setdefault(publication, [])
            self.word_location[word][publication].append(i)

    def add_to_types_dict(self, publication, _type):
        self.publication_type[publication] = _type

    def add_to_cites_dict(self, publication, citation):
        self.citation_count[publication] = citation

    @staticmethod
    # Separate the words by any non-whitespace character
    def separate_words(text):
        splitter = re.compile('\\W*')
        return [s.lower() for s in splitter.split(text) if s != '']

    def _filter(self, publication):
        checker = None
        for index in self.listbox.curselection():
            selected = self.listbox.get(index)
            if self.publication_type[publication] not in selected:
                checker = True
            else:
                checker = False
                return checker
        return checker

    def get_matching_pubs(self, q):
        results = {}
        # Split the words by spaces
        words = [word.encode("utf-8").lower() for word in q.split()]
        if words[0] not in self.word_location:
            return results, words

        pubs_set = set(self.word_location[words[0]].keys())

        for word in words[1:]:
            if word not in self.word_location:
                return results, words
            pubs_set = pubs_set.intersection(self.word_location[word].keys())

        for pub in pubs_set:
            if self._filter(pub):
                continue
            results[pub] = []
            for word in words:
                results[pub].append(self.word_location[word][pub])

        return results, words

    def query(self, q):
        self.first_time = time.time()
        try:
            results, words = self.get_matching_pubs(q)
            if len(self.listbox.curselection()) == 0:
                showwarning("Warning", "Please select at least one filter type!")
                return
            elif self.check_var_cite.get() == 0 and self.check_var_word.get() == 0:
                showwarning("Warning", "Please select one ranking criteria!")
                return
        except AttributeError:
            showwarning("Warning", "Please use build index button just before searching!")
        except IndexError:
            showwarning("Warning", "Please give at least one word to search!")
        else:
            if len(results) == 0:
                showwarning("Warning", "No matching pages found!")
                return
            try:
                scores = self.get_scored_list(results, words)
            except ValueError:
                showwarning("Warning", "Please give one ranking weight!")
            else:
                rankedscores = sorted([(score, pub) for (pub, score) in scores.items()], reverse=1)
                self._show_content(rankedscores)

    def _show_content(self, results):
        self.results = results
        self.last_time = time.time()
        self.next_button.config(state=DISABLED)
        self.pre_button.config(state=DISABLED)
        self.page_number = 1
        self.textw.delete(1.0, END)
        searching_time = self.last_time - self.first_time
        _info = "%d Publications (%.6f seconds)" % (len(results), searching_time)
        self.info_label.config(text=_info)
        page_numbers = len(results) / 10
        if page_numbers > 0:
            self.next_button.config(state=NORMAL)
        self._print_results()

    def _print_results(self):
        self.textw.tag_config("red", foreground="red", font=("Comis Sans", 9))
        self.textw.tag_config("blue", foreground="blue", font=("Comis Sans", 9, "bold"))
        for i, (score, pub) in enumerate(self.results[(self.page_number - 1) * 10:(self.page_number * 10)]):
            r = str(i + ((self.page_number - 1) * 10) + 1) + "." + "\t" + pub + "\t" + "%s\n\n" % (str(score))
            self.textw.insert(END, r)
            self._match_highlight(self.search_entry.get(), "blue")
            self._match_highlight(str(score), "red")

    def _match_highlight(self, word_list, tag):
        words = [word.encode("utf-8").lower() for word in word_list.split()]
        upper_words = [word.encode("utf-8").upper() for word in word_list.split()]
        title_words = [word.encode("utf-8").title() for word in word_list.split()]
        self._highlight(words, tag)
        self._highlight(upper_words, tag)
        self._highlight(title_words, tag)

    def _highlight(self, case, tag):
        for word in case:
            start = 1.0
            search_pos = self.textw.search(word, start, stopindex=END)
            while search_pos:
                length = len(word)
                row, col = search_pos.split('.')
                end = int(col) + length
                end = row + '.' + str(end)
                self.textw.tag_add(tag, search_pos, end)
                start = end
                search_pos = self.textw.search(word, start, stopindex=END)

    def _next_page(self):
        self.pre_button.config(state=NORMAL)
        self.textw.delete(1.0, END)
        self.page_number += 1
        self.page_number_label.config(text=str(self.page_number))
        if self.page_number == (len(self.results) / 10) + 1:
            self.next_button.config(state=DISABLED)
        self._print_results()

    def _previous_page(self):
        self.next_button.config(state=NORMAL)
        self.textw.delete(1.0, END)
        self.page_number -= 1
        self.page_number_label.config(text=str(self.page_number))
        if self.page_number < 2:
            self.pre_button.config(state=DISABLED)
        self._print_results()

    def citation_score(self, results):
        cite_count = dict([(pub, self.citation_count[pub]) for pub in results if pub in self.citation_count])
        return self.normalize_scores(cite_count)

    def get_scored_list(self, results, words):
        totalscores = dict([(pub, 0) for pub in results])
        if self.check_var_cite.get() == 1 and self.check_var_word.get() == 0:
            weights = [(float(self.cite_count_entry.get()), self.citation_score(results))]
        elif self.check_var_word.get() == 1 and self.check_var_cite.get() == 0:
            weights = [(float(self.word_freq_entry.get()), self.frequency_score(results))]
        else:
            weights = [(float(self.word_freq_entry.get()), self.frequency_score(results)),
                       (float(self.cite_count_entry.get()), self.citation_score(results))]
        for (weight, scores) in weights:
            for pub in totalscores:
                totalscores[pub] += weight * scores.get(pub, 0)

        return totalscores

    def frequency_score(self, results):
        counts = {}
        for pub in results:
            score = 1
            for wordlocations in results[pub]:
                score *= len(wordlocations)
            counts[pub] = score
        return self.normalize_scores(counts, smallIsBetter=False)

    @staticmethod
    def normalize_scores(scores, smallIsBetter=0):
        vsmall = 0.00001  # Avoid division by zero errors
        if smallIsBetter:
            minscore = min(scores.values())
            minscore = max(minscore, vsmall)
            return dict([(u, float(minscore) / max(vsmall, l)) for (u, l) \
                         in scores.items()])
        else:
            maxscore = max(scores.values())
            if maxscore == 0:
                maxscore = vsmall
            return dict([(u, float(c) / maxscore) for (u, c) in scores.items()])

    # Create the database tables
    def create_index_tables(self):
        """
        This method initialize shelve database files
        :return:
        """
        # {word:{publication: [loc1, loc2, ..., locN]}}
        self.word_location = shelve.open(self.db_tables['wordlocations'], writeback=True, flag='c')
        # {publication: citationcount}
        self.citation_count = shelve.open(self.db_tables['citationcounts'], writeback=True, flag='c')
        # {publication: type}
        self.publication_type = shelve.open(self.db_tables['types'], writeback=True, flag='c')


if __name__ == '__main__':
    root = Tk()  # Root frame of Tkinter
    root.resizable(width=FALSE, height=FALSE)  # Prevent all resize actions
    root.title('Sehir Scholar')  # Set GUI Title
    root.geometry('{}x{}+250+0'.format('900', '700'))  # Set GUI geometry
    tables = {"wordlocations": "wordlocations.db", "citationcounts": "citationcounts.db", "types": "types.db"}
    app = SehirScholar(root, tables)  # Starting our app and passing tables to our app.
    root.mainloop()  # Show GUI to user
