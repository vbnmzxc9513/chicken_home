import socket
import threading
import datetime
class Client:
    def __init__(self, host, port):
        global name
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock = sock
        self.sock.connect((host, port))
        print("Welcome to chat room!") #by Wei
        print('Input your name:')#chenda
        name = input()
        print ("Chats, Lets Welcome " + str(name)+" join us !!")#by chenpo
        self.sock.send(b'1')
        self.sock.send(name.encode())
        print(name + ":")

    def sendThreadFunc(self):
        global name

        while True:
            try:
                time_str = datetime.datetime.now()
                myword =  name +":" + input() +"   "+str(time_str.hour)+":"+str(time_str.minute)+":"+str(time_str.second)
                self.sock.send(myword.encode())
                print(name + ":")
            except ConnectionAbortedError:
                print('Server closed this connection!')
            except ConnectionResetError:
                print('Server is closed!')

    def recvThreadFunc(self):
        while True:
            try:
                otherword = self.sock.recv(1024) # socket.recv(recv_size)
                print(otherword.decode())
            except ConnectionAbortedError:
                print('Server closed this connection!')

            except ConnectionResetError:
                print('Server is closed!')

def main():
    global name
    c = Client('140.138.145.9', 5550)
    th1 = threading.Thread(target=c.sendThreadFunc)
    th2 = threading.Thread(target=c.recvThreadFunc)
    threads = [th1, th2]
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()


if __name__ == "__main__":
    main()
