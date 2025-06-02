import math
import pygame
import sys
import pygame.locals
import random_move_dune

class Enemy:
    def __init__(self,range_mot:int,horizontal_pos:int,pos:tuple[int,int]):
        self.horizontal_pos=horizontal_pos
        self.range_mot=range_mot
        self.pos=pos
    def destroyplayer(self,playerpos:tuple[int,int])->bool:
        if (self.pos[0]<playerpos[0] and playerpos[0]<self.pos[0]+30) and (self.pos[1]<playerpos[1] and playerpos[1]<self.pos[1]+30):
            return True
        else:
            return False
    def movement(self,surface,going,go)->tuple[int,bool]:
        
        if go:    
            going-=1
        else:
            going+=1
        if going>=self.range_mot:
            go=False
        if going<=0:
            go=True
        rectvalues=[self.pos[0],self.pos[1]+going,30,60]
        pygame.draw.rect(surface,(255,0,0),(rectvalues))
        done=(going,go)
        return done

def main():
    width, height = 1000, 500
    screen = pygame.display.set_mode((width, height))
    fps = 60
    fps_clock = pygame.time.Clock()
    going=0
    go=False
    while True:
        screen.fill((0,0,0))
        jerry=Enemy(40,500,(500,100))
        going,go=jerry.movement(screen,going,go)
        
        


        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()
        fps_clock.tick(fps)
if __name__ == "__main__":
    main()