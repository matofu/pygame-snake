import pygame as pg
import random

pg.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Player:
    def __init__(self, rect_size, screen_size):
        self.screen_size = screen_size
        self.rect_size = rect_size
        self.movement = [0, 0]
        self.length = 4
        self.positions = [[6 + self.length // 2 - i, self.screen_size // 2] for i in range(0, self.length)]
        self.old_positions = self.positions.copy()
        self.dead = 0
        self.apples_eaten = 0
        self.color = GREEN
        # self.buffer just tells if a key has been pressed in the frame already
        self.buffer = 0
    def update(self):
        if self.movement != [0, 0]:
            self.color = GREEN
            self.buffer = 0
            self.old_positions = self.positions.copy()
            for i in range(self.length - 1, -1, -1):
                if i > 0:
                    self.positions[i] = self.old_positions[i - 1].copy()
                else:
                    self.positions[i] = [sum(i) for i in zip(self.positions[i], self.movement)]
            if self.positions[0][0] >= self.screen_size or self.positions[0][1] >= self.screen_size or self.positions[0][0] < 0 or self.positions[0][1] < 0 or self.positions[0] in [item for dex, item in enumerate(self.positions) if dex != 0]:
                self.dead = 1
        else:
            self.color = BLUE
        if self.dead:
            self.movement = [0, 0]
    def render(self, surf):
        for rect in self.get_rects():
            pg.draw.rect(surf, self.color, rect, self.rect_size // 4)
    def handle_events(self, event, apple):
        if event.type == pg.KEYDOWN and not self.buffer:
            if (event.key == pg.K_UP or event.key == pg.K_w) and self.movement[1] != 1:
                self.buffer = 1 # inside this if statement and not the broader one because it prevents the player from not being able to move after pressing any key except arrow keys at the start of the game
                self.movement = [0, -1]
            if (event.key == pg.K_DOWN or event.key == pg.K_s) and self.movement[1] != -1:
                self.buffer = 1
                self.movement = [0, 1]
            if (event.key == pg.K_LEFT or event.key == pg.K_a) and self.movement[0] != 1:
                self.buffer = 1
                self.movement = [-1, 0]
            if (event.key == pg.K_RIGHT or event.key == pg.K_d) and self.movement[0] != -1:
                self.buffer = 1
                self.movement = [1, 0]
            if self.dead:
                apple.reset()
                self.reset()
    def get_rects(self):
        rects = []
        for square in self.positions:
            rects.append(pg.Rect(square[0] * self.rect_size, square[1] * self.rect_size, self.rect_size, self.rect_size))
        return rects
    def reset(self):
        self.movement = [1, 0]
        self.length = 4
        self.positions = [[6 + self.length // 2 - i, self.screen_size // 2] for i in range(0, self.length)]
        self.old_positions = self.positions.copy()
        self.dead = 0
        self.apples_eaten = 0
        self.color = GREEN

    def grow_longer(self):
        # self.length += 1
        self.length = min(self.length + 1, self.screen_size**2)
        if self.length < self.screen_size**2:
            self.positions.append(self.old_positions[-1])

class Apple:
    def __init__(self, rect_size, screen_size):
        self.screen_size = screen_size
        self.rect_size = rect_size
        self.position = [self.screen_size // 2, self.screen_size // 2]
        self.rect = pg.Rect(self.position[0] * self.rect_size, self.position[1] * self.rect_size, self.rect_size, self.rect_size)
    def collisions(self, player, score_words):
        self.rect = pg.Rect(self.position[0] * self.rect_size, self.position[1] * self.rect_size, self.rect_size, self.rect_size)
        if self.rect.colliderect(player.get_rects()[0]):
            self.position = [random.randint(0, self.screen_size - 1), random.randint(0, self.screen_size - 1)]
            player.apples_eaten += 1
            score_words.font_render = score_words.font.render(f'Score: {player.apples_eaten * 100}', 1, WHITE)
            player.grow_longer()
    def render(self, surf):
        pg.draw.rect(surf, RED, self.rect, self.rect_size // 4)
    def reset(self):
        self.position = [self.screen_size // 2, self.screen_size // 2]
        self.rect = pg.Rect(self.position[0] * self.rect_size, self.position[1] * self.rect_size, self.rect_size, self.rect_size)
class Words:
    def __init__(self, font, words, pos):
        self.position = pos
        self.font = pg.font.SysFont(font, 13)
        self.font_render = self.font.render(words, 1, WHITE)
    def render(self, surf):
        surf.blit(self.font_render, self.position)

class WordScreen:
    def __init__(self, font, big_words, small_words, screen_size):
        self.screen_size = screen_size
        self.big_font = pg.font.SysFont(font, 20)
        self.small_font = pg.font.SysFont(font, 13)
        self.big_render = self.big_font.render(big_words, 1, WHITE)
        self.small_render = self.small_font.render(small_words, 1, WHITE)
    def render(self, surf):
        surf.blit(self.big_render, ((self.screen_size[0] - self.big_render.get_width()) // 2, (self.screen_size[1] - (self.big_render.get_height() + self.small_render.get_height())) // 2))
        surf.blit(self.small_render, ((self.screen_size[0] - self.small_render.get_width()) // 2, (self.screen_size[1] - (self.big_render.get_height() + self.small_render.get_height())) // 2 + self.big_render.get_height()))
