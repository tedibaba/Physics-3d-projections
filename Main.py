from Cube import Cube
import pygame
import sys
import time

pygame.init()
screen = pygame.display.set_mode((1000, 1000))

running = True
cube = Cube(30, 30,30,[[500],[500],[100]], 100)
colors = [(255,0,0), (0,255,0), (0,0,255), (255,128,0), (255,255,0), (0,204,204)]

while running:
    screen.fill((0,0,0))

    points = cube.transform_points()

         
    for j,face in enumerate(cube.faces):
        coords = [points[i] for i in face]
        print(coords)
        pygame.draw.polygon(screen, colors[j], coords)
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    
    time.sleep(0.5)

pygame.quit()
sys.exit()
