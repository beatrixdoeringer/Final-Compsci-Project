import pygame
import random
import sys
import math


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

BANANA_SPEED_Y = 200      
SPAWN_INTERVAL = 2000    
BANANAS_PER_BATCH = (1, 3)  
SPAWN_ZONE_WIDTH = 500      

def make_banana_surface(width, height, color=(255, 255, 0)):

    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    pts = []
    for i in range(20):
        t = i / 19
        x = t * width
        curve = math.sin(t * math.pi) * (height * 0.3)
        top_y = height * 0.3 + curve
        bot_y = height * 0.7 + curve
        pts.append((x, top_y))
    for i in range(19, -1, -1):
        t = i / 19
        x = t * width
        curve = math.sin(t * math.pi) * (height * 0.3)
        bot_y = height * 0.7 + curve
        top_y = height * 0.3 + curve
        pts.append((x, bot_y))
    pygame.draw.polygon(surf, color, pts)
    stem_rect = pygame.Rect(0, height * 0.25, width * 0.1, height * 0.1)
    stem_rect.centerx = width - stem_rect.width // 2
    stem_rect.y -= height * 0.1
    pygame.draw.rect(surf, (139, 69, 19), stem_rect)
    return surf

class Banana:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SPAWN_ZONE_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.vy = BANANA_SPEED_Y
        self.landed = False

    def update(self, dt, landed_rects):
        if not self.landed:
            self.rect.y += self.vy * dt
            if self.rect.bottom >= SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT
                self.landed = True
                landed_rects.append(self.rect.copy())
            else:
                for other in landed_rects:
                    if self.rect.colliderect(other):
                        self.rect.bottom = other.top
                        self.landed = True
                        landed_rects.append(self.rect.copy())
                        break

    def draw(self, surface):
        surface.blit(self.image, self.rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()


    banana_img = make_banana_surface(60, 30)

    bananas = []
    landed_rects = []

    SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_EVENT, SPAWN_INTERVAL)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == SPAWN_EVENT:
                for _ in range(random.randint(*BANANAS_PER_BATCH)):
                    bananas.append(Banana(banana_img))

        for b in bananas:
            b.update(dt, landed_rects)

        screen.fill((30, 30, 30))
        for b in bananas:
            b.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()