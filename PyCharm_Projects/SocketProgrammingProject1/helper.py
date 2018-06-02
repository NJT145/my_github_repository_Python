from tkinter import *


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


