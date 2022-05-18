import socket
import threading
import pygame
import random
import queue
import time
import math
# size of screen: 1200 X 1200

IP = "127.0.0.1"
PORT = 5571
myPort = 5569
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
    def __init__(self, host, port, q, rateX, rateY, mainServer, my_client):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.players = []
        self.counter = 0
        self.q = q
        self.rateX = rateX
        self.rateY = rateY
        self.mainServer = mainServer
        self.my_client = my_client
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
            print("in")
            print(f"rateX: {self.rateX}, rateY: {self.rateY}")
            (data, addr) = self.server_socket.recvfrom(1024)
            print("data: ", data.decode())
            d = data.decode()

            if "time" in d:
                self.my_client.sendto("here".encode(), addr)
                print("time checked")

            elif "new rate" in d:
                self.rateX, self.rateY = rateTuples(d)
                print(f"new rate x: {rateX}, new rate y: {rateY}")

            elif d == "out":
                del self.players_locations[addr]
                for i in self.players_locations.keys():
                    self.q.put((("out"+str(addr)), i))

            elif "Hello" in d and addr not in self.players:
                print("********************new player***********************************")
                #adding the new player
                self.counter += 1
                self.players.append(addr)

                #making and sending random backstage position for the new player:
                #cPosition = self.makePosition()
                #self.players_locations[addr] = cPosition
                #print("PlAYERS: ", self.players_locations)
                #self.server_socket.sendto((str(cPosition)).encode(), addr)

                c = listenToClient(addr, self, self.q)
                c.start()
            else:
                try:
                    position = toTuple(d)
                except:
                    None
                print("position i got from client: ", position)
                self.players_locations[addr] = position
                #print("locations: ", self.players_locations)

                if position[0] < self.rateX[0] or position[0] > self.rateX[1] or position[1] < self.rateY[0] or position[1] > self.rateY[1]:
                    print("position is not mine")
                    self.my_client.sendto(("change server " + str(addr) + ", " + str(position)).encode(), self.mainServer)
                    del self.players_locations[addr]
                    for i in self.players_locations.keys():
                        self.q.put((("out" + str(addr)), i))

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

                msg = message[0]
                addr = message[1]
                print("sending: ", msg, "to: ", addr)
                self.server.sendto((str(msg)).encode(), addr)
                print("q after sending: ", list(self.q.queue))
                time.sleep(0.1)

class listenToClient(threading.Thread):
    def __init__(self, addr, Tserver, q):
        threading.Thread.__init__(self)
        #self.client = client
        #self.location = loc
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

def find_my_port(client):
    sock = str(client)
    i = sock.find('laddr')
    end = sock.find(')')
    port = sock[i+18:end]
    return int(port)

#make tuple from big tuple
def rateTuples(bigTuple :str):
    s = bigTuple.find("(")
    m = bigTuple.find(",")
    e = bigTuple.find(")")
    smallTuple1 = (int(bigTuple[s+2:m]), int(bigTuple[m+1:e]))
    s = bigTuple.find("(",e)
    m = bigTuple.find(",",s)
    e = bigTuple.find(")",m)
    smallTuple2 = (int(bigTuple[s+1:m]), int(bigTuple[m+1:e]))
    return smallTuple1, smallTuple2

if __name__ == '__main__':
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        my_socket.sendto("Hello server3".encode(), ADDR)
        print("my;/", my_socket)
        myPort = find_my_port(my_socket)
        (data, server) = my_socket.recvfrom(size)
        rateX, rateY = rateTuples(data.decode())

        s = threadServer(IP, myPort, outgoingQ, rateX, rateY, server, my_socket)
        s.start()
        s.join()