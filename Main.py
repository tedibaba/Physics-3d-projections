import random
from ManualCube import ManualCube
from Cube import Cube
import pygame
import sys


pygame.init()
screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()
running = True
# cube = Cube(1, 1,1,[[500],[500],[300]], 100, (0,0, 1))
colors = [(255,0,0), (0,255,0), (0,0,255), (255,128,0), (255,255,0), (0,204,204), (255,0,0)]

#Overlapping colors cause color issues
cubes = []
cube = ManualCube(1, 1,1,[[500],[500],[300]], 100, (0,0,1))
cubes.append(cube)

while running:
    screen.fill((0,0,0))

    for cube in cubes:
        points = cube.transform_points()
            
        for j,face in cube.visible_faces():
            coords = [points[i] for i in face]
            # print(coords, face)
            pygame.draw.polygon(screen, colors[j], coords)
            for k in range(4):
                pygame.draw.circle(screen, (255,0,0), coords[k], 10)
        
        
    pygame.display.update()

    # cube.change_rotation_values(0.01)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and cube.manual_rotatable:
            cube_to_change = cubes[random.randint(0, len(cubes) - 1)]
            if event.key == pygame.K_q:
                cube_to_change.theta_z -= 0.01
            if event.key == pygame.K_w:
                cube_to_change.theta_y += 0.01
            if event.key == pygame.K_e:
                cube_to_change.theta_z += 0.01
            if event.key == pygame.K_a:
                cube_to_change.theta_x -= 0.01
            if event.key == pygame.K_s:
                cube_to_change.theta_y -= 0.01
            if event.key == pygame.K_d:
                cube_to_change.theta_x += 0.01
        if event.type == pygame.MOUSEBUTTONUP:
            orig_pos = pygame.mouse.get_pos()
            cubes.append(ManualCube(1, 1,1,[[orig_pos[0]],[orig_pos[1]],[300]], 100, (0,0,1)))


    
    clock.tick(60)
 
pygame.quit()
sys.exit()
