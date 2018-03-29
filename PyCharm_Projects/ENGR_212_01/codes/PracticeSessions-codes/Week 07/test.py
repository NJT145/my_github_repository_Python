__author__ = 'doktoray'

import re

#
# pat = "a*b"
#
# r = re.search(pat, "fooaaabcde")
#
# print r.group()
#
# print r.start()
#
# print r.end()
#
# print r.span()
# print
# pat1 = "\w+@(\w+\.)+(com|org|net|edu)"
# r1 = re.match(pat1,"finin@cs.umbc.edu")
# print r1.group()
# print
#
# pat2 = "(\w+)@((\w+\.)+(com|org|net|edu))"
# r2 = re.match(pat2,"finin@cs.umbc.edu")
# print r2.group(1)
# print r2.group(2)
# print r2.groups()

# pat3 ="(?P<name>\w+)@(?P<host>(\w+\.)+(com|org|net|edu))"
# r3 = re.match(pat3,"finin@cs.umbc.edu")
# print r3.group('name')
# print r3.group('host')
#
# print re.split("\W+", "This... is a test, short and sweet, of split().")
# print re.sub('(blue|white|red)', 'black', 'blue socks and red shoes')
# print re.findall("\d+","12 dogs,11 cats, 1 egg")
#
# cpat3 = re.compile(pat3)
# print cpat3
# r3 = cpat3.search("finin@cs.umbc.edu")
# print r3
# print r3.group()

# p1 = re.compile("\w+@\w+\.+com|org|net|edu")
# print p1.match("steve@apple.com").group(0)
# print p1.search("Email steve@apple.com today.").group()
# print p1.findall("Email steve@apple.com and bill@msft.com now.")

# p2 = re.compile("[.?!]+\s+")
# print p2.split("Tired? Go to bed!   Now!! ")

pat = "([bcdfghjklmnpqrstvwxyz]+)(\w+)"
cpat = re.compile(pat)

def piglatin(string):
    return " ".join([piglatin1(w) for w in string.split()])

def piglatin1(word):
    match = cpat.match(word)
    if match:
        consonants = match.group(1)
        rest = match.group(2)
        return rest + consonants + "ay"
    else:
        return word + "zay"

print piglatin("merhaba")











