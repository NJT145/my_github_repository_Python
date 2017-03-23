#-*- coding: utf-8 -*-
from anydbm import *
import sys
a=open("db1.db","c")
u=str(u'UNI 111')
a["aaa"]=u
c=u'\u0130\u015e'
d=c.encode("utf-8")
a["bbb"]=d
print a
bb= a["bbb"].decode('utf-8').encode(sys.stdout.encoding)
print bb
a.close()
