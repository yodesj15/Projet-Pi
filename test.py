import pygame
import PyLidar3
from math import cos, sin, pi
import sys


port =  "/dev/ttyUSB0" #windows
lidar = PyLidar3.YdLidarX4(port) 
if not lidar.Connect():
    sys.exit(1)


WIDTH = 720
HEIGHT = 480

pygame.init()

pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LIDAR")

scan = lidar.StartScanning()

screen = pygame.display.get_surface()
running = True
while running:
    screen.fill((33, 33, 33))

    
    scope = pygame.Surface((WIDTH, HEIGHT))
    scope.fill((33, 33, 33))

    data = next(scan)
    maxKey = max(data, key=data.get)
    maxValue = data[maxKey]
    for angle in data.keys():
        distRelative = data[angle] / maxValue
        dist = (HEIGHT / 2) * distRelative
        angleRad = angle * pi / 180
        pygame.draw.line(scope, (255, 0, 0), (round(WIDTH/2), round(HEIGHT/2)), (round(WIDTH/2 + dist*cos(angleRad)), round(HEIGHT / 2 + dist*sin(angleRad))), 3)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(scope, (0, 0)) # Cet appel permet d'afficher la surface scope sur la surface screen et donc sur la fenêtre
    pygame.display.update()

pygame.quit()
