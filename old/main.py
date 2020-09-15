import sklearn
import pygame
import csv
from Car import Car


WIDTH = 500
HEIGHT = 500
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Genetic algorithm drives a car")
pygame.key.set_repeat(100, 50)
clock = pygame.time.Clock()

car = Car(WIDTH/2, HEIGHT/2, 50, 25)
turning_cw = turning_ccw = moving = False


running = True
while running:
    screen.fill((255, 255, 255))
    if turning_cw: car.rotate_cw()
    if turning_ccw: car.rotate_ccw()
    if moving: car.move()
    car.update(screen)
    pygame.display.flip()
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                break
            elif event.key == pygame.K_UP:
                moving = True
            elif event.key == pygame.K_LEFT:
                turning_cw = True
            elif event.key == pygame.K_RIGHT:
                turning_ccw = True
        elif event.type  == pygame.KEYUP:
            if event.key == pygame.K_UP:
                moving = False
            elif event.key == pygame.K_LEFT:
                turning_cw = False
            elif event.key == pygame.K_RIGHT:
                turning_ccw = False
        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            
pygame.quit()
