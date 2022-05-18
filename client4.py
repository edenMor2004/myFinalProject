import socket
import pygame
import random
import threading
import time

IP = "127.0.0.1"
PORT = 5566
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
MAX_X = 500
MAX_Y = 339

RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (153, 153, 255)
IMAGE = 'C:/Users/yossi/syber/map2.jfif'
REFRESH_RATE = 80
LEFT = 1
SCROLL = 2
RIGHT = 3
VELOCITY = 10
objects = []
clientNumber = 0


class Wrapper():
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

class Player(pygame.sprite.Sprite):
    def __init__(self, color, center):
        pygame.sprite.Sprite.__init__(self)
        #threading.Thread.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = center

    def move(self, sprites, myPos):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            myPos = self.right(sprites, myPos)
        if keys[pygame.K_LEFT]:
            myPos = self.left(sprites, myPos)
        if keys[pygame.K_UP]:
            myPos = self.up(sprites, myPos)
        if keys[pygame.K_DOWN]:
            myPos = self.down(sprites, myPos)
        #print("ny position after moving: ", myPos)
        return myPos

    def right(self, sprites, myPos):
        for s in sprites:
            if s is not self:
                #drawScreen(screen, sprites)
                #print("before: ", s.rect.x)
                #)
                print("moving rightttttttttt")
                screen.fill((2, 255, 255))
                pygame.display.flip()
                #time.sleep(0.1)
                sprites.remove(s)
                #s.rect.center = (s.rect.center[0] - VELOCITY, s.rect.center[1])
                #sprites.add(Player(RED, (s.rect.center[0] - VELOCITY, s.rect.center[1])))
                #print("after: ", s.rect.x)
        if (myPos[0] + VELOCITY) <= 1200:
            myPos = (myPos[0] + VELOCITY, myPos[1])
        return myPos

    def left(self, sprites, myPos):
        for s in sprites:
            if s is not self:
                #drawScreen(screen, sprites)
                #print("before: ", s.rect.x)
                screen.fill((2, 255, 255))
                pygame.display.flip()
                sprites.remove(s)
                #sprites.add(Player((2, 255, 255), s.rect.center))
                #s.rect.center = (s.rect.center[0] + VELOCITY, s.rect.center[1])
                sprites.add(Player(RED, (s.rect.center[0] + VELOCITY, s.rect.center[1])))
                #print("after: ", s.rect.x)
        if (myPos[0] - VELOCITY) >= 0:
            myPos = (myPos[0] - VELOCITY, myPos[1])
        return myPos

    def up(self, sprites, myPos):
        for s in sprites:
            if s is not self:
                #drawScreen(screen, sprites)
                #print("before: ", s.rect.x)
                screen.fill((2, 255, 255))
                pygame.display.flip()
                sprites.remove(s)
                #sprites.add(Player((2, 255, 255), s.rect.center))
                s.rect.y += VELOCITY
                #print("after: ", s.rect.x)
        if (myPos[1] - VELOCITY) >= 0:
            myPos = (myPos[0], myPos[1] - VELOCITY)
        return myPos

    def down(self, sprites, myPos):
        for s in sprites:
            if s is not self:
                #drawScreen(screen, sprites)
                #print("before: ", s.rect.x)
                screen.fill((2, 255, 255))
                pygame.display.flip()
                sprites.remove(Player(RED, s.rect.center))
                #sprites.add(Player((2, 255, 255), s.rect.center))
                s.rect.y -= VELOCITY
                #print("after: ", s.rect.x)
        if (myPos[1] + VELOCITY) <= 1200:
            myPos = (myPos[0], myPos[1] + VELOCITY)
        return myPos


def toTuple(st: str):
    start = st.find("(")
    end = st.find(",")
    #print(st[start+1:end])
    e = st.find(",", end+1)
    en = st.find(")")
    #print(st[end + 1:e], ", ", len(st[start+1:end]))
    return int(st[start+1:end]), (int(st[end+3:e]), int(st[e+1:en]))


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

def fromTupleToString(tup):
    None

def create_pos(st:str):
    start = st.find("(")
    end = st.find(",")
    en = st.find(")")
    return (int(st[start+1:end]), int(st[end+1:en]))

def addr_to_tuple(st: str):
    start = st.find("(")
    end = st.find(",")
    en = st.find(")")
    return (st[start + 1:end], int(st[end + 1:en]))

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

    #p1 = Player(RED, (WINDOW_WIDTH / 3, WINDOW_HEIGHT / 3))
    #(data, server) = client.recvfrom(1024)
    #print("from server: ", data.decode())
    # sprites.add(p)
    locations = {}
    #sprites.add(p1)

    while run:
        #print("in")
        #(data, server) = client.recv(1024).decode()
        #print("server sent: ", data)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client.sendto("out".encode(), (IP, PORT))
                run = False
                # pygame.quit()

        #sprites.update()
        #print("sprites: ", p1.rect.x)

        sprites.add(p)
        sprites.draw(screen)
        pygame.display.flip()
        time.sleep(0.1)
        sprites.empty()

        myPosition = p.move(sprites, myPosition)
        print("my position: ", str(myPosition))
        #time.sleep(0.1)
        client.sendto(str(myPosition).encode(), (IP, PORT))

        (position, server) = client.recvfrom(1024)
        info = position.decode()
        if "out" in info:
            por = addr_to_tuple(info)[1]
            # sprites.add(Player((2, 255, 255), locations[por]))
            # sprites.remove(Player(RED, locations[por]))
            locations.pop(por)

        elif "(" in info:

            print("-----------------------------------------------------------got from server: ", position.decode())
            ad, pos = toTuple(info)
            #if ad in locations.keys():
                # sprites.remove(Player(RED, locations[ad]))
                # sprites.add(Player((2,255,255),locations[ad]))

            x = pos[0]
            y = pos[1]
            #print("removes: ", pos)
            #
            #print("removed? ", sprites.has(Player(RED, pos)))
            #sprites.add(Player((2, 25, 255), pos))
            #sprites.draw()
            if x > 600:
                x = x-600
               #x = 600 - ((1200 - x)/2)

            if y > 600:
                y = y-600
                #y = 600 - ((1200 - y)/2)
            print("another player location: (" , x , ", ", y, ")" )
            #if p1 in sprites:

            #p1 = Player(RED, (x, y))
            #time.sleep(0.1)

            #sprites.add(p1)
            locations[ad] = (x, y)

            for i in locations.keys():
                sprites.add(Player(RED, locations[i]))
        #time.sleep(0.1)

        # try:
        #     position = toTuple(position.decode())
        #     print("the position I got from server: ", position)
        # except:
        #     print("something is wrong - didnt get position")
        # if position != myPosition and (type(position) is tuple):
        #    print("position: ", position)
        #    p1 = Player(RED, position)
        #    sprites.add(p1)
        print("locations: ", locations)


#if p.x not in xList or p.y not in yList and paint == True:
if __name__ == '__main__':
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.sendto("Hello".encode(), (IP, PORT))
    print("my;/", my_socket)
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    my_port = find_my_port(my_socket)
    pygame.display.set_caption(f"Client {my_port}")
    screen.fill((2, 255, 255))
    pygame.display.flip()

    main(screen, my_socket)

