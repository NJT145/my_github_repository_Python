from tkinter import *
import hashlib

def messageFilter(messageText):
    EndFiltered = ''
    for i in range(len(messageText)-1,-1,-1):
        if messageText[i]!='\n':
            EndFiltered = messageText[0:i+1]
            break
    for i in range(0,len(EndFiltered), 1):
            if EndFiltered[i] != "\n":
                    return EndFiltered[i:]+'\n'
    return ''

def displayLocalMessage(chatBox, messageText):
    if messageText != '':
        chatBox.config(state=NORMAL)
        if chatBox.index('end') != None:
            LineNumber = float(chatBox.index('end'))-1.0
            chatBox.insert(END, "YOU: " + messageText)
            chatBox.tag_add("YOU", LineNumber, LineNumber+0.4)
            chatBox.config(state=DISABLED)
            chatBox.yview(END)

def displayRemoteMessage(chatBox, messageText):
    if messageText != '':
        chatBox.config(state=NORMAL)
        if chatBox.index('end') != None:
            try:
                LineNumber = float(chatBox.index('end'))-1.0
            except:
                pass
            chatBox.insert(END, "PARTNER: " + messageText)
            chatBox.tag_add("PARTNER", LineNumber, LineNumber+0.6)
            chatBox.config(state=DISABLED)
            chatBox.yview(END)

def getConnectionInfo(chatBox, messageText):
    if messageText != '':
        chatBox.config(state=NORMAL)
        if chatBox.index('end') != None:
            chatBox.insert(END, messageText+'\n')
            chatBox.config(state=DISABLED)
            chatBox.yview(END)

def getEmojis():
    emojilist = {0:u"\uD83D\uDE01",1: u"\uD83D\uDE02", 2:"\uD83D\uDE04", 3:"\uD83D\uDE05",
                 4:"\uD83D\uDE06", 5:"\uD83D\uDE09",6:"\uD83D\uDE0B", 7:"\uD83D\uDE0D",
                 8:"\uD83D\uDE0F"}
    return emojilist

def getEmoji(ind):
    emojilist = getEmojis()
    return emojilist[ind]

def sendEmoji(mssg):
    emojilist = getEmojis()
    for a in range(len(emojilist)):
        new_str = "emo" + str(a) + "emo"
        if emojilist[a] in mssg:
            return str(mssg).replace(emojilist[a], new_str)
    return mssg

def receiveEmoji(mssg):
    emojilist = getEmojis()
    for a in range(len(emojilist)):
        new_str = "emo" + str(a) + "emo"
        if new_str in mssg:
            return str(mssg).replace(new_str,emojilist[a])
    return mssg

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
    packIDstr = "packID=" + ("0"*(maxLen - idLen)) + str(packID) + "/"
    return packIDstr

def md5Checksum(path):
    with open(path, 'rb') as file_to_check:
        # read contents of the file
        data = file_to_check.read()
        # pipe contents of the file through
        md5_returned = hashlib.md5(data).hexdigest()
    return md5_returned

def checksumPack(hashKey, packID, maxPackID):
    return ((packIndexStr(packID,maxPackID)) + "hash=" + hashKey)

def checksumPackSize(maxPackID):
    hashKey_length = 32  # fixed length for md5 checksum key
    str = (packIndexStr(0,maxPackID) + "hash=" + ("0"*hashKey_length))
    return (len(str), sys.getsizeof(bytes(str, 'utf-8'))) # str_length , byte_size

def checksumPack_file(hashKey, packNumTotal, maxPackID, lastPackSize):
    maxLen = len(str(maxPackID))
    idLen = len(str(packNumTotal))
    packNumTotalstr = "packNumTotal=" + ("0" * (maxLen - idLen)) + str(packNumTotal) + "/"
    return (packNumTotalstr + "hashFile=" + hashKey + "/lastPackSize=" + str(lastPackSize))

def fileSendRequest(fileName, hashKey):
    return ("fileNameToSend="+fileName+"/hashKey="+hashKey) #TODO: support for long fileName

def fileGetRequest(fileName, hashKey):
    return ("fileNameToGet="+fileName+"/hashKey="+hashKey) #TODO: support for long fileName

def isFileSendRequest(mssg):
    return mssg.startswith("fileNameToSend=")

def isFileGetRequest(mssg):
    return mssg.startswith("fileNameToGet=")

