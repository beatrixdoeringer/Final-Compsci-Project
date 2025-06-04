import math
import pygame
import pygame.locals
import sys
import random

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
fps = 60
fps_clock = pygame.time.Clock()
wave_width = screen.get_width() // 2.6

class Intro_dunes:
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
        pygame.draw.lines(screen, (255, 230, 129), False, self.points, 5)
        filled_points = self.points.copy()
    
        filled_points.append([self.points[-1][0], height])  
        filled_points.append([self.points[0][0], height])   

        pygame.draw.polygon(screen, (255, 230, 129), filled_points)


    def get_end_point(self):
        return self.points[-1] 

def create_connected_dune(previous_dune):
    last_x, last_y = previous_dune.get_end_point()
    new_height = random.randrange(60, 140)
    return Intro_dunes(dune_height=new_height, start_x=last_x, start_y=last_y, wave_width=wave_width)

class Dunes:

    def __init__(self, surface: pygame.Surface, dune_height: float, dune_width: float):
        self.surface = surface
        self.dune_height = dune_height
        self.dune_width = dune_width
        self.k = 0.5 * dune_height + 450
        self.h = 20
        self.offset = 0
        self.speed = 0
        self.acceleration = 5

        # self.points = []
        # d = surface.get_height() - self.dune_height
        # for x in range(dune_width):
        #     theta = (((-2*x)) * math.pi - math.pi/8) / dune_width         
        #     self.points.append(((x+(order*dune_width)), self.dune_height * math.sin(theta) + d))
        
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
        height = self.surface.get_height()
        x_values = []
        y_values = []

        for x in range(width):
            input_x = x + self.offset
            y = self.dune_height * math.sin((input_x - self.h) / self.dune_width) + self.k
            x_values.append(x)
            y_values.append(y)

        points = list(zip(x_values, y_values))
        dune_bottom = points + [(width - 1, height), (0, height)]
        pygame.draw.polygon(self.surface, (255, 230, 129), dune_bottom)
        pygame.draw.lines(self.surface, (255, 230, 129), False, points, 10)

    def reset(self):
        self.offset = 0
        self.speed = 0
        self.acceleration = 200

class Ball:
    def __init__(self, x, y, radius=15):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = 0
        self.vy = 0
        self.gravity = 1000
        self.in_air = False
        self.in_air_time = 0.0
        self.in_air_v0 = 0.0
        self.in_air_y0 = 0.0 
        self.crash = False
        self.reached_peak = False
        self.gravity_multiplier_diving = 1.0
        self.gravity_multiplier_screen = 1.0
        self.vy_multiplier = 1.0

    def update(self, dune_y, dune_v, dune_a):
        if self.in_air:
            self.in_air_time += 1/60

            # if self.y < 0:
            #     self.gravity_multiplier_screen = 10

            # if self.y < 100:
            #     self.gravity_multiplier_screen = 200/abs(self.y + 100)

            # else:
            #     self.gravity_multiplier_screen = 1.0
            
            if self.y < 100 and self.vy < 0:
                self.vy_multiplier = abs(self.y/100)
            
            else:
                self.vy_multiplier = 1.0
            
            #self.vy = dune_v(self.x)
            #self.y = self.in_air_y0 + self.in_air_v0 * self.in_air_time + 0.5 * self.gravity*self.gravity_multiplier*self.in_air_time ** 2
            self.vy += self.gravity*self.gravity_multiplier_diving*self.gravity_multiplier_screen/60
            self.vy *= self.vy_multiplier
            self.y += self.vy/60
            self.x += self.vx/60

            terrain_y = dune_y(self.x)
            if self.y > terrain_y + self.radius:
                if dune_v(self.x) < -10 and self.in_air_time > 0.9 and self.vy > 10:
                    self.y = terrain_y
                    self.vx = 0
                    self.vy = 0
                    self.in_air = False
                    self.crash = True
                else:
                    self.y = terrain_y
                    self.vx = 0
                    self.vy = 0
                    self.in_air = False
        
        else:
            if dune_a(self.x) > self.gravity:
                self.in_air = True
                self.in_air_time = 0
                self.in_air_v0 = dune_v(self.x)
                self.vy = self.in_air_v0
                self.in_air_y0 = dune_y(self.x)
                self.gravity_multiplier_diving = 1.0
                self.gravity_multiplier_screen = 1.0
            
            else:
                self.y = dune_y(self.x)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.radius)

    def reset(self):
        self.vx = 0
        self.vy = 0
        self.gravity = 1000
        self.in_air = False
        self.in_air_time = 0.0
        self.in_air_v0 = 0.0
        self.in_air_y0 = 0.0 
        self.crash = False
        self.reached_peak = False
        self.gravity_multiplier_diving = 1.0
        self.gravity_multiplier_screen = 1.0
        self.vy_multiplier = 1.0


