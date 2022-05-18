import socket
import threading
import pygame
import random
import queue
import time
import math
# size of screen: 1200 X 1200

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
        self.addresses = queue.Queue()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((self.host, self.port))
        #self.server_socket.listen()
        self.startPlayers = {}

        s = sendToClient(self.q, self.server_socket, self.players_locations.keys(), self.addresses)
        s.start()

    def makePosition(self):
        return (random.randint(0, 1200), random.randint(0, 1200))

    def run(self):
        print("Server is up and running")
        # pygame.init()
        # size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        # screen = pygame.display.set_mode(size)
        while True:
            (data, addr) = self.server_socket.recvfrom(1024)
            if data.decode() == "out":
                del self.players_locations[addr]
                for i in self.players_locations.keys():
                    self.q.put((("out"+str(addr)), i))

            elif data.decode() == "Hello" and addr not in self.players:
                print("********************new player***********************************")
                #adding the new player
                self.counter += 1
                self.players.append(addr)

                #making and sending random backstage position for the new player:
                cPosition = self.makePosition()
                self.players_locations[addr] = cPosition
                print("PlAYERS: ", self.players_locations)
                self.server_socket.sendto((str(cPosition)).encode(), addr)

                c = listenToClient(addr, self, self.q, cPosition)
                c.start()
            else:
                position = toTuple(data.decode())
                #print("position i got from client: ", position)
                self.players_locations[addr] = position
                #print("locations: ", self.players_locations)
            for i in self.players_locations.keys():
                self.addresses.put(i)
            c = calc(self.players_locations, self.q)
            c.start()

def toTuple(st: str):
    start = st.find("(")
    end = st.find(",")
    #print(st[start+1:end])
    e = st.find(")")
    #print(st[end + 1:e], ", ", len(st[start+1:end]))
    return (int(st[start+1:end]), int(st[end + 1:e]))


class sendToClient(threading.Thread):
    def __init__(self, q, server, players, addr):
        #threading.Thread.__init__(self)
        super(sendToClient, self).__init__()
        self.q = q
        self.server = server
        self.addr = players
        self.addresses = addr
        self.count = 0

    def run(self):
        print("sending")
        while True:
            if not self.q.empty():
                message = self.q.get()
                #print("players to send to: ", self.addr)
                #for i in self.addr:
                    #if i != message[0]:
                # while not self.addresses.empty():
                #     try:
                #         i = self.addresses.get()
                #         self.server.sendto((str(message[1])+str(self.count)).encode(), i)
                #         print(self.count, " sending to: ", i)
                #         self.count += 1
                #             #message[0].send(message[1].encode())
                #     except:
                #         print('socket error :', )

                msg = message[0]
                addr = message[1]
                print("sending: ", msg, "to: ", addr)
                self.server.sendto((str(msg)).encode(), addr)
                print("q after sending: ", list(self.q.queue))
                time.sleep(0.1)

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
        #None
        #self.server.sendto("welcome to game".encode(), self.addr)
        #print("addr: ", self.addr)
        while self.running:
            self.server.sendto("welcome to game".encode(), self.addr)
            time.sleep(0.1)

class calc(threading.Thread):
    def __init__(self, playersLocations, q):
        threading.Thread.__init__(self)
        self.locations = playersLocations
        self.q = q

    def calc_distanse(self, loc1, loc2):
        x = math.pow((loc1[0] - loc2[0]), 2)
        y = math.pow((loc1[1] - loc2[1]), 2)
        return math.sqrt(x+y)

    def run(self):
        #print("current locations: ", self.locations)
        for a in list(self.locations):
            #print("a: ", a)
            loc1 = self.locations[a]
            for b in list(self.locations):
                if b is not a:
                    loc2 = self.locations[b]
                    dis = self.calc_distanse(loc1, loc2)
                    #print("max dis: ", math.sqrt(720000), "current dis = ", dis)
                    if dis <= math.sqrt(180000) and ((b[1], loc2), a) not in self.q.queue:

                        self.q.put(((b[1], loc2), a))
                        print("q: ", list(self.q.queue))
                        time.sleep(0.1)
                        #self.q.put((b, a))
                        #time.sleep(0.1)

if __name__ == '__main__':
        s = threadServer(IP, PORT, outgoingQ)
        s.start()
        s.join()