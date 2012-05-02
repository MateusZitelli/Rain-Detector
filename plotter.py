import serial
import pygame
from pygame.locals import *
ser = serial.Serial('/dev/ttyACM0', 9600)

screen = pygame.display.set_mode([1000, 500])
i = 0
def grid(screen):
    screen.fill((0,0,0))
    for i in range(0, 1000, 25):
        if(i % 25 == 0): w = 1
        if(i % 50 == 0): w = 2
        if(i % 250 == 0): w = 3
        if(i % 500 == 0): w = 4
        pygame.draw.line(screen, (100, 100, 100), (i, 0), (i , 500), w)

    for j in range(0, 500, 25):
        if(j % 25 == 0): w = 1
        if(j % 50 == 0): w = 2
        if(j % 250 == 0): w = 3
        pygame.draw.line(screen, (100, 100, 100), (0, j), (1000 , j), w)
last = 0
high = 0
probes = [1, 1]
j = 0
to_render = 0
while 1:
    if(i % (1000 * 2) == 0):
        grid(screen)
        print float(probes[0]) / probes[1]
        probes = [1, 1]
    #j = 250 - (float(ser.readline()[:-1].split('\r')[0]) / 1024.0 * 500 - 400) * 3
    try:
        j = 250 - (float(ser.readline()[:-1].split('\r')[0]) / 1024.0 * 500 - 380) * 10
        to_render = 1
    except:
        to_render = 0
    if to_render:
        if j < 200 and not high:
            pygame.draw.circle(screen, (255, 0, 0), (i / 2 % 1000, int(j)), 3)
            high = 1
        elif j > 200 and high:
            high = 0
        pygame.draw.line(screen, (0, 255, 0), (i / 2 % 1000, last), (i / 2 % 1000, j))
        pygame.display.flip()
        i += 1
        last = j
        if high:
            probes[0] += 1
        else:
            probes[1] += 1
