import queue
import pygame
import math
# get str return tuple:
def calc_distanse(loc1, loc2):
    x = math.pow((loc1[0] - loc2[0]), 2)
    y = math.pow((loc1[1] - loc2[1]), 2)
    return math.sqrt(x + y)
def main():
    dis = calc_distanse((34,56), (67,100))
    print("dis = ", dis)
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Client")
    screen.fill((2, 255, 255))
    pygame.display.flip()
    finish = False
    while not finish:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
        #pygame.draw.rect(screen, (0,0,0), re)
        pygame.display.flip()
def toTuple(st: str):
    start = st.find("(")
    end = st.find(",")
    #print(st[start+1:end])
    e = st.find(",", end+1)
    en = st.find(")")
    #print(st[end + 1:e], ", ", len(st[start+1:end]))
    return int(st[start+1:end]), (int(st[end+3:e]), int(st[e+1:en]))
def create_pos(st:str):
    start = st.find("(")
    end = st.find(",")
    en = st.find(")")
    return (int(st[start+1:end]), int(st[end+1:en]))

def findNumOfSubServer(st: str):
    i = st.find("server")
    l = len("server")
    return int(st[i+l:])

#make tuple from big tuple
def rateTuples(bigTuple :str):
    s = bigTuple.find("(")
    m = bigTuple.find(",")
    e = bigTuple.find(")0")
    smallTuple1 = (int(bigTuple[s+2:m]), int(bigTuple[m+1:e]))
    s = bigTuple.find("(",e)
    m = bigTuple.find(",",s)
    e = bigTuple.find(")",m)
    smallTuple2 = (int(bigTuple[s+1:m]), int(bigTuple[m+1:e]))
    return smallTuple1, smallTuple2


if __name__ == '__main__':
    loc1, loc2 = rateTuples('((1200,600),(0,600))')



