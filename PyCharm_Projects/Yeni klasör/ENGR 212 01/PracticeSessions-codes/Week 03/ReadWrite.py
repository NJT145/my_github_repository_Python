__author__ = 'aliuzun'


class ReadWrite():

    def getText(self,filename,mode):
        text=''
        with open(filename,mode) as file:
            for line in file:
                text+=line.strip("\n")+" "
                # print line.strip("\n")
        return text

    def createFile(self,filename,mode,text):
        text=text.split(" ")
        with open(filename,mode) as file:
            for word in text:
                file.write(word+" ")
        file.close()



