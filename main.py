import sys
import pygame as pg
from objects import Player
from objects import Apple
from objects import WordScreen
from objects import Words
# testing commit from terminal
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Game:
    def __init__(self):
        pg.init()
        self.highscore = 0
        try:
            with open('highscore.txt', 'r', encoding='UTF-8') as highscore:
                self.highscore = int(highscore.read())
        except:
            with open('highscore.txt', 'w', encoding='UTF-8') as highscore:
                highscore.write(str(0))

        self.running = 1
        self.screen_size = [500, 500]
        self.current_screen_size = [500, 500]
        self.display = pg.Surface(self.screen_size)
        self.screen = pg.display.set_mode(self.current_screen_size, pg.RESIZABLE | pg.DOUBLEBUF, vsync=1)
        self.clock = pg.time.Clock()

        self.speed = 10

        self.player = Player(20, 25)
        self.apple = Apple(20, 25)
        self.death_screen = WordScreen('Futura', f'You died! Your final score was {self.player.apples_eaten * 100}.', 'Press any key to play again.', self.screen_size)
        self.start_screen = WordScreen('Futura', 'Use arrow keys to move.', 'Try and get as many apples as possible.', self.screen_size)
        self.pause_screen = WordScreen('Futura', 'Paused', 'Press ESCAPE to re-enter.', self.screen_size)
        self.score_words = Words('Futura', f'Score: {self.player.apples_eaten * 100}', (10, 10))
        self.highscore_words = Words('Futura', f'Highscore: {self.highscore}', (10, 20))

    def basic_event_handling(self, event):
        if event.type == pg.QUIT:
            self.running = 0
        if event.type == pg.VIDEORESIZE:
            self.current_screen_size = event.size
    def screen_resize(self):
        if self.current_screen_size[0] // self.current_screen_size[1]:
            self.screen.blit(pg.transform.scale(self.display, (self.current_screen_size[1], self.current_screen_size[1])), ((self.current_screen_size[0] - self.current_screen_size[1]) / 2, 0))
            if self.current_screen_size[0] / self.current_screen_size[1] != self.screen_size.copy()[0] / self.screen_size.copy()[1]:
                pg.draw.rect(self.screen, (255, 255, 255), pg.Rect((self.current_screen_size[0] - self.current_screen_size[1]) / 2, 0, self.current_screen_size[1], self.current_screen_size[1]), 1)
        else:
            self.screen.blit(pg.transform.scale(self.display, (self.current_screen_size[0], self.current_screen_size[0])), (0, (self.current_screen_size[1] - self.current_screen_size[0]) / 2))
            pg.draw.rect(self.screen, (255, 255, 255), pg.Rect(0, (self.current_screen_size[1] - self.current_screen_size[0]) / 2, self.current_screen_size[0], self.current_screen_size[0]), 1)

    def run(self):
        buffer_movement = [0, 1]
        while self.player.movement == [0, 0] and self.running:
            self.screen.fill(BLACK)
            self.display.fill(BLACK)
            for event in pg.event.get():
                self.basic_event_handling(event)
                self.player.handle_events(event, self.apple)
            self.apple.render(self.display)
            self.player.render(self.display)
            self.score_words.render(self.display)
            self.highscore_words.render(self.display)
            self.start_screen.render(self.display)

            self.screen_resize()
            pg.display.update()
            self.clock.tick(self.speed)

        while self.running:
            self.screen.fill(BLACK)
            self.display.fill(BLACK)
            for event in pg.event.get():
                self.basic_event_handling(event)
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    if self.player.movement != [0, 0]:
                        buffer_movement = self.player.movement
                        self.player.movement = [0, 0]
                    else:
                        self.player.movement = buffer_movement
                self.player.handle_events(event, self.apple)
                
            self.player.update()
            self.apple.render(self.display)
            self.player.render(self.display)
            self.apple.collisions(self.player, self.score_words)
            self.score_words.render(self.display)
            self.highscore_words.render(self.display)

            if self.player.dead:
                self.death_screen.big_render = self.death_screen.big_font.render(f'You died! Your final score was {self.player.apples_eaten * 100}.', 1, WHITE)
                self.death_screen.render(self.display)
                if self.player.apples_eaten * 100 > self.highscore:
                    with open('highscore.txt', 'w') as highscore:
                        highscore.write(str(self.player.apples_eaten * 100))
                    self.highscore = self.player.apples_eaten * 100
                    self.highscore_words.font_render = self.highscore_words.font.render(f'Highscore: {self.highscore}', 1, WHITE)
            elif self.player.movement == [0, 0]:
                self.pause_screen.render(self.display)

            # Processes screen sizing
            self.screen_resize()
            pg.display.update()
            self.clock.tick(self.speed)
        pg.quit()

if __name__ == '__main__':
    Game().run()
sys.exit()
