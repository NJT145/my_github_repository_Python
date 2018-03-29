__author__ = 'doktoray'

import re

#step 1
pat = "((\+|-)?\d+\.?\d+(\$|%)?)"
print re.findall(pat, "benim +1945.4 20% 2.3$ -2.3 1022")

#step 2
pat2 = "((\"|')\w+(\"|'))"
print re.findall(pat2, "asdasd \"qqq\" asdasdddd 23.3 'asdas'")

#step 3
#words=re.findall(r'\w+', "my name is something 44 ...")
#paragraphs = re.split('\n+\t?', "\tmy name is emrullah.\n\tand my dad ...")
words=re.findall(r'\w+', open("words_").read())
paragraphs = re.split('\n+\t?', open("words_").read())
print len(words), words
print len(paragraphs), paragraphs

#step 4
pat4 = "([A-Z][a-z]*\s)+[A-Z][a-z]*"
new_sentence = re.sub(pat4, "Emrullah Delibas", "Alan Spoon is of the TA of this class.")
print new_sentence

#step 5
#(a) [a-zA-Z]+
#(b) [A-Z][a-z]+
#(c) \w+|[^\w\s]

pat5_a = "[a-zA-Z]+"
print re.findall(pat5_a, "benim +1945.4 20% 2.3$ -2.3 1022 ASDasd ASDAS asd")

pat5_b = "[A-Z][a-z]+"
print re.findall(pat5_b, "benim +1945.4 20% 2.3$ -2.3 1022 ASDasd ASDAS asd What is")

pat5_c = "\w+|[^\w\s]"
print re.findall(pat5_c, "benim +1945.4 20% 2.3$ -2.3 1022 ASDasd ASDAS asd What is ||")

#step 6
pat6 = "[0-9]{2}/[0-9]{2}/[0-9]{4}\s\d{1,2}:\d{2}"
print re.match(pat6, "17/05/2009 8:15").group()

#step 7
pat7 = "([0-9]{2})/([0-9]{2})/([0-9]{4})\s(\d{1,2}):(\d{2})"
pat7 = re.compile(pat7)
print pat7.match("17/05/2009 8:15").groups()

hours = pat7.match("17/05/2009 8:15").group(4)
minutes = pat7.match("17/05/2009 8:15").group(5)
print ( ( (int(hours) * 60) + int(minutes) ) * 60 )

#step 8
pat8 = "[-+]?[0-9]*\.?e?[-+]?[0-9]+"
print re.findall(pat8, "45, 3453 : 19, -1.e-10")

#step 9
def leadingToTrailingUnderscore(script):
    pat9 = "^_(\w+)"
    words = script.split(" ")
    script_final = script
    for word in words:
        try:
            match = re.match(pat9, word).group(1)
            word_new = match + "_"
            script_final = re.sub(word,word_new, script_final)
        except AttributeError:
            pass
    return script_final

print leadingToTrailingUnderscore("_asdAS qqq 132 asdQWE _asdwqe _ASD awqe_qeqwWQE rrt_ .. !!!")