def main():
    pygame.init()
    fps = 60
    fps_clock = pygame.time.Clock()
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    # width, height = screen.get_size()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))

    keys_held: set[int] = set()
    dune = Dunes(screen, dune_height=70, dune_width=40)
    
    ball = Ball(x=width // 2, y=300)

    score = 0
    score_increment = 10
    menu = True
    playing = False
    game_over = False

    idunes = []
    first = Intro_dunes(random.randrange(20, 100), 0, height - 80, wave_width)
    idunes.append(first)

    for i in range(6):
        idunes.append(create_connected_dune(idunes[-1]))

    while True:
        if menu:
            ball.reset()
            dune.reset()
            score = 0
            screen.fill((65, 215, 255))
            for idune in idunes:
                idune.movement()
                idune.display(screen)

            if idunes[0].get_end_point()[0] < 0:
                idunes.pop(0)
                idunes.append(create_connected_dune(idunes[-1]))

            font = pygame.font.Font(None, 100)
            fonttwo=pygame.font.Font(None, 50)
            score_text = font.render('Hill Hop', True, (255, 255, 255))
            enter_text=fonttwo.render('Press Return to Start!', True, (255, 255, 255))
            screen.blit(score_text, (275, 250))
            screen.blit(enter_text,(235, 350))
        
            if pygame.key.get_pressed()[pygame.K_RETURN]:
                screen.fill((0,0,0))
                menu = False
                ball = Ball(x=width // 2, y=300)
                playing = True
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    pygame.quit()
                    sys.exit()

        if game_over:
            screen.fill((65, 215, 255))
            font = pygame.font.Font(None, 100)
            game_over_text = font.render('Game Over!', True, (255, 255, 255))
            score_text=fonttwo.render(f'Score: {score}', True, (255, 255, 255))
            try_again_text=fonttwo.render('Press Shift to Try Again', True, (255, 255, 255))
            screen.blit(game_over_text, (200, 250))
            screen.blit(score_text,(340, 350))
            screen.blit(try_again_text,(200, 425))
            if pygame.key.get_pressed()[pygame.K_RSHIFT]:
                screen.fill((0,0,0))
                menu = True
                game_over = False
                
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    pygame.quit()
                    sys.exit()

        if playing:
            font = pygame.font.Font(None, 100)
            screen.fill((65, 215, 255))
            dune.draw()
        
            if ball.crash:
                playing = False
                game_over = True

            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT or ball.crash:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    keys_held.add(event.key)
                    if ball.in_air_time > 0.2:
                        ball.gravity_multiplier_diving = 5.0

                elif event.type == pygame.KEYUP:
                    keys_held.discard(event.key)
                    ball.gravity_multiplier_diving = 1.0

            if pygame.K_SPACE in keys_held or ball.in_air:
                dune.update()

            else:
                dune.speed = 100
                dune.update()
        
            score_playing_text = font.render(f'{score}', True, (255, 255, 255))
            screen.blit(score_playing_text, (377, 10))
        
            ball.update(lambda x: dune.get_height_at(x), lambda x: dune.get_velocity_at(x), lambda x: dune.get_acceleration_at(x))
        
            if ball.y <= 350 and not ball.reached_peak:
                score += score_increment
                ball.reached_peak = True

            if not ball.in_air:
                ball.reached_peak = False

            ball.draw(screen)

        pygame.display.flip()
        fps_clock.tick(fps)

if __name__ == "__main__":
    main()

#add graphics to game and state pages
#somehow make the game a little easier

    
