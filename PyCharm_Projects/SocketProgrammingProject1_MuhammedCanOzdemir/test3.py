import hashlib
import sys

def fileBit_sliceAndDice(path, packSize):
    file = open(path, 'rb')  # read file as bytes
    parts = []
    while True:
        part = file.read(packSize)  # read file next packSize bytes each time
        if part != bytes('', 'utf-8'):  # if data is not empty
            parts.append(part)
        else:  # when file data is empty break the loop
            break
    file.close()
    return parts
def packIndexStr(packID, maxPackID):
    maxLen = len(str(maxPackID))
    idLen = len(str(packID))
    packIDstr = "packID#" + ("0"*(maxLen - idLen)) + str(packID) + "#"
    return packIDstr


path = r"C:\Users\nejat\Desktop\test.PNG"
path2 = r"C:\Users\nejat\Desktop\test2.PNG"
file = open(path, 'rb')  # read file as bytes

packSize = 1000
maxPackID = 10**10

parts = fileBit_sliceAndDice(path, packSize)

file.close()


file2 = open(path2, 'wb')
for part in parts:
    file2.write(part)
file2.close()

print(parts)
print(sys.getsizeof(bytes(str(maxPackID), 'utf-8')))
print((str(maxPackID)))
print((packIndexStr(1,maxPackID)))


def md5Checksum(path):
    with open(path, 'rb') as file_to_check:
        # read contents of the file
        data = file_to_check.read()
        # pipe contents of the file through
        md5_returned = hashlib.md5(data).hexdigest()
    return md5_returned

print(len(md5Checksum(path)))
print(sys.getsizeof(bytes(md5Checksum(path), 'utf-8')))
#print(sys.getsizeof(bytes("packID#", 'utf-8')))
#print(sys.getsizeof(bytes("hash#", 'utf-8')))
#print(sys.getsizeof(bytes(((packIndexStr(1,maxPackID))), 'utf-8')))
#print(sys.getsizeof(bytes((packIndexStr(1,maxPackID)), 'utf-8')))
def checksumPack(hashKey, packID, maxPackID):
    return ((packIndexStr(packID,maxPackID)) + "hash#" + hashKey)

def checksumPackSize(maxPackID):
    hashKey_length = 32  # fixed length for md5 checksum key
    str = (packIndexStr(0,maxPackID) + "hash#" + ("0"*hashKey_length))
    return (len(str), sys.getsizeof(bytes(str, 'utf-8'))) # str_length , byte_size

def checksumPack_file(hashKey, packNumTotal, maxPackID, lastPackSize):
    maxLen = len(str(maxPackID))
    idLen = len(str(packNumTotal))
    packNumTotalstr = "packNumTotal#" + ("0" * (maxLen - idLen)) + str(packNumTotal) + "#"
    return (packNumTotalstr + "hashFile#" + hashKey + "#lastPackSize#" + str(lastPackSize))

test1 = checksumPack_file(md5Checksum(path), maxPackID, maxPackID, 1004)
print(len(test1))
print(sys.getsizeof(bytes(test1, 'utf-8')))