import socket
import threading
import pygame
import random

IP = "127.0.0.1"
PORT = 5566
ADDR = (IP, PORT)
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 339

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
        self.server_socket = socket.socket()
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

    def run(self):
        print("Server is up and running")
        # pygame.init()
        # size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        # screen = pygame.display.set_mode(size)
        while True:
            client, addr = self.server_socket.accept()
            client.settimeout(60)
            self.counter += 1
            #self.players[self.counter] = [client, addr]
            c = listenToClient(client, addr)
            self.players_locations[client] = (c.posX, c.posY)
            print("PlAYERS: ", self.players_locations)
            self.send_to_clients(client)
            c.start()
            print("run client ended")
            #self.players_locations[c] = (c.posX, c.posY)
            #self.send_to_clients(c)

    def send_to_clients(self, p):
        print("sending new player to all players")
        for c in self.players_locations.keys():
            c.send(f"new player:{self.players_locations[p]}")

class listenToClient(threading.Thread):
    def __init__(self, client, addr):
        threading.Thread.__init__(self)
        self.client = client
        self.addr = addr
        self.posX = random.randint(0, WINDOW_WIDTH)
        self.posY = random.randint(0, WINDOW_HEIGHT)
        self.running = True

    def run(self):
        self.client.send("welcome to game".encode())
        self.client.send(f"your location: X = {self.posX}, Y = {self.posY}".encode())


        # pygame.init()
        # size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        # screen = pygame.display.set_mode(size)
        # pygame.display.set_caption("Game")
        # img = pygame.image.load(IMAGE)
        # screen.blit(img, (0, 0))
        # pygame.display.flip()
        # finish = False
        # while not finish:
        #     self.client.send("still here".encode())
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             finish = True

# def main():
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind(ADDR)
#     server.listen()
#     print("[server is up and listening]")
#
#     while True:
#         connection, adress = server.accept()

if __name__ == '__main__':
        s = threadServer(IP, PORT)
        s.start()
        s.join()