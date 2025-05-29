import math
import pygame
import pygame.locals
import sys


class Dunes:

    def __init__(self, surface: pygame.Surface, dune_height: float, dune_width: float):
        self.surface = surface
        self.dune_height = dune_height
        self.dune_width = dune_width
        self.k = 0.5 * dune_height + 300
        self.h = 20
        self.offset = 0
        self.speed = 0
        self.acceleration = 200
        
    def update(self):
        self.speed += self.acceleration * 1/60
        self.offset += self.speed * 1/60

    def get_height_at(self, x: float) -> float:
        input_x = x + self.offset
        return self.dune_height * math.sin((input_x - self.h) / self.dune_width) + self.k
    
    def get_velocity_at(self, x: float) -> float:
        input_x = x + self.offset
        return self.dune_height * self.speed / self.dune_width * math.cos((input_x - self.h) / self.dune_width)

    def get_acceleration_at(self, x: float) -> float:
        input_x = x + self.offset
        return -self.dune_height * self.speed ** 2 / self.dune_width ** 2 * math.sin((input_x - self.h) / self.dune_width) + self.dune_height * self.acceleration / self.dune_width * math.cos((input_x - self.h) / self.dune_width)

    def draw(self):
        width = self.surface.get_width()
        x_values = []
        y_values = []

        for x in range(width):
            input_x = x + self.offset
            y = self.dune_height * math.sin((input_x - self.h) / self.dune_width) + self.k
            x_values.append(x)
            y_values.append(y)

        points = list(zip(x_values, y_values))
        pygame.draw.lines(self.surface, (255, 255, 0), False, points, 10)

class Ball:
    def __init__(self, x, y, radius=20):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = 0
        self.vy = 0
        self.gravity = 800
        # self.jump_strength = -15
        # self.jump_speed = 8
        self.in_air = False
        self.in_air_time = 0.0
        self.in_air_v0 = 0.0
        self.in_air_y0 = 0.0 

    def update(self, dune_y, dune_v, dune_a, is_diving):
        if self.in_air:
            self.in_air_time += 1/60
            if is_diving:
                self.vy += self.gravity * 2
            else:
                self.vy += self.gravity
            
            self.y = self.in_air_y0 + self.in_air_v0 * self.in_air_time + 0.5 * self.gravity*self.in_air_time ** 2
            self.x += self.vx

            terrain_y = dune_y(self.x) - self.radius*0
            if self.y >= terrain_y - self.radius*0:
                self.y = terrain_y - self.radius*0
                self.vx = 0
                self.vy = 0
                self.in_air = False
        
        else:
            if dune_a(self.x) > self.gravity:
                self.in_air = True
                self.in_air_time = 0 #acceleration is more neg (greater) than gravity then switch state to in air
                self.in_air_v0 = dune_v(self.x)
                self.vy = self.in_air_v0
                self.in_air_y0 = dune_y(self.x-self.radius*0)
            
            else:
                self.y = dune_y(self.x)


    # def jump(self, dune, h):
    #     if not self.in_air:
    #         screen_x = self.x
    #         x = screen_x + dune.offset
    #         slope = (dune.dune_height / dune.dune_width) * math.cos((x - h) / dune.dune_width)

    #         dx = 1
    #         dy = slope
    #         magnitude = math.sqrt(dx**2 + dy**2)
    #         dx /= magnitude
    #         dy /= magnitude

    #         speed = self.jump_speed
    #         self.vx = speed * dx
    #         self.vy = -speed * dy  

    #         self.in_air = True

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), self.radius)

def main():
    pygame.init()
    fps = 60
    fps_clock = pygame.time.Clock()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))

    keys_held: set[int] = set()
    dune = Dunes(screen, dune_height=100, dune_width=50)
    
    ball = Ball(x=width // 2, y=300)

    while True:
        screen.fill((0, 0, 0))
        dune.draw()

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                keys_held.add(event.key)
            elif event.type == pygame.KEYUP:
                keys_held.discard(event.key)
                #if event.key == pygame.K_SPACE:
                    #ball.jump(dune, dune.h)

        if pygame.K_SPACE in keys_held:
            dune.update()

        else:
            dune.speed = 100
            dune.update()
        
        is_diving = pygame.K_SPACE in keys_held
        ball.update(lambda x: dune.get_height_at(x), lambda x: dune.get_velocity_at(x), lambda x: dune.get_acceleration_at(x), is_diving) #lamba x: dune.get_acceleration_at(x),
        
        ball.draw(screen)

        pygame.display.flip()
        fps_clock.tick(fps)

if __name__ == "__main__":
    main()
    
    #make player lose when it hits dune at pos slope
    #make the ball not go higher when you just hold down the space bar
    #add scoring to the game (based on how high you go)
    #add states to start playing the game and ending the game
    
