from tkinter import *
from socket import *
import threading
import util
import os
import os.path
import sys


class Server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.s = socket(AF_INET, SOCK_DGRAM)

    def receive(self):
        while True:
            userInfo, userAddress = self.s.recvfrom(1024)
            print(type(userInfo))
            userIP, userPORT = userAddress
