#(c) 2012 metamaquina.com.br Licensed under GPLv3 or later
import serial
import pygame
import copy
from pygame.locals import *
from math import sqrt
from random import random
from time import gmtime, strftime
x = 100
y = 100

screen = pygame.display.set_mode([x * 3, y * 3 + 100])
pygame.font.init()

omega = 0.5
water = [[0.0 for j in range(y)] for i in range(x)]
nwater = [[0.0 for j in range(y)] for i in range(x)]
sqrt2 = sqrt(2)

ser = serial.Serial('/dev/ttyACM0', 9600, timeout = 0.00)
font = pygame.font.Font(None, 20)
text = font.render("No Data", True, (255,0, 0))
textRect = text.get_rect()
x_graph = 0
rain_data = []
frame = 1 
last_mean = 0
rain_screen = screen.subsurface(pygame.Rect(0, 0, 300, 300))
graph_screen = screen.subsurface(pygame.Rect(0, 300, 300, 100))

log = open("Log.csv", 'w')

def draw_drops(screen):
    global water, nwater
    for k in range(0, x - 1):
        for j in range(0, y - 1):
            nwater[k][j] =  -water[k][j] * 0.3 + (water[k + 1][j] + water[k - 1][j] + water[k][j + 1] + water[k][j - 1] + (water[k + 1][j + 1] + water[k - 1][j + 1] + water[k - 1][j - 1] + water[k + 1][j - 1]) / sqrt2) / 4.0 * 0.6
            r = nwater[k][j] * 255
            g = 0
            if r > 255: r = 255
            if r < 0:
                g = -r
                r = 0
            if g > 255: g = 255
            if(r > 1 or g > 1):
                pygame.draw.rect(screen, (g, g, r + g), ((k * 3, j * 3), (3, 3)))
    water = copy.deepcopy(nwater)

def process_serial(ser):
    global text, textRect, water, rain_data
    data = ser.readline()
    if len(data) > 3:
        text = font.render(data[:-2], True, (120,0, 255))
        textRect = text.get_rect()
        textRect.centery = 290
        water[int(random() * x)][int(random() * y)] = 2000
        parsed_data = data.split(' ')
        if len(parsed_data) > 1 and len(parsed_data[0]):
            print parsed_data
            rain_data.append(float(parsed_data[0]))
    screen.blit(text, textRect)
    
def update_screen(screen):
    pygame.display.flip()
    screen.fill((0,0,0))
    
while 1:
    draw_drops(screen)
    process_serial(ser)
    update_screen(rain_screen)
    frame += 1
    if frame % 20 == 0:
        if rain_data:
            mean = sum(rain_data) / float(len(rain_data))
        else:
            mean = 0
        rain_data = []
        pygame.draw.line(graph_screen, (0, 255, 0), (frame / 20, 100 - last_mean), (frame / 20 + 1, 100 - mean))
        print mean
        log.write("%d\n" % mean + "," + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))
        last_mean = mean
