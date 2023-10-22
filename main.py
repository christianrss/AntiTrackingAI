import pygame, sys, time
import pygame.time
import random

from settings import *
from sprites import BG, Fish, Worm

class Game:
    opcode = 0
    operand = 0 
    worm_ip = 0
    worm_counter = 0 
    worm_pattern_index = 0
    worm_xv = 0
    worm_yv = 0

    pattern_5 = [
        OPC_TRACKING_EVASIVE, 10,
        OPC_N, 100,
        OPC_TRACKING_EVASIVE, 20,
        OPC_E, 110,
        OPC_TRACKING_EVASIVE, 30,
        OPC_S, 70,
        OPC_TRACKING_EVASIVE, 40,
        OPC_W, 60,
        OPC_TRACKING_EVASIVE, 50,
        OPC_END, 0
    ]

    pattern_6 = [
        OPC_TRACKING_EVASIVE, 10,
        OPC_S, 100,
        OPC_TRACKING_EVASIVE, 20,
        OPC_SE, 110,
        OPC_TRACKING_EVASIVE, 30,
        OPC_E, 120,
        OPC_TRACKING_EVASIVE, 40,
        OPC_S, 50,
        OPC_TRACKING_EVASIVE, 50,
        OPC_RAND, 10,
        OPC_TRACKING_EVASIVE, 60,
        OPC_RAND, 5,
        OPC_TRACKING_EVASIVE, 10,
        OPC_END, 0
    ]

    pattern_7 = [
        OPC_TRACKING_EVASIVE, 10,
        OPC_NW, 100,
        OPC_TRACKING_EVASIVE, 20,
        OPC_N, 110,
        OPC_TRACKING_EVASIVE, 30,
        OPC_NE, 60,
        OPC_TRACKING_EVASIVE, 40,
        OPC_SE, 40,
        OPC_TRACKING_EVASIVE, 50,
        OPC_RAND, 4,
        OPC_TRACKING_EVASIVE, 60,
        OPC_RAND, 3,
        OPC_TRACKING_EVASIVE, 10,
        OPC_E, 60,
        OPC_TRACKING_EVASIVE, 20,
        OPC_END, 0
    ]

    pattern_8 = [
        OPC_TRACKING_EVASIVE, 10,
        OPC_E, 100,
        OPC_TRACKING_EVASIVE, 20,
        OPC_S, 100,
        OPC_TRACKING_EVASIVE, 30,
        OPC_SW, 100,
        OPC_TRACKING_EVASIVE, 20,
        OPC_W, 50,
        OPC_TRACKING_EVASIVE, 30,
        OPC_RAND, 4,
        OPC_TRACKING_EVASIVE, 10,
        OPC_RAND, 3,
        OPC_TRACKING_EVASIVE, 50,
        OPC_S, 100,
        OPC_TRACKING_EVASIVE, 10,
        OPC_END, 0
    ]

    patterns = [pattern_5, pattern_6, pattern_7, pattern_8]

    curr_pattern = None
    def __init__(self):
        #setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("AntiTrackingAI by Christian ZeroBit")
        self.clock = pygame.time.Clock()
        self.active = True

        # sprite groups
        self.all_sprites = pygame.sprite.Group()

        # scale factor
        bg_height = pygame.image.load('graphics/water2.jpg').get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height

        # sprite setup
        BG(self.all_sprites, self.scale_factor)
        self.worm = Worm(self.all_sprites, self.scale_factor / 5.0)
        self.fish = Fish(self.all_sprites, self.scale_factor / 5.0)

        #text
        self.font = pygame.font.Font('graphics/fonts/NiseSegaSonic.ttf', 30)
        self.start_offset = 0
    def worm_ai(self):
        WEST_BIT  = 1
        EAST_BIT  = 2
        NORTH_BIT = 4
        SOUTH_BIT = 8

        if (self.curr_pattern == None):
            self.skelaton_pattern_index = random.randint(0,len(self.patterns)-1)
            self.curr_pattern = self.patterns[self.skelaton_pattern_index]
            self.worm_ip      = 0
            self.worm_counter = 0
        if (self.worm_counter <= 0):
            opcode  = self.curr_pattern[self.worm_ip]
            self.worm_ip +=1
            operand = self.curr_pattern[self.worm_ip]
            self.worm_ip +=1

            if opcode == OPC_E:
                self.worm_xv = 3
                self.worm_yv = 0
                self.worm.direction = 180
                self.worm_counter = operand
            elif opcode == OPC_NE:
                self.worm_xv = 3
                self.worm_yv = -3
                self.worm.direction = -80
                self.worm_counter = operand
            elif opcode == OPC_N:
                self.worm_xv = 0
                self.worm_yv = -3
                self.worm.direction = -80
                self.worm_counter = operand
            elif opcode == OPC_NW:
                self.worm_xv = -3
                self.worm_yv = -3
                self.worm.direction = -80
                self.worm_counter = operand
            elif opcode == OPC_W:
                self.worm_xv = -3
                self.worm_yv = 0
                self.worm.direction = 0
                self.worm_counter = operand
            elif opcode == OPC_SW:
                self.worm_xv = -3
                self.worm_yv = 3
                self.worm.direction = 80
                self.worm_counter = operand
            elif opcode == OPC_S:
                self.worm_xv = 0
                self.worm_yv = 3
                self.worm.direction = 80
                self.worm_counter = operand
            elif opcode == OPC_SE:
                self.worm_xv = 3
                self.worm_yv = 3
                self.worm.direction = 80
                self.worm_counter = operand
            elif opcode == OPC_STOP:
                self.worm_xv = 0
                self.worm_yv = 0
                self.worm_counter = operand
            elif opcode == OPC_RAND:
                self.worm_counter = 0
            elif opcode == OPC_TRACKING_EVASIVE:
                if abs(self.worm.pos.x - self.fish.pos.x) + abs(self.worm.pos.y - self.fish.pos.y) < 350:
                    direction = 0

                    if (self.fish.pos.x < self.worm.pos.x):
                        direction |= EAST_BIT
                    elif (self.fish.pos.x > self.worm.pos.x):
                        direction |= WEST_BIT
                    if (self.fish.pos.y < self.worm.pos.y):
                        direction |= SOUTH_BIT
                    elif (self.fish.pos.y > self.worm.pos.y):
                        direction |= NORTH_BIT

                    if (direction == WEST_BIT):
                        self.worm_xv = -3
                        self.worm_yv = 0
                        self.worm.direction = 0
                        self.worm_counter = operand
                    elif (direction == EAST_BIT):
                        self.worm_xv = 3
                        self.worm_yv = 0
                        self.worm.direction = 180
                        self.worm_counter = operand
                    elif (direction == NORTH_BIT):
                        self.worm_xv = 0
                        self.worm_yv = -3
                        self.worm.direction = -80
                        self.worm_counter = operand
                    elif (direction == SOUTH_BIT):
                        self.worm_xv = 0
                        self.worm_yv = 3
                        self.worm.direction = 80
                        self.worm_counter = operand
                    elif (direction == NORTH_BIT | WEST_BIT):
                        self.worm_xv = -3
                        self.worm_yv = -3
                        self.worm.direction = -80
                        self.worm_counter = operand
                    elif (direction == NORTH_BIT | EAST_BIT):
                        self.worm_xv = 3
                        self.worm_yv = -3
                        self.worm.direction = -80
                        self.worm_counter = operand
                    elif (direction == SOUTH_BIT | WEST_BIT):
                        self.worm_xv = -3
                        self.worm_yv = 3
                        self.worm.direction = 80
                        self.worm_counter = operand
                    elif (direction == SOUTH_BIT | EAST_BIT):
                        self.worm_xv = 3
                        self.worm_yv = 3
                        self.worm.direction = 80
                        self.worm_counter = operand
                self.worm_counter = operand
            elif opcode == OPC_END:
                self.worm_xv = 0
                self.worm_yv = 0
                self.skelaton_pattern_index = random.randint(0,len(self.patterns)-1)
                self.curr_pattern = self.patterns[self.skelaton_pattern_index]
                self.worm_ip = 0
                self.worm_counter = 0

        self.worm_counter -= 1

    def run(self):
        last_time = time.time()
        pygame.key.set_repeat(1,10)
        while True:
            # delta time
            dt = time.time() - last_time
            last_time = time.time()

            fish_speed = 200 * dt

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.fish.up(fish_speed)
                    elif event.key == pygame.K_DOWN:
                        self.fish.down(fish_speed)
                    elif event.key == pygame.K_RIGHT:
                        self.fish.right(fish_speed)
                    elif event.key == pygame.K_LEFT:
                        self.fish.left(fish_speed)

            self.worm_ai()
            self.worm.pos.x += 50 * self.worm_xv * dt
            self.worm.rect.x = round(self.worm.pos.x)
            self.worm.pos.y += 50 * self.worm_yv * dt
            self.worm.rect.y = round(self.worm.pos.y)

            # game logic
            self.display_surface.fill('black')
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)

            pygame.display.update()
            self.clock.tick(FRAMERATE)

if __name__ == '__main__':
    game = Game()
    game.run()