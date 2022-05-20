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
ADDR = (IP, PORT)

size = 1024

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
        self.subServersAddr = {}
        #self.server_socket.listen()
        self.startPlayers = {}

        #area of sub servers in the beggining
        self.subServers = {1:[((0,600),(0,600))], 2:[((600,1200), (0,600))], 3:[((0,600), (600,1200))], 4:[((600,1200), (600,1200))]}
        #s = sendToClient(self.q, self.server_socket, self.players_locations.values(), self.addresses)
        # s.start()

    def makePosition(self):
        return (random.randint(0, 1200), random.randint(0, 1200))

    def run(self):
        print("Server is up and running")
        # pygame.init()
        # size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        # screen = pygame.display.set_mode(size)
        while True:
            (data, addr) = self.server_socket.recvfrom(1024)
            information = data.decode()
            #print("got: ", information)
            if information == "out":
                del self.players_locations[addr]
                for i in self.players_locations.keys():
                    self.q.put((("out"+str(addr)), i))

            elif "Hello" in information and addr not in self.players:
                if "player" in information:
                    print("********************new player***********************************")
                    #adding the new player
                    self.counter += 1
                    self.players.append(addr)

                    #making and sending random backstage position for the new player:
                    cPosition = self.makePosition()
                    self.players_locations[addr] = cPosition
                    print("PlAYERS: ", self.players_locations)
                    self.server_socket.sendto((str(cPosition)).encode(), addr)
                    clientServer = self.sortPlayers(cPosition)
                    self.server_socket.sendto((str(self.subServers[clientServer][1])).encode(), addr)

                    times = {}
                    for i in self.subServers:
                        time = self.check_response_time(self.subServers[i][1])
                        print(f" server {i} time: {time}")
                        if time > 10:
                            print("changing server number ", i)
                            if i == 1:
                                self.subServers[i][0] = ((self.subServers[i][0][0][0], self.subServers[i][0][0][1]-50), (self.subServers[i][0][1][0], self.subServers[i][0][1][1]-50))
                                print("new rate" + str(self.subServers[i][0]))
                                self.server_socket.sendto(("new rate" + str(self.subServers[i][0])).encode(), self.subServers[i][1])
                                self.subServers[2][0] = ((self.subServers[2][0][0][0] - 50, self.subServers[2][0][0][1]), self.subServers[2][0][1])
                                print("new rate" + str(self.subServers[2][0]))
                                self.server_socket.sendto(("new rate" + str(self.subServers[2][0])).encode(),self.subServers[2][1])

                                self.subServers[3][0] = (self.subServers[3][0][0], (self.subServers[3][0][1][0] - 50, self.subServers[3][0][1][1]))
                                print("new rate" + str(self.subServers[3][0]))
                                self.server_socket.sendto(("new rate" + str(self.subServers[3][0])).encode(),self.subServers[3][1])
                            elif i == 2:
                                self.subServers[i][0] = ((self.subServers[i][0][0][0] + 50, self.subServers[i][0][0][1]) , (self.subServers[i][0][1][0], self.subServers[i][0][1][1]-50))
                                print("new rate" + str(self.subServers[i][0]))
                                self.server_socket.sendto(("new rate" + str(self.subServers[i][0])).encode(), self.subServers[i][1])

                                self.subServers[1][0] = ((self.subServers[1][0][0][0], self.subServers[1][0][0][1] + 50), self.subServers[1][0][1])
                                print("new rate" + str(self.subServers[1][0]))
                                self.server_socket.sendto(("new rate" + str(self.subServers[1][0])).encode(),self.subServers[1][1])

                                self.subServers[4][0] = (self.subServers[4][0][0], (self.subServers[4][0][1][0] - 50, self.subServers[4][0][1][1]))
                                print("new rate" + str(self.subServers[4][0]))
                                self.server_socket.sendto(("new rate" + str(self.subServers[4][0])).encode(),self.subServers[4][1])
                            elif i == 3:
                                self.subServers[i][0] = ((self.subServers[i][0][0][0], self.subServers[i][0][0][1] - 50), (self.subServers[i][0][1][0] + 50, self.subServers[i][0][1][1]))
                                print("new rate" + str(self.subServers[i][0]))
                                self.server_socket.sendto(("new rate" + str(self.subServers[i][0])).encode(), self.subServers[i][1])

                                self.subServers[1][0] = (self.subServers[1][0][0], (self.subServers[1][0][1][0], self.subServers[1][0][1][1] + 50))
                                print("new rate" + str(self.subServers[1][0]))
                                self.server_socket.sendto(("new rate" + str(self.subServers[1][0])).encode(),self.subServers[1][1])

                                self.subServers[4][0] = ((self.subServers[4][0][0][0] - 50, self.subServers[4][0][0][1]), self.subServers[4][0][1])
                                print("new rate" + str(self.subServers[4][0]))
                                self.server_socket.sendto(("new rate" + str(self.subServers[4][0])).encode(),self.subServers[4][1])
                            elif i == 4:
                                    self.subServers[i][0] = ((self.subServers[i][0][0][0] + 50, self.subServers[i][0][0][1]), (self.subServers[i][0][1][0] + 50, self.subServers[i][0][1][1]))
                                    print("new rate" + str(self.subServers[i][0]))
                                    self.server_socket.sendto(("new rate" + str(self.subServers[i][0])).encode(),self.subServers[i][1])

                                    self.subServers[2][0] = (self.subServers[2][0][0], (self.subServers[2][0][1][0], self.subServers[2][0][1][1] + 50))
                                    print("new rate" + str(self.subServers[2][0]))
                                    self.server_socket.sendto(("new rate" + str(self.subServers[2][0])).encode(),self.subServers[2][1])

                                    self.subServers[3][0] = ((self.subServers[3][0][0][0], self.subServers[3][0][0][1] + 50), self.subServers[3][0][1])
                                    print("new rate" + str(self.subServers[3][0]))
                                    self.server_socket.sendto(("new rate" + str(self.subServers[3][0])).encode(),self.subServers[3][1])

                        times[i] = time
                    print("times = ", times)


                if "server" in information:
                    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&server")
                    #print(information)
                    num = findNumOfSubServer(information)
                    self.subServers[num].append(addr)
                    print(self.subServers[num])
                    self.server_socket.sendto((str(self.subServers[num][0])).encode(), addr)
                    #s1 = listenToServer(addr, self.server_socket, num)
                    #s1.start()
                    #s1.join()

            elif "change server" in information:
                clientTransfer, clientLoc = addr_to_tuple(information)
                n = self.sortPlayers(clientLoc)
                print("address of client to transfer: ", clientTransfer)
                self.server_socket.sendto(("change server " + str(self.subServers[n][1])).encode(), clientTransfer)
                times = {}
                for i in self.subServers:
                    time = self.check_response_time(self.subServers[i][1])
                    print(f" server {i} time: {time}")
                    if time > 10:
                        print("changing server number ", i)
                        if i == 1:
                            self.subServers[i][0] = ((self.subServers[i][0][0][0], self.subServers[i][0][0][1] - 50),
                                                     (self.subServers[i][0][1][0], self.subServers[i][0][1][1] - 50))
                            print("new rate" + str(self.subServers[i][0]))
                            self.server_socket.sendto(("new rate" + str(self.subServers[i][0])).encode(),
                                                      self.subServers[i][1])
                            self.subServers[2][0] = (
                            (self.subServers[2][0][0][0] - 50, self.subServers[2][0][0][1]), self.subServers[2][0][1])
                            print("new rate" + str(self.subServers[2][0]))
                            self.server_socket.sendto(("new rate" + str(self.subServers[2][0])).encode(),
                                                      self.subServers[2][1])

                            self.subServers[3][0] = (
                            self.subServers[3][0][0], (self.subServers[3][0][1][0] - 50, self.subServers[3][0][1][1]))
                            print("new rate" + str(self.subServers[3][0]))
                            self.server_socket.sendto(("new rate" + str(self.subServers[3][0])).encode(),
                                                      self.subServers[3][1])
                        elif i == 2:
                            self.subServers[i][0] = ((self.subServers[i][0][0][0] + 50, self.subServers[i][0][0][1]),
                                                     (self.subServers[i][0][1][0], self.subServers[i][0][1][1] - 50))
                            print("new rate" + str(self.subServers[i][0]))
                            self.server_socket.sendto(("new rate" + str(self.subServers[i][0])).encode(),
                                                      self.subServers[i][1])

                            self.subServers[1][0] = (
                            (self.subServers[1][0][0][0], self.subServers[1][0][0][1] + 50), self.subServers[1][0][1])
                            print("new rate" + str(self.subServers[1][0]))
                            self.server_socket.sendto(("new rate" + str(self.subServers[1][0])).encode(),
                                                      self.subServers[1][1])

                            self.subServers[4][0] = (
                            self.subServers[4][0][0], (self.subServers[4][0][1][0] - 50, self.subServers[4][0][1][1]))
                            print("new rate" + str(self.subServers[4][0]))
                            self.server_socket.sendto(("new rate" + str(self.subServers[4][0])).encode(),
                                                      self.subServers[4][1])
                        elif i == 3:
                            self.subServers[i][0] = ((self.subServers[i][0][0][0], self.subServers[i][0][0][1] - 50),
                                                     (self.subServers[i][0][1][0] + 50, self.subServers[i][0][1][1]))
                            print("new rate" + str(self.subServers[i][0]))
                            self.server_socket.sendto(("new rate" + str(self.subServers[i][0])).encode(),
                                                      self.subServers[i][1])

                            self.subServers[1][0] = (
                            self.subServers[1][0][0], (self.subServers[1][0][1][0], self.subServers[1][0][1][1] + 50))
                            print("new rate" + str(self.subServers[1][0]))
                            self.server_socket.sendto(("new rate" + str(self.subServers[1][0])).encode(),
                                                      self.subServers[1][1])

                            self.subServers[4][0] = (
                            (self.subServers[4][0][0][0] - 50, self.subServers[4][0][0][1]), self.subServers[4][0][1])
                            print("new rate" + str(self.subServers[4][0]))
                            self.server_socket.sendto(("new rate" + str(self.subServers[4][0])).encode(),
                                                      self.subServers[4][1])
                        elif i == 4:
                            self.subServers[i][0] = ((self.subServers[i][0][0][0] + 50, self.subServers[i][0][0][1]),
                                                     (self.subServers[i][0][1][0] + 50, self.subServers[i][0][1][1]))
                            print("new rate" + str(self.subServers[i][0]))
                            self.server_socket.sendto(("new rate" + str(self.subServers[i][0])).encode(),
                                                      self.subServers[i][1])

                            self.subServers[2][0] = (
                            self.subServers[2][0][0], (self.subServers[2][0][1][0], self.subServers[2][0][1][1] + 50))
                            print("new rate" + str(self.subServers[2][0]))
                            self.server_socket.sendto(("new rate" + str(self.subServers[2][0])).encode(),
                                                      self.subServers[2][1])

                            self.subServers[3][0] = (
                            (self.subServers[3][0][0][0], self.subServers[3][0][0][1] + 50), self.subServers[3][0][1])
                            print("new rate" + str(self.subServers[3][0]))
                            self.server_socket.sendto(("new rate" + str(self.subServers[3][0])).encode(),
                                                      self.subServers[3][1])
                    times[i] = time
                print("times = ", times)


    def check_response_time(self, server):
        start = time.perf_counter()
        self.server_socket.sendto("time".encode(), server)
        (response, serverAddr) = self.server_socket.recvfrom(1024)
        return time.perf_counter() - start

    def sortPlayers(self, location):
        x = location[0]
        y = location[1]
        if x >= 0 and x <= 600 and y >= 0 and y <= 600:
            return 1
        if x >= 600 and x <= 1200 and y >= 0 and y <= 600:
            return 2
        if x >= 0 and x <= 600 and y >= 600 and y <= 1200:
            return 3
        if x >= 600 and x <= 1200 and y >= 600 and y <= 1200:
            return 4


def findNumOfSubServer(st: str):
    i = st.find("server")
    l = len("server")
    return int(st[i+l:])

# find client address and client location
def addr_to_tuple(st: str):
    start = st.find("(")
    mid = st.find(",")
    en = st.find(")")
    addr = (str(st[start + 2:mid-1]), int(st[mid + 1:en]))
    start = st.find("(", en)
    mid = st.find(",", start)
    en = st.find(")", mid)
    loc = (int(st[start + 1:mid]), int(st[mid + 1: en]))
    return addr, loc



if __name__ == '__main__':
        s = threadServer(IP, PORT, outgoingQ)
        s.start()
        s.join()