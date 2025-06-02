import math
import pygame
import pygame.locals
import sys
import random

pygame.init()
width, height = 1000, 750
screen = pygame.display.set_mode((width, height))
fps = 60
fps_clock = pygame.time.Clock()
wave_width = screen.get_width() // 3.2

class Dune:
    def __init__(self, dune_height: float, start_x: float, start_y: float, wave_width: int, num_points: int = 150):
        self.dune_height = dune_height
        self.wave_width = wave_width
        self.speed = 2
        self.points = []
        
        
        self.phase_offset = math.asin(max(-1, min(1, (start_y - (height - dune_height)) / dune_height)))

        for i in range(num_points + 1):
            x = start_x + i * (wave_width / num_points) #so that the dunes line up
            theta = (2 * math.pi * (x - start_x) / wave_width) + self.phase_offset
            y = dune_height * math.sin(theta) + (height - dune_height)
            self.points.append([x, y])


    def movement(self):
        for point in self.points:
            point[0] -= self.speed

    def display(self, screen):
        pygame.draw.lines(screen, (255, 0, 0), False, self.points, 5)

    def get_end_point(self):
        return self.points[-1] #need this to make end points to match up



def create_connected_dune(previous_dune):
    last_x, last_y = previous_dune.get_end_point()
    new_height = random.randrange(60, 140)
    return Dune(dune_height=new_height, start_x=last_x, start_y=last_y, wave_width=wave_width)



def main():

    dunes = []
    first = Dune(random.randrange(60, 140), 0, height - 80, wave_width)
    dunes.append(first)

    for i in range(6):
        dunes.append(create_connected_dune(dunes[-1])) #make a loop instead of doing 6 different orders

    while True:  
        screen.fill((0,0,0))

        for dune in dunes:
            dune.movement()
            dune.display(screen)

        if dunes[0].get_end_point()[0] < 0:
            dunes.pop(0)
            dunes.append(create_connected_dune(dunes[-1]))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        pygame.display.flip()
        fps_clock.tick(fps)
        

if __name__ == "__main__":
    main()
    