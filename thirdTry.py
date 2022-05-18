import socket
import threading
import pygame
import random
import queue
import time

IP = "127.0.0.1"
PORT = 5566
ADDR = (IP, PORT)
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (153, 153, 255)
size = 1024
IMAGE = 'C:/Users/yossi/syber/map2.jfif'
REFRESH_RATE = 40
LEFT = 1
SCROLL = 2
RIGHT = 3
VELOCITY = 5
outgoingQ = queue.Queue()

class threadServer(threading.Thread):
    def __init__(self, host, port, q):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.players = []
        self.counter = 0
        self.q = q
        # pygame.init()
        # size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        # self.screen = pygame.display.set_mode(size)
        self.players_locations = {}
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((self.host, self.port))
        #self.server_socket.listen()
        self.startPlayers = {}

        s = sendToClient(self.q, self.server_socket, self.players_locations.keys())
        s.start()

    def makePosition(self):
        return (random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT))

    def run(self):
        print("Server is up and running")
        # pygame.init()
        # size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        # screen = pygame.display.set_mode(size)
        while True:
            (data, addr) = self.server_socket.recvfrom(1024)
            #print(" data first: ", data.decode())
            #client.settimeout(60)
            #print("got from this addr: ", addr)
            if addr not in self.players_locations.keys():
                print("********************new player***********************************")
                #print("data first: ", data.decode())
                self.counter += 1
                #self.players[self.counter] = [client, addr]

                #self.q.put((addr, cPosition))

                #if addr not in self.players_locations.keys():
                self.players.append(addr)
                cPosition = self.makePosition()
                self.players_locations[addr] = cPosition
                print("PlAYERS: ", self.players_locations)

                self.server_socket.sendto((str(cPosition)).encode(), addr)

                c = listenToClient(addr, self, self.q, cPosition)
                c.start()

def toTuple(st: str):
    start = st.find("(")
    end = st.find(",")
    #print(st[start+1:end])
    e = st.find(")")
    #print(st[end + 1:e], ", ", len(st[start+1:end]))
    return (int(st[start+1:end]), int(st[end + 1:e]))


class sendToClient(threading.Thread):
    def __init__(self, q, server, players):
        #threading.Thread.__init__(self)
        super(sendToClient, self).__init__()
        self.q = q
        self.server = server
        self.addr = players

    def run(self):
        print("sending")
        while True:
            if not self.q.empty():
                message = self.q.get()
                #print("players to send to: ", self.addr)
                #for i in self.addr:
                    #if i != message[0]:
                try:
                    i =
                    self.server.sendto((str(message[1])).encode(), )
                            #print("sending to: ", i, "sending: ", (str(message[1])))
                            #message[0].send(message[1].encode())
                except:
                    print('socket error :', )

            #time.sleep(0.1)

class listenToClient(threading.Thread):
    def __init__(self, addr, Tserver, q, loc):
        threading.Thread.__init__(self)
        #self.client = client
        self.location = loc
        self.addr = addr
        self.server = Tserver.server_socket
        #self.posX = random.randint(0, WINDOW_WIDTH)
        #self.posY = random.randint(0, WINDOW_HEIGHT)
        self.running = True
        self.players = Tserver.players_locations
        #self.Tserver = Tserver
        self.q = q

    def run(self):
        self.server.sendto("welcome to game".encode(), self.addr)
        #print("addr: ", self.addr)
        while self.running:

            (data, client) = self.server.recvfrom(size)
            #print("data second: ", data.decode())
            try:
                self.location = toTuple(data.decode())
            #print("loc: ", self.location)
                #time.sleep(0.1)
                self.q.put((self.addr, self.location))
            except:
                print("something didnt work, data: ", data.decode())
            #print(self.q.queue)


if __name__ == '__main__':
        s = threadServer(IP, PORT, outgoingQ)
        s.start()
        s.join()