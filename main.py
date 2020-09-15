import pygame
from Species import Species
from math import hypot


WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI mover")
clock = pygame.time.Clock()


species = Species(10)

target = (0.1, 0.9)

def calculate_fitness(agent):
    return 1 / (hypot(agent.x-target[0], agent.y-target[1]) ** 2)


running = True
while running:

    screen.fill((255, 255, 255))
    # drawing
    species.update(screen)
    pygame.draw.circle(screen, (0, 0, 0), (int(target[0] * WIDTH), int(target[1] * HEIGHT)), 10)
    # end drawing
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
            elif event.key == pygame.K_SPACE:
                species.next_generation(calculate_fitness, 1/10, 0.3)
pygame.quit()
