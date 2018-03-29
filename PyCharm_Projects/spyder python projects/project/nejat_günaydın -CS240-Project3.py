# -*- coding: utf-8 -*-

"""
this script designed by using python2.7 .
i used Anaconda interpreter by Continuum Analytics.

thinkstats2 module -download ThinkStats2-master.zip from "https://github.com/AllenDowney/ThinkStats2", unpack ThinkStats2-master file in it, open Anaconda commend prompt with administrator privilege and, for path = -path of ThinkStats2-master/code/- , write "cd path" then "python setup.py install" to the prompt.

csv module -dowload csv-1.0.tar.gz from "http://www.object-craft.com.au/projects/csv/download.html" - open Anaconda commend prompt with administrator privilege and, for path = -path of the directory that you downloaded "csv-1.0.tar.gz"- , write "cd path" then ""pip install csv-1.0.tar.gz"" to the prompt.
            -info in-http://www.object-craft.com.au/projects/csv/ 
                     https://docs.python.org/2/library/csv.html

"""
import thinkstats2
import thinkplot
import csv
import random
import numpy as np

def readData(filename):
    doc=open(filename,"rb")
    csv_doc = csv.reader(doc)
    list_rows=[]
    for row in csv_doc:
        list_rows.append(row)

    dict_tupleList={} 
    listKeys=list_rows[0]
    listValuesList=list_rows[1:]
    for num1 in range(len(listKeys)):
        key=listKeys[num1]
        dict_tupleList.setdefault(key, [])
        for num2 in range(len(listValuesList)):
            try:
                dict_tupleList[key].append(float(listValuesList[num2][num1]))
            except:
                dict_tupleList[key].append((listValuesList[num2][num1]))
    return tuple(dict_tupleList.values())
        
print ">>> print readData(“data.csv”)"
print readData("data.csv")

raw_input("Press a button to continue...")

print "\nPart 1"

(Gender, age, time_spend_on_social_media, GPA) = readData("data.csv")

class PART1_HypothesisTest1(thinkstats2.HypothesisTest): 
        
    def TestStatistic(self, data):
        xs, ys = data
        test_stat = abs(thinkstats2.Corr(xs, ys)) 
        return test_stat
        
    def RunModel(self):
        xs, ys = self.data 
        xs = np.random.permutation(xs)
        return xs, ys
    
print "\n-(1)-"

ht1 = PART1_HypothesisTest1((time_spend_on_social_media, GPA))

mean1x=thinkstats2.Mean(time_spend_on_social_media)
mean1y=thinkstats2.Mean(GPA)
print "Time spend mean:",mean1x,"\nGPA mean:",mean1y

actualCorrelation = (thinkstats2.Corr(time_spend_on_social_media, GPA))

print "The actual correlation is",actualCorrelation
print "Computed p-value is", ht1.PValue()

raw_input("Press a button to continue...")

print "\n-(2)-"

ht2 = PART1_HypothesisTest1((time_spend_on_social_media, age))

mean2x=thinkstats2.Mean(time_spend_on_social_media)
mean2y=thinkstats2.Mean(age)
print "Time spend mean:",mean2x,"\nAge mean:",mean2y

actualCorrelation = (thinkstats2.Corr(time_spend_on_social_media, age))

print "The actual correlation is",actualCorrelation
print "Computed p-value is", ht2.PValue()

raw_input("Press a button to continue...")

print "\n-(3)-"

def groupDivider(group11, group22):
    """
    This function will divide group22 according to matching group11 values.
    This function will return a list of tuples whose first item from group11 
    and second is list of values matching from group22.
    """
    if len(group11)!=len(group22):
        raise ValueError
    classes=[]
    resultDict={}
    for i in group11:
        if i not in classes:
            classes.append(i)
    for i in range(len(group11)):
        for n in range(len(classes)):
            resultDict.setdefault(classes[n], [])
            if group11[i]==classes[n]:
                resultDict[classes[n]].append(group22[i])           
    return resultDict.items()
#print groupDivider(Gender, time_spend_on_social_media)

