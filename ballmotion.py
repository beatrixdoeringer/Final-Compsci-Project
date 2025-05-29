import sys

import pygame
import pygame.locals

class Player:

    def __init__(self, surface: pygame.Surface, x: float, y: float) -> None:
        self.surface = surface
        self.x = 250
        self.y = y
        self.vy = 0
        self.ay = 0.1
        self.on_slope = False

        self.line_start = (500, 20)
        self.line_end = (30, 350)
        self. slope = (self.line_end[1] - self. line_start[1]) / (self.line_end[0] - self.line_start[0])
        self.intercept = self.line_start[1] - self.slope * self.line_start[0]
        
    def move(self) -> None:
        line_y = self.slope * self.x + self.intercept
        if not self.on_slope and abs((self.y + 30) - line_y) < 5 and self.vy > 0:
            self.on_slope = True
            self.vy = 0

        if self.on_slope:
            dx = 2
            dy = self.slope * dx
            
            if self.slope < 0 and dy < 0:
                dx = -dx
                dy = -dy
            elif self.slope > 0 and dy < 0:
                dx = -dx
                dy = -dy
            
            self.x += dx
            self.y += dy
        
        else:
            self.vy += self.ay
            self.y += self.vy


    def display(self) -> None:
        pygame.draw.circle(self.surface, "#ff0000", (self.x, self.y), 30)
        pygame.draw.line(self.surface, "#ff0000", self.line_start, self.line_end, 5)


def main():
    fps = 60
    fps_clock = pygame.time.Clock()
    width, height = 500, 500
    screen = pygame.display.set_mode((width, height))

    p = Player(screen, width/2, 30)

    while True:
        screen.fill("#000000")

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    p.vy = -5
                

        p.move()
        p.display()
        

        pygame.display.flip()
        fps_clock.tick(fps)


if __name__ == "__main__": 
    main()