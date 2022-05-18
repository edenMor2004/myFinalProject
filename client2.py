import socket
import pygame
import random
import threading

IP = "127.0.0.1"
PORT = 5566
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 239
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

class Rect():
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h

class Wrapper():
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

class Player(pygame.sprite.Sprite, threading.Thread):
    def __init__(self, color, center):
        pygame.sprite.Sprite.__init__(self)
        threading.Thread.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = center
        #self.screen = screen
        #self.client = client

    # def draw(self, screen): # draw the playerr
    #     pygame.draw.rect(screen, self.color, self.rect)
    # def run(self):
    #     run = True
    #
    #     clock = pygame.time.Clock()
    #
    #     paint = True
    #     sprites = pygame.sprite.Group()
    #     # wrappers = pygame.sprite.Group()
    #     p = Player(PURPLE, (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
    #     p1 = Player(RED, (WINDOW_WIDTH / 3, WINDOW_HEIGHT / 3))
    #
    #     sprites.add(self.)
    #     sprites.add(p1)
    #     # wrappers.add(Rect(p.rect.x+1, p.rect.y + 1, p.image.get_width() + 2, p.image.get_height()))
    #     # wrappers.add(Rect(p1.rect.x + 1, p1.rect.y + 1, p1.image.get_width() + 2, p1.image.get_height()))
    #     while run:
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 run = False
    #                 # pygame.quit()
    #         clock.tick(30)
    #         #sprites.update()
    #         print("sprites: ", p1.rect.x)
    #         sprites.draw(screen)
    #         pygame.display.flip()
    #         p.move(sprites)
    #         r = recvFromServer()
    #         r.start()
    #         data = r.run(self.client)
    #         print("got from server: ", data)

    def move(self, sprites):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.right(sprites)
        if keys[pygame.K_LEFT]:
            self.left(sprites)
        if keys[pygame.K_UP]:
            self.up(sprites)
        if keys[pygame.K_DOWN]:
            self.down(sprites)

    def right(self, sprites):
        for s in sprites:
            if s is not self:
                drawScreen(screen, sprites)
                #print("before: ", s.rect.x)
                s.rect.center = (s.rect.center[0] - VELOCITY, s.rect.center[1])
                #print("after: ", s.rect.x)

    def left(self, sprites):
        for s in sprites:
            if s is not self:
                drawScreen(screen, sprites)
                #print("before: ", s.rect.x)
                s.rect.center = (s.rect.center[0] + VELOCITY, s.rect.center[1])
                #print("after: ", s.rect.x)

    def up(self, sprites):
        for s in sprites:
            if s is not self:
                drawScreen(screen, sprites)
                #print("before: ", s.rect.x)
                s.rect.y += VELOCITY
                #print("after: ", s.rect.x)

    def down(self, sprites):
        for s in sprites:
            if s is not self:
                drawScreen(screen, sprites)
                #print("before: ", s.rect.x)
                s.rect.y -= VELOCITY
                #print("after: ", s.rect.x)

    def recv(self, client):
        r = recvFromServer()
        r.start()
        data = r.recv(client)
        print("got from server: ", data)

class recvFromServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self, client):
       return client.recv(1024).decode()

def drawScreen(screen, sprites):

    screen.fill((2, 255, 255))
    pygame.display.flip()
    sprites.draw(screen)
    pygame.display.flip()
    # pygame.draw.circle(screen, RED, (50,50), 10)
    # pygame.display.flip()


def compare_lists(l1, l2):
    for i in l1:
        for j in l2:
            if i == j:
                return True
    return False

def create_loc_list(loc, len):
    lst = []
    for i in range(0, len):
        lst.append(loc+i)
    return lst

def main(screen, client):
    run = True

    clock = pygame.time.Clock()

    paint = True
    sprites = pygame.sprite.Group()
    # wrappers = pygame.sprite.Group()
    p = Player(PURPLE, (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
    p1 = Player(RED, (WINDOW_WIDTH / 3, WINDOW_HEIGHT / 3))

    sprites.add(p)
    sprites.add(p1)
    # wrappers.add(Rect(p.rect.x+1, p.rect.y + 1, p.image.get_width() + 2, p.image.get_height()))
    # wrappers.add(Rect(p1.rect.x + 1, p1.rect.y + 1, p1.image.get_width() + 2, p1.image.get_height()))
    while run:
        #data = client.recv(1024).decode()
        print("server sent: ", data)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                # pygame.quit()
        clock.tick(30)
        #sprites.update()
        #print("sprites: ", p1.rect.x)
        sprites.draw(screen)
        pygame.display.flip()
        p.move(sprites)
        #p.recv(client)

        # myX = create_loc_list(p.x, 50)
        # myY = create_loc_list(p.y, 50)
        # # redRawWindow(screen, p)
        # if not compare_lists(xList, myX) or not compare_lists(yList, myY) and paint == True:
        #     pygame.draw.rect(screen, RED, (x1, y1, 50, 50))
        #     pygame.display.flip()
        # else:
        #     paint = False

#if p.x not in xList or p.y not in yList and paint == True:
if __name__ == '__main__':
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((IP, PORT))
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Client")
    screen.fill((2, 255, 255))
    pygame.display.flip()
    data = my_socket.recv(1024).decode()
    print("from server: ", data)
    # if "location" in data:
    #     x = data.index("X")
    #     endX = data.index(",")
    #     xLoc = int(data[x + 4:endX])
    #     y = data.index("Y")
    #     yLoc = int(data[y+4:])
    #     print("x: ", data[x+4:endX], "y: ", data[y+4:])

    #main(screen, my_socket)
    p = Player(RED, (50, 50))
    main(screen, my_socket)
