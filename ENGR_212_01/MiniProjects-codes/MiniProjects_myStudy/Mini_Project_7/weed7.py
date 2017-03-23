import os
# get current directory as cwd
cwd = os.getcwd()
# check if a file or directory named 'assets' exists in our cwd
if os.path.exists('assets')==True:
    for name in os.listdir(cwd):
        if 'assets' == name:
            path = os.path.join(cwd, 'assets')
            # check if 'assets' is a file
            if os.path.isdir(path)==True:
                listItems = os.listdir(path)
                listItems.sort()
                print listItems
                for i in listItems:
                    print "self."+i

