import docclass
import random
class Tweet:
    #open the file and match corresponding lines
        def read(self,txt1,txt2):
                list_=[]
                list1=[]
                list2=[]
                openedfile1=open("Data Set for Practice12//Tweet Ground Truth//"+txt1)
                openedfile2=open("Data Set for Practice12//Tweet Text for each Company//"+txt2)
                for line in openedfile2:
                    list1.append(line.strip())
                for line1 in openedfile1:
                        list2.append(line1.strip())

                for i in range(len(list1)):
                    a=tuple((list1[i],list2[i]))
                    list_.append(a)
                return list_
        #takes %90 random sample
        def randomsample(self,txt1,txt2):
                result = self.read(txt1,txt2)
                newresult=random.sample(result,90)
                for i in newresult:
                        result.remove(i)
                return newresult,result
        #train the sample
        def training(self, cl, txt1,txt2):
                category=self.randomsample(txt1,txt2)[0]
                for i,j in category:
                        cl.train(i,j)
        #test the 10 tweeets
        def test(self, cl,txt1,txt2):
            category=self.randomsample(txt1,txt2)[1]
            result=[]
            for i,j in category:
                cat=cl.classify(i)
                result.append(cat)
            return result
        def listelen(self, list_):
            k=0
            for item in list_:
                    if item != None:
                            k+=1
            return k
        #accuracy of each company
        def accuracy(self,cl, txt1,txt2):
            list1=self.test(cl,txt1,txt2)
            list2=self.randomsample(txt1,txt2)[1]
            list3=[]
            k=0
            for i,j in list2:
                list3.append(j)
            for i in range(len(list3)):
                if list1[i]==list3[i]:
                    k=k+1
            accuracy=float(k)/self.listelen(list1)
            return accuracy*100
        #averageaccuracy in ten times run
        def tentimes(self,cl,txt1,txt2):
            list_=[]
            for i in range(10):
                accurate=self.accuracy(cl,txt1,txt2)
                list_.append(accurate)
            averageaccuracy=sum(list_)/len(list_)
            return averageaccuracy
        #train all companies
        def trainall(self,classifier):
            companies=["Best Buy.txt","Warner Bross.txt","Sprint.txt","Delta Airlines.txt","Dunkin Donat.txt","Ford.txt","Gap.txt","Overstock.txt","Rim.txt","Southwest Airlines.txt"]
            for i in companies:
                self.training(classifier,i,i)
        #dump to file
        def dumptofile(self,cl):
            companies=["Best Buy.txt","Warner Bross.txt","Sprint.txt","Delta Airlines.txt","Dunkin Donat.txt","Ford.txt","Gap.txt","Overstock.txt","Rim.txt","Southwest Airlines.txt"]
            filename=open("classification_results.txt","w")
            filename.write("Company" + "        " + "Naive Bayes Accuracy\n")
            print "Company" + "        " + "Naive Bayes Accuracy"
            print "-------" + "        " + "-------------------" 
            filename.write("-------" + "           " + "-------------------\n")
            list1=[]
            list2=[]
            for i in companies:
                average=self.tentimes(cl,i,i)
                list1.append(average)
                
                filename.write(i + "           " + str(average) + " %" "        \n")
                print i + "           "  + str(average) + "%" 
            Average=sum(list1)/len(list1)
         
            print "Average        " + str(Average) +" %"
            filename.write("Average        " + str(Average)+ " %")
