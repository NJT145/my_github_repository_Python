#-*- coding: utf-8 -*-

a = open("ABONE_SAYISI.txt")
g = open("GAZ_KULLANICI_SAYISI.txt")
p = open("PERSONELE_DUSEN_ABONE_SAYISI.txt")

aL = []
for i1 in a:
    aL.append(i1.strip())

gL = []
for i2 in g:
    gL.append(i2.strip())

pL = []
for i3 in p:
    pL.append(i3.strip())

size_aL = len(aL)

results_aL = {}
last_key = None
for i in range(size_aL):
    if i%2==0:
        results_aL[aL[i]] = None
        last_key = aL[i]
    elif i%2==1:
        results_aL[last_key] = "".join(aL[i].split("."))
keys = results_aL.keys()
keys.sort()
for key in keys:
    print key, results_aL[key]

    #result.append(aL[i])
    #result.append(gL[i])
    #result.append(pL[i])
    #print result