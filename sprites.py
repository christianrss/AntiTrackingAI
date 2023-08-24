import pygame
from settings import *
from random import choice, randint

class BG(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        bg_image = pygame.image.load('graphics/water2.jpg').convert()

        full_height = bg_image.get_height() * scale_factor
        full_width  = bg_image.get_width() * scale_factor
        full_sized_image = pygame.transform.scale(bg_image, (full_width,full_height))

        self.image = pygame.Surface((full_width * 2, full_height))
        self.image.blit(full_sized_image, (0,0))
        self.image.blit(full_sized_image, (full_width,0))

        self.rect = self.image.get_rect(topleft = (0,0))
        self.pos = pygame.math.Vector2(self.rect.topleft)
    def update(self,dt):
        self.pos.x = 0
        self.rect.x = round(self.pos.x)

class Fish(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)

        # image
        self.import_frames(scale_factor)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        #rect
        self.rect = self.image.get_rect(topright = (WINDOW_WIDTH - 20, 10))
        self.pos = pygame.math.Vector2(self.rect.topright)

        #movement
        self.direction = 0

        # mask
        self.mask = pygame.mask.from_surface(self.image)

        # sound
        #self.jump_sound = pygame.mixer.Sound('sounds/jump.mp3')
        #self.jump_sound.set_volume(0.3)
    #def jump(self):
        #self.jump_sound.play()
        #self.direction = -400
    def import_frames(self, scale_factor):
        self.frames = []
        for i in range(1,4):
            surf = pygame.image.load(f'graphics/fish/fish_left_{i}.png').convert_alpha()
            scaled_surface = pygame.transform.scale(surf, pygame.math.Vector2(surf.get_size()) * scale_factor)
            self.frames.append(scaled_surface)

    def up(self, move_factor):
        self.direction = -80
        self.pos.y -= move_factor
        self.rect.y = round(self.pos.y)
    def down(self, move_factor):
        self.direction = 80
        self.pos.y += move_factor
        self.rect.y = round(self.pos.y)
    def right(self, move_factor):
        self.direction = 180
        self.pos.x += move_factor
        self.rect.x = round(self.pos.x)
    def left(self, move_factor):
        self.direction = 0
        self.pos.x -= move_factor
        self.rect.x = round(self.pos.x)
    def test_offscreen(self):
        if (self.pos.x >= WINDOW_WIDTH):
            self.pos.x = -self.image.get_width()
            self.rect.x = round(self.pos.x)
        elif (self.pos.x < -self.image.get_width()):
            self.pos.x = WINDOW_WIDTH
            self.rect.x = round(self.pos.x)

        if (self.pos.y >= WINDOW_HEIGHT):
            self.pos.y = -self.image.get_height()
            self.rect.y = round(self.pos.y)
        elif (self.pos.y < -self.image.get_height()):
            self.pos.y = WINDOW_HEIGHT
            self.rect.y = round(self.pos.y)
    def animate(self,dt):
        self.frame_index += 10 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
    def rotate(self):
        rotated_fish = pygame.transform.rotozoom(self.image, self.direction, 1)
        self.image = rotated_fish
        self.mask = pygame.mask.from_surface(self.image)
    def update(self,dt):
        self.test_offscreen()
        self.animate(dt)
        self.rotate()

class Worm(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)

        # image
        self.import_frames(scale_factor)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        #rect
        self.rect = self.image.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.pos = pygame.math.Vector2(self.rect.center)

        self.direction = 0

        # mask
        self.mask = pygame.mask.from_surface(self.image)
    def import_frames(self, scale_factor):
        self.frames = []
        for i in range(1,4):
            surf = pygame.image.load(f'graphics/worm/worm_left_{i}.png').convert_alpha()
            scaled_surface = pygame.transform.scale(surf, pygame.math.Vector2(surf.get_size()) * scale_factor)
            self.frames.append(scaled_surface)
    def test_offscreen(self):
        if (self.pos.x >= WINDOW_WIDTH):
            self.pos.x = -self.image.get_width()
            self.rect.x = round(self.pos.x)
        elif (self.pos.x < -self.image.get_width()):
            self.pos.x = WINDOW_WIDTH
            self.rect.x = round(self.pos.x)

        if (self.pos.y >= WINDOW_HEIGHT):
            self.pos.y = -self.image.get_height()
            self.rect.y = round(self.pos.y)
        elif (self.pos.y < -self.image.get_height()):
            self.pos.y = WINDOW_HEIGHT
            self.rect.y = round(self.pos.y)

    def animate(self,dt):
        self.frame_index += 5 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def rotate(self):
        rotated_worm = pygame.transform.rotozoom(self.image, self.direction, 1)
        self.image = rotated_worm
        self.mask = pygame.mask.from_surface(self.image)

    def update(self,dt):
        self.test_offscreen()
        self.animate(dt)
        self.rotate()