class PART1_HypothesisTest2(thinkstats2.HypothesisTest):
    
    def TestStatistic(self, data):
        group1, group2 = data
        test_stat = abs(group1.mean() - group2.mean()) 
        return test_stat
    
    def MakeModel(self):
        group1, group2 = self.data
        self.n, self.m = len(group1), len(group2) 
        self.pool = np.hstack((group1, group2))
    
    def RunModel(self):
        np.random.shuffle(self.pool) 
        data = self.pool[:self.n], self.pool[self.n:]
        return data

M_timeSpend_list=groupDivider(Gender, time_spend_on_social_media)[0][1]
F_timeSpend_list=groupDivider(Gender, time_spend_on_social_media)[1][1]

mean3M=thinkstats2.Mean(M_timeSpend_list)
mean3F=thinkstats2.Mean(F_timeSpend_list)
print "Time spend mean for male students:",mean3M
print "Time spend mean for female students:",mean3F
print "The actual difference between means is", abs(mean3M-mean3F)

min_len=min(len(M_timeSpend_list), len(F_timeSpend_list))

ht3 = PART1_HypothesisTest1((M_timeSpend_list[:min_len], F_timeSpend_list[:min_len]))

print "Computed p-value is", ht3.PValue(),"   (first",min_len,"items taken)"

raw_input("Press a button to continue...")

print "\nPart 2"

xs=time_spend_on_social_media
ys=GPA

print "\n*1) Plot the scatter plot of GPA and time spend in social media, find the inter and slope;"

inter, slope = thinkstats2.LeastSquares(xs, ys)
fit_xs, fit_ys = thinkstats2.FitLine(xs, inter, slope) 
thinkplot.Scatter(xs, ys, alpha=1.0)
thinkplot.Config(xlabel='time_spend_on_social_media', ylabel='GPA', legend=True)
thinkplot.Plot(fit_xs, fit_ys, label="Fitted line")
thinkplot.Save(root='Part2-1', formats=['jpg'], xlabel='GPA', ylabel='time_spend_on_social_media')
thinkplot.Show(xlabel='time_spend_on_social_media', ylabel='GPA')
print "intercept:", inter, "\nslope:",slope

raw_input("Press a button to continue...")

print "\n*2) Measure the residuals for the GPA versus time spend in social media and plot the residuals."

def Residuals(xs, ys, inter, slope):
    xs = np.asarray(xs)
    ys = np.asarray(ys)
    res = ys - (inter + slope * xs)
    return res


residuals=Residuals(xs, ys, inter, slope)

thinkplot.Scatter(ys, residuals, alpha=1.0)
thinkplot.Config(xlabel='GPA', ylabel='residuals')
inter2, slope2 = thinkstats2.LeastSquares(ys, residuals)
fit_xs2, fit_ys2 = thinkstats2.FitLine(ys, inter2, slope2)
thinkplot.Plot(fit_xs2, fit_ys2, label="fit line for residual GPA")
thinkplot.Save(root='Part2-2', formats=['jpg'], xlabel='GPA', ylabel='residuals')
thinkplot.Show(xlabel='GPA', ylabel='residuals (GPA)')

#raw_input("Press a button to continue...")

print "\n*3) Using the data from the data.csv, compute the linear least squares fit for log(GPA) versus age. ..."

logGPA=np.log10(GPA)
thinkplot.Scatter(age, logGPA, alpha=1.0)
thinkplot.Config(xlabel='age', ylabel='log10(GPA)')
inter3, slope3 = thinkstats2.LeastSquares(age, logGPA)
fit_xs3, fit_ys3 = thinkstats2.FitLine(age, inter3, slope3)
thinkplot.Plot(fit_xs3, fit_ys3, label="fit line for residual log10(GPA)")
thinkplot.Save(root='Part2-3', formats=['jpg'], xlabel='age', ylabel='log10(GPA)')
thinkplot.Show(xlabel='age', ylabel='log10(GPA)')

#raw_input("Press a button to continue...")

print "\n*4) Suppose you meet a student who is 21 years old, male and 300 minutes time spend in social media. Can you predict his GPA. (use Poisson regression) "















