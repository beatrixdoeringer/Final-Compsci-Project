import math
import pygame
import pygame.locals
import sys
import random



def dune_generation(surface: pygame.Surface,dune_height:float,dune_width:float):
   
    k = 1 / 2 * dune_height+300
    h = 20
    x_values: list[float] = []
    y_values: list[float] = []
    for x in range(1, surface.get_width()):  # until the sine wave returns to 0
        x_values.append(x)
        y_values.append(dune_height * math.sin((x - h) / dune_width) + k)
    points = list(zip(x_values, y_values))
    pygame.draw.lines(surface, (255, 255, 0), False, points, 10)
    dune_height, dune_width = (random.randrange(100,110),random.randrange(50,55))


def main():
    plane = 0
    width, height = 1000, 500
    screen = pygame.display.set_mode((width, height))
    fps = 60
    fps_clock = pygame.time.Clock()
    while True:

        screen.fill("#000000")

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()

        dune_generation(screen,75,45)

        pygame.display.flip()
        fps_clock.tick(fps)

if __name__ == "__main__":
    main()