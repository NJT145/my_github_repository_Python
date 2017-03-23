
def openFile(filename):
    dictionary = dict()
    with open(filename) as openfile:
        for line in openfile:
            line = line.split()
            #escape the newline command
            # line[-1] = line[-1].strip()
            # line[-1]=line[-1].strip("\r\n")
            dictionary.setdefault(line[0], {})
            sliced_line = line[3:]
            for i in range(0, (len(sliced_line) - 1), 2):
                dictionary[line[0]][sliced_line[i]] = sliced_line[i + 1]
    return dictionary


print openFile("delicious.tiny.txt")

def createDataset(filename):
    datadictionary = openFile(filename)
    out_file = file("bookmarkdataset_test.txt", "w")
    out_file.write("Urls")
    wordlist = []

    # create list of tags
    for values in datadictionary.values():
        for key in values:
            if key not in wordlist:
                wordlist.append(key)

    # # write tags in wordlist to file
    for word in wordlist:
        out_file.write('\t%s' % word)
    out_file.write('\n')
    #
    # # convert dictionary to tuple. The tuple is like that = [(url,{tag:value}]
    for key, values in datadictionary.items():
        out_file.write(key)
        out_file.write('\t')
    #
        for word in wordlist:
            # if word not in values,it equalize it value to 0 and write to file
            if word not in values:
                out_file.write('0\t')
            else:
                out_file.write(values[word])
                out_file.write('\t')
        out_file.write('\n')

createDataset("delicious.tiny.txt")