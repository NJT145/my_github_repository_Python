import sys

a = u'GENEL M\xdcD\xdcRL\xdcK'
print a.encode('utf-8').decode(sys.stdout.encoding)
