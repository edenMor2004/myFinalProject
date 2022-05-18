import socket
import threading
import pygame
import random

IP = "127.0.0.1"
PORT = 5566
ADDR = (IP, PORT)
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (153, 153, 255)

IMAGE = 'C:/Users/yossi/syber/map2.jfif'
REFRESH_RATE = 40
LEFT = 1
SCROLL = 2
RIGHT = 3
VELOCITY = 5


class threadServer(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.players = {}
        self.counter = 0
        # pygame.init()
        # size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        # self.screen = pygame.display.set_mode(size)
        self.players_locations = {}
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((self.host, self.port))
        #self.server_socket.listen()

    def run(self):
        print("Server is up and running")
        # pygame.init()
        # size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        # screen = pygame.display.set_mode(size)
        while True:
            (data, addr) = self.server_socket.recvfrom(1024)
            print("data: ", data.decode())
            #client.settimeout(60)
            self.counter += 1
            #self.players[self.counter] = [client, addr]
            c = listenToClient(addr, self)
            self.players_locations[addr] = (c.posX, c.posY)
            print("PlAYERS: ", self.players_locations)
            #m = sendToClient("*************************new player**************************************************************************************8",self.players_locations, self.server_socket)
            #m.start()
            #if len(self.players_locations) > 1:
            #    self.send_to_clients(addr)
            c.start()
            print("run client ended")
            #self.players_locations[c] = (c.posX, c.posY)
            #self.send_to_clients(c)
    #def delay(self):
        #3for i in range()

    # def send_to_clients(self, p):
    #     print("sending new player to all players")
    #     for c in self.players_locations.keys():
    #         if c is not p:
    #             self.server_socket.sendto(f"new player connected".encode(), c)
    #             print("sent new player")

class sendToClient(threading.Thread):
    def __init__(self, msg, players, server):
        #threading.Thread.__init__(self)
        super(sendToClient, self).__init__()
        self.msg = msg
        self.players = players
        self.server = server

    def run(self):
        for p in self.players.keys():
            print("sending to: ", p)
            self.server.sendto(self.msg.encode(), p)

class listenToClient(threading.Thread):
    def __init__(self, addr, Tserver):
        threading.Thread.__init__(self)
        #self.client = client
        self.addr = addr
        self.server = Tserver.server_socket
        self.posX = random.randint(0, WINDOW_WIDTH)
        self.posY = random.randint(0, WINDOW_HEIGHT)
        self.running = True
        self.players = Tserver.players_locations
        self.Tserver = Tserver

    def run(self):
        self.server.sendto("welcome to game".encode(), self.addr)
        while self.running:
            self.server.sendto((str(self.players)).encode(), self.addr)
            #self.server.sendto("................".encode(), self.addr)
            print(self.addr, ": ", "self.Tserver.players_locations:", self.Tserver.players_locations)

            #self.server.sendto(f"your location: X = {self.posX}, Y = {self.posY}".encode(), self.addr)
            self.Tserver = T
            self.players = self.Tserver.players_locations

if __name__ == '__main__':
        s = threadServer(IP, PORT)
        s.start()
        s.join()