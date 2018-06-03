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

def checksumPack(hashKey, packNoTotal, maxPackID, lastPackSize):
    maxLen = len(str(maxPackID))
    idLen = len(str(packNoTotal))
    packNoTotalstr = "packNoTotal=" + ("0" * (maxLen - idLen)) + str(packNoTotal) + "/"
    return (packNoTotalstr + "hashFile=" + hashKey + "/lastPackSize=" + str(lastPackSize))

def getChecksumPack(mssg):
    packInfo = {}
    packInfo["packNoTotal"] = mssg.split("/hashFile=")[0][12:]
    packInfo["hashKey"] = mssg.split("/hashFile=")[1].split("/lastPackSize=")[0]
    packInfo["lastPackSize"] = mssg.split("/hashFile=")[1].split("/lastPackSize=")[1]
    return packInfo

def sendPackageMssg(packIDstr, packContent):
    return (bytes(packIDstr, 'utf-8') + bytes("packContent=", 'utf-8') + packContent)

def getPackageMssg(mssg):
    packID = int(mssg.split("/packContent=")[0][7:])
    packContent = bytes((mssg.split("/packContent=")[1]), 'utf-8')
    return (packID, packContent)

def isPackageMssg(mssg):
    return mssg.startswith("packID=")

def isChecksumMssg(mssg):
    return mssg.startswith("packNoTotal=")

def fileSendRequest(fileName, hashKey):
    return ("fileNameToSend="+fileName+"/hashKey="+hashKey) #TODO: support for long fileName

def fileGetRequest(fileName, hashKey):
    return ("fileNameToGet="+fileName+"/hashKey="+hashKey) #TODO: support for long fileName

def isFileSendRequest(mssg):
    return mssg.startswith("fileNameToSend=")

def isFileGetRequest(mssg):
    return mssg.startswith("fileNameToGet=")

def errorMessage():
    return "Abort///"

def isErrorMssg(mssg):
    return mssg.startswith("Abort//")

def fileNameGenerateFromAnother(filename, num):
    extension = filename.split(".")[-1]
    fileNameWithoutExtension = ".".join(filename.split(".")[0:-1])
    return (fileNameWithoutExtension+"("+str(num)+")"+extension)

def writeFile(path, contentBytes):
    file = open(path, 'wb')  # write file as bytes
    file.write(contentBytes)
    file.close()

