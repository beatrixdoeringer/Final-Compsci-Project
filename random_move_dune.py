import math
import pygame
import pygame.locals
import sys
import random
#convert to be an import
width, height = 1000, 750
screen = pygame.display.set_mode((width, height))
wave_width = screen.get_width() // 5


class Dune:
    def __init__(self, dune_height: float, horizontal_dis: float,order:int):
        self.dune_height = dune_height
        self.horizontal_dis = horizontal_dis

        self.points = []
        d = screen.get_height() - self.dune_height
        for x in range(wave_width):
            
            theta = ((-2*x)) * math.pi / wave_width
           
            self.points.append(((x+(order*wave_width)), self.dune_height * math.sin(theta) + d))

    def display(self):
        pygame.draw.lines(screen, (255, 0, 0), False, self.points,2)
    def movement(self,movepos:float):
        for i in range(len(self.points)):
            update=list(self.points[i])
            update[0]-=movepos
        
            self.points[i]=tuple(update)







def main():
    width, height = 1000, 500
    screen = pygame.display.set_mode((width, height))
    fps = 60
    fps_clock = pygame.time.Clock()

    off_left = Dune(random.randrange(40, 100),wave_width,-1)
    first = Dune(random.randrange(40, 100),wave_width,0)
    second = Dune(random.randrange(40, 100), wave_width,1)
    third = Dune(random.randrange(40, 100), wave_width,2)
    fourth = Dune(random.randrange(40, 100), wave_width,3)
    fifth = Dune(random.randrange(40, 100), wave_width,4)
    off_right = Dune(random.randrange(40, 100),wave_width,5)
    current_dunes: list[Dune] = [
        off_left,
        first,
        second,
        third,
        fourth,
        fifth,
        off_right,
    ]

    while True:
        screen.fill("#000000")
        for dune in current_dunes:
            dune.movement(2)
            dune.display()
        if current_dunes[0].points[-1][0] < 0:
            current_dunes.pop(0)
            current_dunes.append(Dune(random.randrange(40, 100), wave_width, 5))

        # actual code
        # next session reminders: The code is broken, it seems to get a very limited amount of points for each sin wave, and the process for displacing them is messed up.

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()
        fps_clock.tick(fps)
        

if __name__ == "__main__":
    main()
    
