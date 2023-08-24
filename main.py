import pygame, sys, time
import pygame.time

from settings import *
from sprites import BG, Fish, Worm
from pygame import mixer, math
import random

opcode              = 0 # general opcode
operand             = 0 # general operand
worm_ip             = 0 # pattern instruction pointer for worm
worm_counter        = 0 # counter of pattern control
worm_pattern_index  = 0 # the current pattern being executed

opcode_names = {
    OPC_E,
    OPC_NE,
    OPC_N,
    OPC_NW,
    OPC_W,
    OPC_SW,
    OPC_S,
    OPC_SE,
    OPC_STOP,
    OPC_RAND,
    OPC_TEST_DIST
}

pattern_1 = {
    OPC_W, 10, OPC_NW, 10, OPC_N, 10, OPC_NE, 10,
    OPC_TEST_DIST, 50, # a distance test
    OPC_E, 10, OPC_SE, 10, OPC_S, 10, OPC_SW, 10,
    OPC_W, 10, OPC_RAND, 10,
    OPC_TEST_DIST, 50, # a distance test
    OPC_W, 20, OPC_NW, 10, OPC_N, 20, OPC_NE, 10,
    OPC_E, 20, OPC_SE, 10, OPC_S, 20, OPC_SW, 10,
    OPC_TEST_DIST, 50, # a distance test
    OPC_W, 10, OPC_END, 0
}

pattern_2 = {
    OPC_E, 20, OPC_W, 20, OPC_STOP, 20, OPC_NE, 10,
    OPC_TEST_DIST, 50, # a distance test
    OPC_W, 10, OPC_NW, 10, OPC_SW, 20, OPC_NW, 20,
    OPC_TEST_DIST, 50, # a distance test
    OPC_SW, 20, OPC_NW, 30, OPC_SW, 10, OPC_S, 50,
    OPC_TEST_DIST, 50, # a distance test
    OPC_W, 2, OPC_NW, 2, OPC_N, 2, OPC_NE, 50 , OPC_TEST_DIST, 50, # a distance test
    OPC_E, 2, OPC_SE, 2, OPC_S, 2, OPC_RAND, 10, OPC_END, 0
}

pattern_3 = {
    OPC_N, 10, OPC_S, 10, OPC_N, 10, OPC_S, 10,
    OPC_TEST_DIST, 50, # a distance test
    OPC_E, 10, OPC_W, 10, OPC_E, 10, OPC_W, 10,
    OPC_TEST_DIST, 50, # a distance test
    OPC_NW, 10, OPC_N, 10, OPC_NE, 10, OPC_N, 10,
    OPC_TEST_DIST, 60, # a distance test
    OPC_STOP, 20, OPC_RAND, 5, OPC_E, 50, OPC_S, OPC_W, 50,
    OPC_TEST_DIST, 50, # a distance test
    OPC_E, 10, OPC_E, 10, OPC_E, 10, OPC_NW, 100, OPC_TEST_DIST, 60, # a distance test,
    OPC_STOP, 10, OPC_END, 0
}

pattern_4 = {
    OPC_W, 100,
    OPC_NW, 2, OPC_N, 2, OPC_NE, 2,
    OPC_E, 100,
    OPC_NE, 2, OPC_N, 2, OPC_NW, 2,
    OPC_TEST_DIST, 50, # a distance test
    OPC_W, 100,
    OPC_NW, 2, OPC_N, 2, OPC_NE, 2,
    OPC_E, 100,
    OPC_NE, 2, OPC_N, 2, OPC_NW, 2,
    OPC_TEST_DIST, 50, # a distance test
    OPC_W, 100,
    OPC_NW, 2, OPC_N, 2, OPC_NE, 2,
    OPC_E, 100,
    OPC_NE, 2, OPC_N, 2, OPC_NW, 2,
    OPC_TEST_DIST, 50, # a distance test
    OPC_RAND, 10, OPC_RAND, 5,

    OPC_SW, 2, OPC_S, 2, OPC_SE, 2,
    OPC_E, 100,
    OPC_TEST_DIST, 50, # a distance test
    OPC_SE, 2, OPC_S, 2, OPC_SW, 2,
    OPC_W, 100,
    OPC_TEST_DIST, 50, # a distance test
    OPC_SW, 2, OPC_S, 2, OPC_SE, 2,
    OPC_E, 100,
    OPC_SE, 2, OPC_S, 2, OPC_SW, 2,
    OPC_W, 100,
    OPC_TEST_DIST, 50, # a distance test
    OPC_SW, 2, OPC_S, 2, OPC_SE, 2,
    OPC_E, 100,
    OPC_TEST_DIST, 50, # a distance test
    OPC_SE, 2, OPC_S, 2, OPC_SW, 2,
    OPC_W, 100, OPC_END, 0
}

