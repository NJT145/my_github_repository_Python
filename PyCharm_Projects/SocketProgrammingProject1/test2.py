import os
import sys

path = r"C:\Users\nejat\Desktop\test.PNG"
path2 = r"C:\Users\nejat\Desktop\test2.PNG"
statinfo = os.stat(path)
sys_file_size = statinfo.st_size
file = open(path, 'rb')  # read file as bytes
read_file_size = sys.getsizeof(file)
print(read_file_size)
packID = 0
sizeList = []
size1 = 0
file2 = open(path2, 'wb')
while True:
    part = file.read(1024)  # read file next 1000 bytes each time

    if part != bytes('', 'utf-8'):  # if data is not empty
        file2.write(part)
        read_file_size2 = sys.getsizeof(part)
        size1 += read_file_size2
        print(read_file_size2)
    else:  # when file data is empty break the loop
        break

file.close()
file2.close()
print(size1)