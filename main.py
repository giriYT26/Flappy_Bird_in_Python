import pygame,os,sys,signal
from tkinter.messagebox import showerror,showwarning
from os.path import join,dirname,isfile
WIDTH = 576 
HEIGHT = 1024
FPS = 120
CUR_DIR = dirname(__file__)
BG_IMG = join(CUR_DIR,"sprites","background-day.png")
FLOOR_IMG = join(CUR_DIR,"sprites","base.png")

class Player:
    def __init__(self):
        pass

class Background:
    def __init__(self):
        self.bg_surface = pygame.image.load(BG_IMG).convert()
        self.bg_surface = pygame.transform.scale2x(self.bg_surface)

        self.floor = pygame.image.load(FLOOR_IMG).convert()
        self.floor = pygame.transform.scale2x(self.floor)
        self.floor_x_pos = 0
    def update(self):
        self.floor_x_pos -=1
        if self.floor_x_pos <= -self.floor.get_width():
            self.floor_x_pos = 0

    def draw(self,surface):
        surface.blit(self.bg_surface,(0,0))
        surface.blit(self.floor,(self.floor_x_pos,790))
        surface.blit(self.floor,(self.floor_x_pos+self.floor.get_width(),790)) #0,790 -> correct pos of the base
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((576,900))
        self.clock = pygame.time.Clock()
        self.bg = Background()
    def run(self)->None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    os.kill(os.getpid(),signal.SIGTERM)
            self.bg.update()
            self.bg.draw(self.screen)
            pygame.display.update()
            self.clock.tick(FPS)

if  __name__   == "__main__":
    #print(__file__)
    game = Game()
    game.run()