from socket import *
import time
from tkinter.scrolledtext import ScrolledText
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import threading
import json
import util



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
        print(self.USERNAME + '*')
        self.rootLogin.destroy()


class UserWindow:
    def __init__(self, root):
        self.rootMain = Tk()
        self.rootMain.geometry("650x480")
        self.rootMain.resizable(False, False)
        self.rootMain.title("消息界面")

        self.contacts = []

        self.root = root
        self.IP = self.root.IP
        self.PORT = self.root.PORT
        self.USERNAME = self.root.USERNAME

        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.connect((self.IP, int(self.PORT)))

        if self.USERNAME:
            self.s.send(self.USERNAME.encode())
        else:
            print('*')
            self.s.send('no name'.encode())

        self.makeDialogueTo = "Nobody"

        self.messageList = ScrolledText(self.rootMain)
        self.messageList.tag_config('red', foreground='red')
        self.messageList.tag_config('blue', foreground='blue')
        self.messageList.tag_config('green', foreground='green')
        self.messageList.tag_config('pink', foreground='pink')
        self.messageList.insert(END, 'Welcome to the chat room!', 'blue')

        self.messageList.place(x=5, y=0, width=485, height=320)

        messageScroll = ttk.Scrollbar(self.messageList, orient=VERTICAL, command=self.messageList.yview)
        messageScroll.place(x=460, y=0, width=20, height=320)
        self.messageList.configure(yscrollcommand=messageScroll.set)

        self.contactList = Listbox(self.rootMain)
        self.contactList.place(x=490, y=0, width=140, height=320)
        self.contactList.bind('<ButtonRelease-1>', self.privateDialogue)

        contactScroll = ttk.Scrollbar(self.contactList, orient=VERTICAL, command=self.contactList.yview)
        contactScroll.place(x=520, y=0, width=20, height=320)
        self.contactList.configure(yscrollcommand=contactScroll.set)

        self.message = StringVar()
        self.messageEntry = Entry(self.rootMain, width=120, textvariable=self.message)
        self.messageEntry.place(x=5, y=330, width=485, height=50)

        sendButton = Button(self.rootMain, text="send", command=self.sendMessage)  # 需要定义函数
        sendButton.place(x=500, y=345, width=30, height=20)
        self.rootMain.bind('<Return>', self.sendMessage)

    def sendMessage(self, *args):
        self.contacts.append('------Group chat-------')
        if self.makeDialogueTo not in self.contacts:
            messagebox.showerror("Send error", message="There is nobody there!")
            return
        messageEncode = (self.message.get() + ":;" + self.USERNAME + ":;" + self.makeDialogueTo).encode()
        self.s.send(messageEncode)

        self.message.set("")
        return "break"

    def receiveMessage(self):
        while True:
            data = self.s.recv(1024)
            data = data.decode()
            print("data.decode():", data)
            try:
                data = json.loads(data)
                print("json.loads(data):", data)
                self.contactList.delete(0, END)
                self.contacts = data
                showContactsNumber = '      Users Online: ' + str(len(data))
                self.contactList.insert(END, showContactsNumber)
                self.contactList.itemconfig(END, fg="green", bg="#f0f0ff")
                self.contactList.insert(END, '------Group chat-------')
                for contact in self.contacts:
                    self.contactList.insert(END, contact)
                    self.contactList.itemconfig(END, bg="green")
            except:
                data = data.split(':;')
                print(data)
                dataMessage = data[0]
                dataSenderName = data[1]
                dataReceiverName = data[2]
                dataMessage = '\n' + dataMessage
                print(dataMessage)
                if dataReceiverName == '------Group chat-------':
                    if dataSenderName == self.USERNAME:
                        self.messageList.insert(END, dataMessage, 'blue')
                    else:
                        self.messageList.insert(END, dataMessage, 'green')
                    if len(data) == 4:
                        self.messageList.insert(END, dataMessage, 'pink')
                elif dataSenderName == self.USERNAME or dataReceiverName == self.USERNAME:
                    self.messageList.insert(END, dataMessage, 'red')
            self.messageList.see(END)

    def privateDialogue(self, *args):
        contactIndices = self.contactList.curselection()
        index = contactIndices[0]
        if index > 0:
            cursorContent = self.contactList.get(index)
            if cursorContent == "------Group chat-------":
                self.rootMain.title(self.USERNAME)
                return
            self.makeDialogueTo = cursorContent
            privateTitle = self.USERNAME + ' --> ' + self.makeDialogueTo
            self.rootMain.title(privateTitle)


Login = LoginWindow()
Login.rootLogin.mainloop()

User = UserWindow(Login)
process = threading.Thread(target=User.receiveMessage)
process.start()
User.rootMain.mainloop()

