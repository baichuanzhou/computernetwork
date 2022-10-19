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
users = []
Lock = threading.Lock()


class Server(threading.Thread):
    def __init__(self, port=50007):
        threading.Thread.__init__(self)
        self.ADDRESS = ('', port)
        self.s = socket(AF_INET, SOCK_STREAM)
        os.chdir(sys.path[0])

    def tcpConnect(self, connect, address):
        username = connect.recv(1024).decode()

        for i in range(len(users)):
            if username == users[i][1]:
                print('Username already taken!')
                username = username + '_2'

        if username == 'no name':
            username = address[0] + ':' + address[1]

        users.append((connect, username, address))

        print(' New connection: ', address, ':', username, end='')
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
            Queue.put((address, data))
        finally:
            Lock.release()

    def sendData(self):
        while True:
            if not Queue.empty():
                data = ''
                message = Queue.get()
                if isinstance(message[1], str):
                    for i in range(len(users)):
                        # users[i][1] 是用户名，users[i][2]是address， 将message[0]改为用户名
                        for j in range(len(users)):
                            if message[0] == users[j][2]:
                                print(' Message from user[{}]'.format(j))
                                data = ' ' + users[i][1] + ':' + message[1]
                                break
                        users[i][0].send(data.encode())

                if isinstance(message[1], list):
                    data = json.dumps(message[1])
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
    server = Server()
    server.start()
    while True:

        time.sleep(1)
        if not server.isAlive():
            print("Connection lost!")
            sys.exit(0)
