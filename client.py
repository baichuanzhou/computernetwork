from socket import *
import time
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import threading
import json
import util

IP = ''
PORT = ''
username = ''
friends = {}
currentContact = ''


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
        self.rootLogin.mainloop()

    def Login(self, *args):
        global IP, PORT, username
        IP = self.IP.get()
        PORT = self.PORT.get()
        username = self.USERNAME.get()
        self.rootLogin.destroy()


class MainWindow:
    def __init__(self):
        self.rootMain = Tk()
        self.rootMain.geometry("640x800")
        self.rootMain.resizable(False, False)
        self.rootMain.title("消息界面")

        messageList = Listbox(self.rootMain)
        messageList.place(x=5, y=0, width=485, height=320)
        if username != "":
            messageList.insert(END, "欢迎用户" + username + "进入聊天室!")
            messageList.insert(END, '\n')

        messageScroll = ttk.Scrollbar(messageList, orient=VERTICAL, command=messageList.yview)
        messageScroll.place(x=460, y=0, width=20, height=320)
        messageList.configure(yscrollcommand=messageScroll.set)

        contactList = Listbox(self.rootMain)
        contactList.place(x=490, y=0, width=140, height=320)

        contactScroll = ttk.Scrollbar(contactList, orient=VERTICAL, command=contactList.yview)
        contactScroll.place(x=520, y=0, width=20, height=320)
        contactList.configure(yscrollcommand=contactScroll.set)

        self.message = StringVar()
        self.messageEntry = Entry(self.rootMain, width=120, textvariable=self.message)
        self.messageEntry.place(x=5, y=330, width=485, height=50)

        sendButton = Button(self.rootMain, text="发送")
        sendButton.place(x=500, y=345, width=30, height=20)

        self.rootMain.mainloop()


Login = LoginWindow()
Message = MainWindow()

# UDP部分
ip_port = (IP, int(PORT))
s = socket(AF_INET, SOCK_DGRAM)

if username:
    s.sendto(username.encode(), ip_port)  # 发送用户名
else:
    username = IP + ':' + PORT
    s.sendto(username.encode(), ip_port)


def send():
    oneMessage = Message.messageEntry.get()
    s.sendto(oneMessage.encode(), ip_port)
    print("已发送:" + oneMessage)
    Message.message.set("")
    return "break"

def
