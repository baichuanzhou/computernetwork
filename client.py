from socket import *
import time
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import threading
import json
import util

"""
IP = ''
PORT = ''
username = ''
friends = {}
currentContact = ''
"""


class LoginWindow:
    """A window that is used when logging in"""

    def __init__(self):
        self.rootLogin = Tk()
        self.rootLogin.title("用户登录窗口")
        self.rootLogin.geometry("300x150")
        self.rootLogin.resizable(False, False)

        self.PORT = StringVar()
        self.USERNAME = StringVar()
        self.IP = StringVar()

        IPLabel = ttk.Label(self.rootLogin, text="目的IP:")
        IPLabel.place(x=20, y=5, width=100, height=40)
        IPEntry = ttk.Entry(self.rootLogin, textvariable=self.IP)
        IPEntry.place(x=100, y=10, width=100, height=30)

        PORTLabel = ttk.Label(self.rootLogin, text="目的端口:")
        PORTLabel.place(x=20, y=40, width=100, height=40)
        PORTEntry = ttk.Entry(self.rootLogin, textvariable=self.PORT)
        PORTEntry.place(x=100, y=45, width=100, height=30)

        USERLabel = ttk.Label(self.rootLogin, text="用户名:")
        USERLabel.place(x=20, y=75, width=100, heigh=40)
        USEREntry = ttk.Entry(self.rootLogin, textvariable=self.USERNAME)
        USEREntry.place(x=100, y=80, width=100, height=30)

        loginButton = ttk.Button(self.rootLogin, text="登录", command=self.Login)
        loginButton.place(x=135, y=120, width=40, height=20)
        self.rootLogin.bind("<Return>", self.Login)

    def Login(self, *args):
        self.IP = self.IP.get()
        self.PORT = self.PORT.get()
        self.USERNAME = self.USERNAME.get()
        self.rootLogin.destroy()


class UserWindow:
    def __init__(self, root):
        self.rootMain = Tk()
        self.rootMain.geometry("640x800")
        self.rootMain.resizable(False, False)
        self.rootMain.title("消息界面")

        self.contacts = []

        self.root = root
        self.IP = self.root.IP
        self.PORT = self.root.PORT
        self.USERNAME = self.root.USERNAME

        self.s = socket(AF_INET, SOCK_DGRAM)

        self.messageList = Listbox(self.rootMain)
        self.messageList.place(x=5, y=0, width=485, height=320)
        if self.USERNAME != "":
            self.messageList.insert(END, "欢迎用户" + self.USERNAME + "进入聊天室!")
            self.messageList.insert(END, '\n')

        messageScroll = ttk.Scrollbar(self.messageList, orient=VERTICAL, command=self.messageList.yview)
        messageScroll.place(x=460, y=0, width=20, height=320)
        self.messageList.configure(yscrollcommand=messageScroll.set)

        self.contactList = Listbox(self.rootMain)
        self.contactList.place(x=490, y=0, width=140, height=320)

        contactScroll = ttk.Scrollbar(self.contactList, orient=VERTICAL, command=self.contactList.yview)
        contactScroll.place(x=520, y=0, width=20, height=320)
        self.contactList.configure(yscrollcommand=contactScroll.set)

        self.message = StringVar()
        self.messageEntry = Entry(self.rootMain, width=120, textvariable=self.message)
        self.messageEntry.place(x=5, y=330, width=485, height=50)

        sendButton = Button(self.rootMain, text="发送", command=self.sendMessage)  # 需要定义函数
        sendButton.place(x=500, y=345, width=30, height=20)

    def addFriend(self, friend):
        self.contacts.append(friend)
        friendButton = Button(self.contactList, text=friend.friendName, command=friend.rootFriend.mainloop())  # 需要定义函数
        friendButton.pack()
        self.contactList.insert(END, friend.friendName)

    def sendMessage(self):
        ip_port = (self.IP, int(self.PORT))
        messageEncode = self.message.get().encode()
        self.s.sendto(messageEncode, ip_port)
        self.messageList.insert(END, self.USERNAME + ": " + self.message.get())
        self.message.set("")
        return "break"

    def receiveMessage(self):
        while True:
            data = self.s.recv(1024)
            dataDecode = data.decode()
            self.messageList.insert(END, dataDecode)


"""
class FriendWindow:
    def __init__(self, friendName, User):
        self.rootFriend = Tk()
        self.friendName = friendName
        self.rootFriend.title("self.friendName")
        self.rootFriend.geometry("300x150")
        self.rootFriend.resizable(False, False)
        self.rootFriend.configure(background="LightBlue")

        self.message = StringVar()

        self.sendToIP = User.IP
        self.sendToPort = User.Port

        self.messageEntry = Entry(self.rootFriend, textvariable=self.message, background="White")
        self.messageEntry.place(x=20, y=40, width=100, height=30)

        self.sendButton = Button(self.rootFriend, text="发送", background="White", command=self.sendMessage)
        self.sendButton.place(x=125, y=50, width=20, height=10)
"""

Login = LoginWindow()
Login.rootLogin.mainloop()

User = UserWindow(Login)
User.rootMain.mainloop()

# UDP部分
"""
ip_port = (IP, int(PORT))
s = socket(AF_INET, SOCK_DGRAM)


if username:
    s.sendto(username.encode(), ip_port)  # 发送用户名
else:
    username = IP + ':' + PORT
    s.sendto(username.encode(), ip_port)
"""
