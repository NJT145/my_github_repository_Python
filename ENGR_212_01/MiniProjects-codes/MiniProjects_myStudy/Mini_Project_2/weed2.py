#-*- coding: utf-8 -*-

from anydbm import *

ratings=open("cc_ratings.db")
for i in ratings:
    print i
    for z in ratings[i]:
        print z
        print ratings[i]

##############################################################################################
print "\n"

str1 = str('Ac\xc4\xb1l\xc4\xb1 Tavuk --> 0')
str2 = str('Ac\xc4\xb1l\xc4\xb1 Tavuk')

if str1.find(str2)!=-1:
    print "str1!=str2"
else:
    print "str1==str2"