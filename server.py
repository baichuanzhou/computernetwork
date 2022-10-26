from tkinter import *
from socket import *
import threading
import queue
import os
import os.path
import sys
import json
import time

Queue = queue.Queue()
users = []  # [0]: 套接字接口 [1]: 用户名 [2]: 用户IP地址+端口
Lock = threading.Lock()
usernames = []


class Server(threading.Thread):
    def __init__(self, port=50007):
        threading.Thread.__init__(self)
        self.ADDRESS = ('', port)
        self.s = socket(AF_INET, SOCK_STREAM)
        os.chdir(sys.path[0])

    def tcpConnect(self, connect, address):
        username = connect.recv(1024).decode()
        # print(connect, address)

        username = self.adjustName(username, address)
        users.append((connect, username, address))
        usernames.append(username)
        print(' New connection: ', address, ':', username, end='\n')
        onlineUsers = [users[i][1] for i in range(len(users))]

        self.receiveMessage(onlineUsers, address)
        try:
            while True:
                data = connect.recv(1024)
                data = data.decode()
                self.receiveMessage(data, address)
            connect.close()
        except:
            print(username + ' Connection lost')
            self.delUsers(connect, address)
            connect.close()

    def adjustName(self, username, address):
        if username == 'no name':
            username = address[0] + ':' + address[1]

        name_count = 1
        while username in usernames:
            name_count += 1
            username = username.partition('_')[0] + '_' + str(name_count)
        return username

    def delUsers(self, connect, address):
        count = 0
        for user in users:
            if user[0] == connect:
                users.pop(count)
                print(' Remaining online users: ', end='')
                onlineUsers = [users[i][1] for i in range(len(users))]
                self.receiveMessage(onlineUsers, address)
                print(onlineUsers)
                break
            count += 1

    def receiveMessage(self, data, address):
        Lock.acquire()
        try:
            Queue.put((data, address))
        finally:
            Lock.release()

    def sendData(self):
        while True:
            if not Queue.empty():
                data = ''
                message, sender = Queue.get()
                print("sender: ", sender)
                print("message: ", message)
                if isinstance(message, str):
                    for i in range(len(users)):
                        # users[i][1] 是用户名，users[i][2]是address， 将message[0]为用户名
                        for j in range(len(users)):
                            if sender == users[j][2]:
                                print(' Message from user[{}]'.format(j))
                                data = ' ' + users[j][1] + ':' + message
                                break
                        users[i][0].send(data.encode())

                if isinstance(message, list):
                    data = json.dumps(message)
                    for i in range(len(users)):
                        try:
                            users[i][0].send(data.encode())
                        except:
                            pass

    def run(self):
        self.s.bind(self.ADDRESS)
        self.s.listen(5)
        print('Server starts running...')
        process = threading.Thread(target=self.sendData)
        process.start()
        while True:
            connect, address = self.s.accept()
            tcpProcess = threading.Thread(target=self.tcpConnect, args=(connect, address))
            tcpProcess.start()
        self.s.close()


if __name__ == '__main__':
    server = Server(11111)
    server.start()
    while True:
        time.sleep(1)
        if not server.is_alive():
            print("Connection lost!")
            sys.exit(0)
