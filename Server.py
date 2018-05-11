# -*- encoding: utf-8 -*-
import socket
import threading
from time import gmtime, strftime
global count
global id
class Server:
    def __init__(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock = sock
        self.sock.bind((host, port))
        self.sock.listen(5)
        print('Server', socket.gethostbyname(host), 'listening ...')
        self.mylist = list()

    def checkConnection(self):
        global count
        connection, addr = self.sock.accept()
        count += 1
        print(count)
        print('Accept a new connection', connection.getsockname(), connection.fileno())


        try:
            buf = connection.recv(1024).decode()
            if buf == '1':
                # start a thread for new connection
                mythread = threading.Thread(target=self.subThreadIn, args=(connection, connection.fileno()))
                mythread.setDaemon(True)
                mythread.start()


            else:
                connection.send(b'please go out!')
                connection.close()
        except:
            pass

    # send whatToSay to every except people in exceptNum
    def tellOthers(self, exceptNum, whatToSay):
        for c in self.mylist:
            if c.fileno() != exceptNum:
                try:
                    c.send(whatToSay.encode())
                except:
                    pass


    def subThreadIn(self, myconnection, connNumber):
        global count
        global id
        self.mylist.append(myconnection)

        while True:
            try:
                recvedMsg = myconnection.recv(1024).decode()
                if recvedMsg:
                    if ':' not in recvedMsg:
                        id.append(recvedMsg)
                        self.tellOthers(connNumber, "System:  "+ str(recvedMsg) + "in the chat room.")
                    else:
                        self.tellOthers(connNumber, recvedMsg)
                else:
                    pass

            except (OSError, ConnectionResetError):
                count -= 1
                self.tellOthers(connNumber, "New chat room people number " + str(count))
                print(count)
                print("Someone leave! Chat room")
                try:
                    self.mylist.remove(myconnection)

                except:
                    pass

                myconnection.close()
                return


def main():
    s = Server('140.138.145.9', 5550)#by Ping
    global count
    global id
    id = dict()
    count = 0
    while True:
        s.checkConnection()


if __name__ == "__main__":
    main()

