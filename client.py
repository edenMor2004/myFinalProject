import socket
import pygame
import random

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
REFRESH_RATE = 40
LEFT = 1
SCROLL = 2
RIGHT = 3
VELOCITY = 10

clientNumber = 0

class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.sx = 0
        self.sy = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        # if keys[pygame.K_UP]:
        #     self.sy += VELOCITY
        # if keys[pygame.K_DOWN]:
        #     self.sy -= VELOCITY
        # if keys[pygame.K_RIGHT]:
        #     self.sx -= VELOCITY
        # if keys[pygame.K_LEFT]:
        #     self.sx += VELOCITY
        if keys[pygame.K_UP]:
            self.y -= VELOCITY
        if keys[pygame.K_DOWN]:
            self.y += VELOCITY
        if keys[pygame.K_RIGHT]:
            self.x += VELOCITY
        if keys[pygame.K_LEFT]:
             self.x -= VELOCITY

        # if self.x > (WINDOW_WIDTH - self.width):
        #     self.x -= VELOCITY
        # if self.x < 0:
        #     self.x += VELOCITY
        # if self.y > (WINDOW_HEIGHT - self.height):
        #     self.y -= VELOCITY
        # if self.y < 0:
        #     self.y += VELOCITY
        self.rect = (self.x, self.y, self.width, self.height)
        # self.draw(screen)
        #
        # if self.sy < -100:
        #     self.sy = -100
        # #if self.sy < 0:
        #    # self.sy = 0
        # if self.sx < -100:#MAX_X:
        #     self.sx = -100
        # if self.sx > 0:
        #    self.sx = 0
        #
        # print("sx: ", self.sx)
        # print("sy: ", self.sy)
        # img = pygame.image.load(IMAGE)
        # screen.blit(img, (self.sx, self.sy))

def redRawWindow(screen, player):
    # img = pygame.image.load(IMAGE)
    # screen.blit(img, (0, 0))
    img = pygame.image.load(IMAGE)
    screen.blit(img, (0, 0))
    player.draw(screen)
    pygame.display.flip()

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

def main(x, y):
    run = True
    p = Player(x, y, 50, 50, (0, 255, 0))
    clock = pygame.time.Clock()
    x1 = random.randint(0, WINDOW_WIDTH)
    y1 = random.randint(0, WINDOW_HEIGHT)
    print("x1 = ", x1, "y1 = ", y1)
    # pygame.draw.rect(screen, RED, (x1, y1, 50, 50))
    xList = create_loc_list(x1, 50)
    yList = create_loc_list(y1, 50)
    # pygame.display.flip()
    paint = True
    while run:
        # if not paint:
        #     x1 = random.randint(0, (WINDOW_WIDTH - 50))
        #     y1 = random.randint(0, WINDOW_HEIGHT - 50)
        #     print("x1 = ", x1, "y1 = ", y1)
        #     pygame.draw.rect(screen, RED, (x1, y1, 50, 50))
        #     xList = create_loc_list(x1, 50)
        #     yList = create_loc_list(y1, 50)
        #     pygame.display.flip()
        #     paint = True

        print("self: x = ", p.x, "y = ", p.y)
        for evevt in pygame.event.get():
            if evevt.type == pygame.QUIT:
                run = False
                # pygame.quit()
        clock.tick(20)
        # p.draw(screen)
        # pygame.display.flip()
        p.move()
        myX = create_loc_list(p.x, 50)
        myY = create_loc_list(p.y, 50)
        redRawWindow(screen, p)
        if not compare_lists(xList, myX) or not compare_lists(yList, myY) and paint == True:
            pygame.draw.rect(screen, RED, (x1, y1, 50, 50))
            pygame.display.flip()
        else:
            paint = False

#if p.x not in xList or p.y not in yList and paint == True:
if __name__ == '__main__':
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((IP, PORT))
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Client")
    data = my_socket.recv(1024).decode()
    print("from server: ", data)
    if "location" in data:
        x = data.index("X")
        endX = data.index(",")
        xLoc = int(data[x + 4:endX])
        y = data.index("Y")
        yLoc = int(data[y+4:])
        print("x: ", data[x+4:endX], "y: ", data[y+4:])
    main(xLoc, yLoc)
