import socket
import pygame
import random
import threading
import time
import math

IP = "127.0.0.1"
PORT = 5571
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
MAX_X = 500
MAX_Y = 339

RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (153, 153, 255)

REFRESH_RATE = 80
LEFT = 1
SCROLL = 2
RIGHT = 3
VELOCITY = 10
objects = []
clientNumber = 0


class Player(pygame.sprite.Sprite):
    def __init__(self, color, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = center

    def move(self, sprites, myPos, locatios):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            myPos, locatios = self.right(sprites, myPos, locatios)
        if keys[pygame.K_LEFT]:
            myPos, locatios = self.left(sprites, myPos, locatios)
        if keys[pygame.K_UP]:
            myPos, locatios = self.up(sprites, myPos, locatios)
        if keys[pygame.K_DOWN]:
            myPos, locatios = self.down(sprites, myPos, locatios)
        #print("ny position after moving: ", myPos)
        return myPos, locatios

    def right(self, sprites, myPos, locs):
        for s in sprites:
            if s is not self:
                loc = s.rect.center
                sprites.add(Player((2, 255, 255), s.rect.center))
                if s.rect.center[0] - VELOCITY >= 0:
                    sprites.add(Player(RED, (s.rect.center[0] - VELOCITY, s.rect.center[1])))
                for i in locs:
                    if locs[i] == loc:
                        locs[i] = (s.rect.center[0] - VELOCITY, s.rect.center[1])

        if (myPos[0] + VELOCITY) <= 1200:
            myPos = (myPos[0] + VELOCITY, myPos[1])
        return myPos, locs

    def left(self, sprites, myPos, locs):
        for s in sprites:
            if s is not self:
                #drawScreen(screen, sprites)
                #print("before: ", s.rect.x)
                print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$4s.rect.center: ",s.rect.center)
                loc = s.rect.center
                sprites.add(Player((2, 255, 255), s.rect.center))
                if s.rect.center[0] + VELOCITY <=1200:
                    sprites.add(Player(RED, (s.rect.center[0] + VELOCITY, s.rect.center[1])))
                #sprites.remove(s)
                #print("after: ", s.rect.x)
                for i in locs:
                    if locs[i] == loc:
                        locs[i] = (s.rect.center[0] + VELOCITY, s.rect.center[1])
        if (myPos[0] - VELOCITY) >= 0:
            myPos = (myPos[0] - VELOCITY, myPos[1])
        return myPos, locs

    def up(self, sprites, myPos, locs):
        for s in sprites:
            if s is not self:
                #drawScreen(screen, sprites)
                #print("before: ", s.rect.x)
                print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$4s.rect.center: ",s.rect.center)
                loc = s.rect.center
                sprites.add(Player((2, 255, 255), s.rect.center))
                if s.rect.center[1]+VELOCITY <=1200:
                    sprites.add(Player(RED, (s.rect.center[0], s.rect.center[1]+VELOCITY)))
                #sprites.remove(s)
                #s.rect.y += VELOCITY
                #print("after: ", s.rect.x)
                for i in locs:
                    if locs[i] == loc:
                        locs[i] = (s.rect.center[0], s.rect.center[1]+VELOCITY)
        if (myPos[1] - VELOCITY) >= 0:
            myPos = (myPos[0], myPos[1] - VELOCITY)
        return myPos, locs

    def down(self, sprites, myPos, locs):
        for s in sprites:
            if s is not self:
                #drawScreen(screen, sprites)
                print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$4s.rect.center: ", s.rect.center)
                loc = s.rect.center
                sprites.add(Player((2, 255, 255), s.rect.center))
                if s.rect.center[1] - VELOCITY >=0:
                    sprites.add(Player(RED, (s.rect.center[0], s.rect.center[1] - VELOCITY)))
                #sprites.remove(s)
                #s.rect.y -= VELOCITY
                #print("after: ", s.rect.x)
                for i in locs:
                    if locs[i] == loc:
                        locs[i] = (s.rect.center[0], s.rect.center[1] - VELOCITY)
        if (myPos[1] + VELOCITY) <= 1200:
            myPos = (myPos[0], myPos[1] + VELOCITY)
        return myPos, locs

def toTuple(st: str):
    start = st.find("(")
    end = st.find(",")
    #print(st[start+1:end])
    e = st.find(",", end+1)
    en = st.find(")")
    #print(st[end + 1:e], ", ", len(st[start+1:end]))
    return int(st[start+1:end]), (int(st[end+3:e]), int(st[e+1:en]))

def create_loc_list(loc, len):
    lst = []
    for i in range(0, len):
        lst.append(loc+i)
    return lst

def find_my_port(client):
    sock = str(client)
    i = sock.find('laddr')
    end = sock.find(')')
    port = sock[i+18:end]
    return int(port)

def findPos(st: str):
    #print("st: ", tuple(st))
    #st = st.split(',')

    return tuple(st)


def create_pos(st:str):
    start = st.find("(")
    end = st.find(",")
    en = st.find(")")
    return (int(st[start+1:end]), int(st[end+1:en]))

def addr_to_tuple(st: str):
    start = st.find("(")
    end = st.find(",")
    en = st.find(")")
    return ('127.0.0.1', int(st[end + 1:en]))

def main(screen, client):
    run = True
    clock = pygame.time.Clock()
    my_port = find_my_port(client)
    print("port: ", my_port)

    #paint = True
    sprites = pygame.sprite.Group()
    # wrappers = pygame.sprite.Group()
    clock.tick(60)

    p = Player(PURPLE, (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
    #recv start position from server:
    (position, server) = client.recvfrom(1024)
    try:
         myPosition = create_pos(position.decode())
         print("my position: ", myPosition)
    except:
        print("something is wrong - didnt get position")

    (subServer, server) = client.recvfrom(1024)
    subAddr = addr_to_tuple(subServer.decode())
    print(subAddr)
    #my_socket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.sendto("Hello player".encode(), subAddr)

    #p1 = Player(RED, (WINDOW_WIDTH / 3, WINDOW_HEIGHT / 3))
    #(data, server) = client.recvfrom(1024)
    #print("from server: ", data.decode())

    locations = {}
    my_locs = {}
    #sprites.add(p1)

    while run:

        print("in")
        #(data, server) = client.recv(1024).decode()
        #print("server sent: ", data)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client.sendto("out".encode(), subAddr)
                run = False
                # pygame.quit()


        (position, server) = client.recvfrom(1024)
        info = position.decode()
        print("info: ", info)
        if "out" in info:
            print("outtttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt")
            por = addr_to_tuple(info)[1]
            if por in my_locs:
                sprites.add(Player((2, 255, 255), my_locs[por]))
                sprites.remove(Player(RED, my_locs[por]))
                del locations[por]
                del my_locs[por]

        elif "change server" in info:
            subAddr = addr_to_tuple(info)
            client.sendto("Hello player".encode(), subAddr)
            time.sleep(0.1)

        elif "(" in info:

            print("-----------------------------------------------------------got from server: ", position.decode())
            ad, pos = toTuple(info)
            if ad in locations.keys():
                sprites.remove(Player(RED, my_locs[ad]))
                sprites.add(Player((2,255,255), my_locs[ad]))

            x = pos[0]
            y = pos[1]

            sparex = math.fabs(x - myPosition[0])
            sparey = math.fabs(y - myPosition[1])
            if x > 600:
                x = x-600
            #    #x = 600 - ((1200 - x)/2)
            #
            if y > 600:
                y = y-600
            # if myPosition[0] > x:
            #     x = x - sparex
            # elif myPosition[0] < x:
            #     x = x + sparex
            # else:

                #y = 600 - ((1200 - y)/2)
            print("another player location: (", x, ", ", y, ")" )

            if ad in locations:
                if x > locations[ad][0]:
                    my_locs[ad] = (my_locs[ad][0] + VELOCITY, my_locs[ad][1])
                if x < locations[ad][0]:
                    my_locs[ad] = (my_locs[ad][0] - VELOCITY, my_locs[ad][1])
                if y > locations[ad][1]:
                    my_locs[ad] = (my_locs[ad][0], my_locs[ad][1] + VELOCITY)
                if y < locations[ad][1]:
                    my_locs[ad] = (my_locs[ad][0], my_locs[ad][1] - VELOCITY)
                locations[ad] = (x, y)

            else:
                locations[ad] = (x, y)
                my_locs[ad] = (x, y)

        for i in locations.keys():
            #if not sprites.has(Player(RED, locations[i])):
            sprites.add(Player(RED, my_locs[i]))

        myPosition, my_locs = p.move(sprites, myPosition, my_locs)
        print("locations: ", my_locs)
        print("my position: ", str(myPosition))
        # time.sleep(0.1)
        client.sendto(str(myPosition).encode(), subAddr)

        sprites.add(p)
        sprites.draw(screen)
        pygame.display.flip()
        sprites.empty()

        #time.sleep(0.1)



#if p.x not in xList or p.y not in yList and paint == True:
if __name__ == '__main__':
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.sendto("Hello player".encode(), (IP, PORT))
    print("my;/", my_socket)
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    my_port = find_my_port(my_socket)
    pygame.display.set_caption(f"Client {my_port}")
    screen.fill((2, 255, 255))
    pygame.display.flip()

    main(screen, my_socket)
