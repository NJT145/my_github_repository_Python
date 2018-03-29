fin = open('words.txt')
#print fin
#print fin.readline()
##word=fin.readline()
##print word.strip()
"""
for line in fin:
    word=line.strip()
    print word
"""
###Q1
def f(text):
    for line in text:
        word=line.strip()
        if len(word)>20:
            print word
#f(fin)

###Q2
def has_no_e(text):
    for i in text:
        if i=="e":
            return False
    return True
#print has_no_e("abcdefg")
#print has_no_e("abcdfg")

###Q3
def avoid(word,letters):
    for i in letters:
        if i in word:
            return False
    return True
#print avoid("abcdef","eb")
#print avoid("abcdef","gh")

###Q4
def use_only(word,available):
    for i in word:
        if i not in available:
            return False
    for i in available:
        if i not in word:
            return False
    return True
#print use_only("banana","ban")
#print use_only("banana","ed")

###Q5
def use_all(word,letters):
    for i in letters:
        if i not in word:
            return False
    return True
#print use_all("banana","ban")

###Q6
def abecedarian(word):
    for i in range(len(word)-1):
        if word[i]>word[i+1]:
            return False
    return True
#print abecedarian("abcdee")
#print abecedarian("abcdeed")

###Q7

def abecedarian1(word):
    for i in range(len(word)-1):
        if word[i]>word[i+1]:
            return False
    return True
#print abecedarian1("abcdee")
#print abecedarian1("abcdeed")

def abecedarian2(word):
    i=0
    while i<len(word)-1:
        if word[i]>word[i+1]:
            return False
        i+=1
    return True
#print abecedarian2("abcdee")
#print abecedarian2("abcdeed")

#### ?????? abecedarian by recursion ?????? ####

##Q8

def palindrome(sequence):
    word=str(sequence)
    i=0
    j=(len(word)-1)-i
    while i<j:
        if word[i] != word[j]:
            return False
        i+=1
        j-=1
    return True
#print palindrome("aka")
#print palindrome("abc")
#print palindrome(121)
#print palindrome(123)
