import docclass
cl= docclass.classifier(docclass.getwords)
print cl.weightedprob("online","good",cl.fprob)
docclass.sampletrain(cl)
print cl.weightedprob("online","good",cl.fprob)
docclass.sampletrain(cl)
print cl.weightedprob("online","good",cl.fprob)