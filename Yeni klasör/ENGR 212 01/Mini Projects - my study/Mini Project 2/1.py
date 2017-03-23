#-*- coding: utf-8 -*-

from anydbm import *

ratings=open("cc_ratings.db")
for i in ratings:
    print i
    for z in ratings[i]:
        print z
        print ratings[i]