patterns = { pattern_1, pattern_2, pattern_3, pattern_4 }

curr_pattern = None

class Game:
    def __init__(self):
        #setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("AntiTrackingAI by Christian Rafael")
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

        self.music = pygame.mixer.Sound('sounds/roving_mars.mp3')
        #self.music.play(loops = -1)

        #self.gameover_sound = pygame.mixer.Sound('sounds/game_over.mp3')
    def worm_ai(self, move_factor):
        old_worm_pos = self.worm.pos.copy()
        if ((abs(self.worm.pos.x - self.fish.pos.x) + abs(self.worm.pos.y - self.fish.pos.y)) < 300):
            if (self.fish.pos.x < self.worm.pos.x):
                self.worm.direction = 180
                self.worm.pos.x += move_factor
                self.worm.rect.x = round(self.worm.pos.x)
            elif (self.fish.pos.x > self.worm.pos.x):
                self.worm.direction = 0
                self.worm.pos.x -= move_factor
                self.worm.rect.x = round(self.worm.pos.x)

            if (self.fish.pos.y < self.worm.pos.y):
                #self.worm.direction = 80
                self.worm.pos.y += move_factor
                self.worm.rect.y = round(self.worm.pos.y)
            elif (self.fish.pos.y > self.worm.pos.y):
                #self.worm.direction = -80
                self.worm.pos.y -= move_factor
                self.worm.rect.y = round(self.worm.pos.y)
        else:
            if (WINDOW_WIDTH/2 > self.worm.pos.x):
                self.worm.direction = 180
                self.worm.pos.x += move_factor
                self.worm.rect.x = round(self.worm.pos.x)
            elif (WINDOW_WIDTH/2 < self.worm.pos.x):
                self.worm.direction = 0
                self.worm.pos.x -= move_factor
                self.worm.rect.x = round(self.worm.pos.x)

            if (WINDOW_HEIGHT/2 > self.worm.pos.y):
                self.worm.direction = 80
                self.worm.pos.y += move_factor
                self.worm.rect.y = round(self.worm.pos.y)
            elif (WINDOW_HEIGHT/2 < self.worm.pos.y):
                self.worm.direction = -80
                self.worm.pos.y -= move_factor
                self.worm.rect.y = round(self.worm.pos.y)
    def fish_ai(self, delta_time):
        tv_vector = pygame.Vector2()
        tv_vector.xy = (self.worm.pos.x - self.fish.pos.x, self.worm.pos.y - self.fish.pos.y)
        tv = tv_vector.xy / tv_vector.length()

        old_fish_pos = self.fish.pos.copy()
        if (self.worm.pos.x > self.fish.pos.x):
            self.fish.direction = 180
            self.fish.pos.x += WORM_TRACKING_RATE * tv_vector.x * delta_time
            self.fish.rect.x = round(self.fish.pos.x)
        elif (self.worm.pos.x < self.fish.pos.x):
            self.fish.direction = 0
            self.fish.pos.x -= WORM_TRACKING_RATE * tv_vector.x * delta_time
            self.fish.rect.x = round(self.fish.pos.x)

        if (self.worm.pos.y > self.fish.pos.y):
            self.fish.direction = 80
            self.fish.pos.y += WORM_TRACKING_RATE * tv_vector.y * delta_time
            self.fish.rect.y = round(self.fish.pos.y)
        elif (self.worm.pos.y < self.fish.pos.y):
            self.fish.direction = -80
            self.fish.pos.y -= WORM_TRACKING_RATE * tv_vector.y * delta_time
            self.fish.rect.y = round(self.fish.pos.y)
    def run(self):
        last_time = time.time()
        pygame.key.set_repeat(1,10)
        while True:
            # delta time
            dt = time.time() - last_time
            last_time = time.time()

            worm_speed = 100 * dt + random.random() % 9
            fish_speed = 100 * dt + random.random() % 9

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

            self.worm_ai(worm_speed)
            #self.fish_ai(dt)
            # game logic
            self.display_surface.fill('black')
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)

            pygame.display.update()
            self.clock.tick(FRAMERATE)

if __name__ == '__main__':
    game = Game()
    game.run()