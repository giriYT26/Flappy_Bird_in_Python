import pygame,os,sys,signal
from tkinter.messagebox import showerror,showwarning
from os.path import join,dirname,isfile
from random import choice
#global GRAVITY,PLAYER_MOVEMENT
#print("game starts")
WIDTH = 576 
HEIGHT = 1024
FPS = 60 #130
GRAVITY = 0.24
PLY_MOV = 0
CUR_DIR = dirname(__file__)
BG_IMG = join(CUR_DIR,"sprites","background-day.png")
FLOOR_IMG = join(CUR_DIR,"sprites","base.png")
OBS_IMG = join(CUR_DIR,"sprites","pipe-green.png")
PLAYER1_IMG = join(CUR_DIR,"sprites","redbird-downflap.png")
PLAYER2_IMG = join(CUR_DIR,"sprites","redbird-midflap.png")
PLAYER3_IMG = join(CUR_DIR,"sprites","redbird-upflap.png")

class Player:
    def __init__(self):
        self.bird_movement = PLY_MOV
        self.bird_idx = 0
        #self.bird_surface = pygame.image.load(PLAYER_IMG).convert_alpha()
        self.sprite_load() # Loads the sprites before the game starts
        self.animation()
        self.bird_rect = self.bird_surface.get_rect(center=(100,600)) #100,512
        self.bird_flaps = pygame.USEREVENT + 1
        pygame.time.set_timer(self.bird_flaps,200) #Created a user event that triggers for every 200ms
    def sprite_load(self):
        bird_downflap = pygame.image.load(PLAYER1_IMG).convert_alpha()
        bird_midflap = pygame.image.load(PLAYER2_IMG).convert_alpha()
        bird_upflap = pygame.image.load(PLAYER3_IMG).convert_alpha()
        self.bird_frame = [bird_downflap,bird_midflap,bird_upflap]
    def animation(self):
        self.bird_surface = self.bird_frame[self.bird_idx]
        self.bird_surface = pygame.transform.scale2x(self.bird_surface)
    def update(self):
        self.bird_movement += GRAVITY
        self.bird_rect.centery += self.bird_movement
    def ply_rotate(self):
        self.Rotated_bird_surface = pygame.transform.rotozoom(self.bird_surface,-self.bird_movement*3,1)
        return self.Rotated_bird_surface
    def draw(self,surface):
        rotated_bird_surface = self.ply_rotate()
        surface.blit(rotated_bird_surface,self.bird_rect)
    
class Pipes:
    def __init__(self):
        self.pipe_surface = pygame.image.load(OBS_IMG).convert()
        self.pipe_surface = pygame.transform.scale2x(self.pipe_surface)
        self.pipe_lst = []
        self.pipe_height = [400,600,610,500] #all the possible height for the pipe
        #Spawn pipe on a time interval of 1200ms (2.1sec)
        self.spawnpipe = pygame.USEREVENT #creating a user event 
        pygame.time.set_timer(self.spawnpipe,1200) # user event triger by time for every 2.1sec
    def create_pipe(self) :
        random_pipe_height = choice(self.pipe_height)
        self.bottom_pipe = self.pipe_surface.get_rect(midtop=(700,random_pipe_height)) #700,512
        self.top_pipe = self.pipe_surface.get_rect(midbottom=(700,random_pipe_height-300))
        return self.bottom_pipe,self.top_pipe
    def check_collision(self,bird):
        for pipe in self.pipe_lst:
            if bird.colliderect(pipe):
                return False
            elif bird.top <= -100 or bird.bottom >= 790:
                print("game_over") 
                return False
        return True
    def move_pipes(self)->list:
        """Move the pipes to left"""
        for pipe in self.pipe_lst:
            pipe.centerx -= 5
        return self.pipe_lst
    
    def draw(self,surface):
        for pipe in self.pipe_lst:
            if pipe.bottom >= 900:#1028
                surface.blit(self.pipe_surface,pipe)
            else:
                filp_pipe = pygame.transform.flip(self.pipe_surface,False,True)
                surface.blit(filp_pipe,pipe)
        
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
        self.game_active = True
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
                    if event.key == pygame.K_SPACE and self.game_active == True:
                        self.player.bird_movement = 0
                        #for the default game 9 is good for 60fps
                        self.player.bird_movement -= 9 #12 when hard or 10 it's ok to handle it and if the game what to be easy set it to 5-8
                    if event.key == pygame.K_SPACE and self.game_active == False:
                        self.game_active = True
                        self.pipe.pipe_lst.clear()
                        self.player.bird_rect.center = (100,450) #100,512
                        self.player.bird_movement = PLY_MOV
                        #self.player.

                if event.type == self.pipe.spawnpipe :
                    self.pipe.pipe_lst.extend(self.pipe.create_pipe())
                    #print(self.pipe.pipe_lst)
                if event.type == self.player.bird_flaps:
                    if self.player.bird_idx < 2:
                        self.player.bird_idx +=1
                        #print(self.player.bird_idx)
                    else:
                        self.player.bird_idx = 0
                    self.player.animation()

            #background 
            self.bg.update()
            self.bg.draw_background(self.screen)

            #this below line will work only if the game is active
            if self.game_active:
                #pipes
                self.pipe.pipe_lst = self.pipe.move_pipes()
                self.pipe.draw(self.screen)
                #player
                self.player.update()
                self.player.draw(self.screen)
                #Checking for collision
                self.game_active= self.pipe.check_collision(self.player.bird_rect)

            #floor
            self.bg.draw_floor(self.screen)

            pygame.display.update()
            self.clock.tick(FPS)

if  __name__   == "__main__":
    #print(__file__)
    game = Game()
    game.run()