import pygame,os,sys,signal
from tkinter.messagebox import showerror,showwarning
from os.path import join,dirname,isfile
#global GRAVITY,PLAYER_MOVEMENT
print("game starts")
WIDTH = 576 
HEIGHT = 1024
FPS = 130
GRAVITY = 0.24
CUR_DIR = dirname(__file__)
BG_IMG = join(CUR_DIR,"sprites","background-day.png")
FLOOR_IMG = join(CUR_DIR,"sprites","base.png")
PLAYER_IMG = join(CUR_DIR,"sprites","redbird-midflap.png")
OBS_IMG = join(CUR_DIR,"sprites","pipe-green.png")

class Player:
    def __init__(self):
        self.bird_movement = 0
        self.bird_surface = pygame.image.load(PLAYER_IMG).convert()
        self.bird_surface = pygame.transform.scale2x(self.bird_surface)
        self.bird_rect = self.bird_surface.get_rect(center=(100,HEIGHT//2))
    def update(self):
        self.bird_movement += GRAVITY
        self.bird_rect.centery += self.bird_movement
    def draw(self,surface):
        surface.blit(self.bird_surface,self.bird_rect)
class Pipes:
    def __init__(self):
        self.pipe_surface = pygame.image.load(OBS_IMG).convert()
        self.pipe_surface = pygame.transform.scale2x(self.pipe_surface)
        self.pipe_lst = []
        #Spawn pipe on a time interval of 1200ms (2.1sec)
        self.spawnpipe = pygame.USEREVENT #creating a user event 
        pygame.time.set_timer(self.spawnpipe,1200) # user event triger by time for every 2.1sec
    def create_pipe(self) :
        self.new_pipe = self.pipe_surface.get_rect(midtop=(700,512)) #700,512
        return self.new_pipe
    
    def move_pipes(self):
        """Move the pipes to left"""
        for pipe in self.pipe_lst:
            pipe.centerx -= 5
        return self.pipe_lst
    
    def draw(self,surface):
        for pipe in self.pipe_lst:
            surface.blit(self.pipe_surface,pipe)
        
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

    def draw_background(self,surface):
        surface.blit(self.bg_surface,(0,0))
    def draw_floor(self,surface):
        surface.blit(self.floor,(self.floor_x_pos,790))
        surface.blit(self.floor,(self.floor_x_pos+self.floor.get_width(),790)) #0,790 -> correct pos of the base
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((576,900))
        self.clock = pygame.time.Clock()
        self.bg = Background()
        self.player = Player()
        self.pipe = Pipes()
    def run(self)->None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    os.kill(os.getpid(),signal.SIGTERM)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.bird_movement = 0
                        self.player.bird_movement -=12
                if event.type == self.pipe.spawnpipe :
                    self.pipe.pipe_lst.append(self.pipe.create_pipe())
                    #print(self.pipe.pipe_lst)
            #background 
            self.bg.update()
            self.bg.draw_background(self.screen)
            #pipes
            self.pipe.pipe_lst = self.pipe.move_pipes()
            self.pipe.draw(self.screen )
            #floor
            self.bg.draw_floor(self.screen)
            #player
            self.player.update()
            self.player.draw(self.screen)
            pygame.display.update()
            self.clock.tick(FPS)

if  __name__   == "__main__":
    #print(__file__)
    game = Game()
    game.run()