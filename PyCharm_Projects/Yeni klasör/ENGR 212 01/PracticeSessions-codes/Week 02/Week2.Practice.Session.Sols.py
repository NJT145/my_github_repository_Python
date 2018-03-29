__author__ = 'acakmak'
import os

#Q1
def filter(oldfile, newfile):
     infile = open(oldfile, "r")
     outfile = open(newfile, "w")
     while True:
         text = infile.readline()
         if len(text) == 0:
            break
         if text[0] == "#":
            continue

         # Put any more processing logic here
         outfile.write(text)

     infile.close()
     outfile.close()


#Q2
f = open("image.png", "rb")
g = open("image.copy.png", "wb")

while True:
    buf = f.read(1024)
    if len(buf) == 0:
         break
    g.write(buf)

f.close()
g.close()

#Q3
import os

def walk(dirname, suffix):
    """Finds the names of all files in dirname and its subdirectories.

    dirname: string name of directory
    """
    names = []
    for name in os.listdir(dirname):
        path = os.path.join(dirname, name)

        if os.path.isfile(path):
            if name.endswith(suffix):
                names.append(path)
        else:
            names.extend(walk(path))
    return names

#Q4
import anydbm
import pickle

db = anydbm.open("frequency_letters.db", "c")


def get_frequency():
    temporary_db = dict()
    words = open("words.txt", "r")
    for word in words:
        for letter in word:
            if letter in temporary_db:
                temporary_db[letter] += 1
            else:
                temporary_db[letter] = 1
    return temporary_db


def store_to_db(letter_frequency):
    for letter in letter_frequency:
        frequency = letter_frequency[letter]
        frequency = pickle.dumps(frequency)
        if frequency in db:
            pickled_list_of_letters = db[frequency]
            list_of_letters = pickle.loads(pickled_list_of_letters)
            list_of_letters.append(letter)
            pickled_list_of_letters = pickle.dumps(list_of_letters)
            db[frequency] = pickled_list_of_letters
        else:
            pickled_list_of_letter = pickle.dumps([letter])
            db[frequency] = pickled_list_of_letter


def display_data():
    for pickled_frequency in db:
        frequency = pickle.loads(pickled_frequency)
        list_of_letters = pickle.loads(db[pickled_frequency])
        print frequency, list_of_letters


letter_frequency = get_frequency()
store_to_db(letter_frequency)
display_data()

#Q5

def sumAll(filename):
    sumInteger=0
    if not os.path.isfile(filename): # check whether given file exist or not
        return "No such file !!"
    else:
        with open(filename,"r") as file: # open file
            for integer in file:  # get the integer at each line
                sumInteger+=int(integer) # convert the "integer" variable to integer and add to sumInteger
        file.close()
    return sumInteger

# Q6
def reverseContext(filename1,filename2):
    if not os.path.isfile(filename1): # check whether given file exist or not
        return "No such file !!"
    else:
        with open(filename1,"r") as file: # open file
            text=file.readlines()
            file.close()

    text[-1] = text[-1]+"\n"
    text.reverse()
    with open(filename2,"w") as file:
        for line in text:
            file.write(line)
    file.close()


print reverseContext("abc.txt","a.txt")

#Q7
def Q7(filename1,filename2):
    counter = 1
    with open(filename1,"r") as file: # open file
        with open(filename2,"w") as file2:
            for line in file:
                num="%.4d"%counter
                file2.write(num +" " +line)
                counter += 1
        file2.close()
    file.close()

Q7("abc.txt", "abc.numbered.txt")

#Q8
def Q8(filename1,filename2):
    with open(filename1,"r") as file:
        with open(filename2,"w") as file2:
            for line in file:
                words = line.split(" ")
                file2.write(' '.join(words[1:]))
        file2.close()
    file.close()

Q8("abc.numbered.txt", "abc.copy.txt")