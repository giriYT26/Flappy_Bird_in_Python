import pygame,os,sys,signal
from tkinter.messagebox import showerror,showwarning
from os.path import join,dirname,isfile
from random import choice
#global GRAVITY,PLAYER_MOVEMENT
#print("game starts")
WIDTH = 576 
HEIGHT = 1024
FPS = 90 #const 60 fps not 130
GRAVITY = 0.24
PLY_MOV = 0
CUR_DIR = dirname(__file__)
#print(CUR_DIR)
BG_IMG = join(CUR_DIR,"sprites","background-day.png")
FLOOR_IMG = join(CUR_DIR,"sprites","base.png")
OBS_IMG = join(CUR_DIR,"sprites","pipe-green.png")
GAME_OVER_IMG_PATH = join(CUR_DIR,"sprites","gameover.png")
TRY_AGAIN_IMG_PATH = join(CUR_DIR,"sprites","Try_Again.png")
PLAYER1_IMG = join(CUR_DIR,"sprites","redbird-downflap.png")
PLAYER2_IMG = join(CUR_DIR,"sprites","redbird-midflap.png")
PLAYER3_IMG = join(CUR_DIR,"sprites","redbird-upflap.png")
FLAP_SOUND_PATH = join(CUR_DIR,"audio","wing.wav")
PLY_HIT_SOUND_PATH = join(CUR_DIR,"audio","hit.wav")
COIN_SOUND_PATH = join(CUR_DIR,"audio","point.wav")
FONT_FILE_PATH = join(CUR_DIR,"04B_19.TTF")

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
    def check_collision(self,bird,ply_hit_sound):
        for pipe in self.pipe_lst:
            if bird.colliderect(pipe):
                ply_hit_sound.play()
                return False
            elif bird.top <= -100 or bird.bottom >= 800: #800
                #print("game_over") 
                ply_hit_sound.play()
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

class Scoreboard:
    "Handels Scores and Game Over part"
    def __init__(self):
        self.game_font = pygame.font.Font(FONT_FILE_PATH,40)
        self.score,self.high_score = 0,0
    def update_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
    def score_display(self,game_status,screen,coin_sound = None):
        if game_status == "main_game":
            self.score_surface = self.game_font.render(str(int(self.score)),antialias= True, color=(255,255,255))
            self.score_rect = self.score_surface.get_rect(center = (288,50))
            screen.blit(self.score_surface,self.score_rect)
            #coin_sound.play()
        if game_status == "game_over":
            #Current_score or score after u die 
            self.score_surface = self.game_font.render(f"Score: {int(self.score)}",antialias= True, color=(0,0,0))
            self.score_rect = self.score_surface.get_rect(center = (288,70))
            screen.blit(self.score_surface,self.score_rect)
            #GameOver
            self.game_over_surface = pygame.transform.scale2x(pygame.image.load(GAME_OVER_IMG_PATH))
            self.game_over_rect = self.game_over_surface.get_rect(center=(285,200))
            screen.blit(self.game_over_surface,self.game_over_rect)
            #Try_Again
            self.try_again_surface = pygame.transform.scale2x((pygame.image.load(TRY_AGAIN_IMG_PATH))).convert_alpha()
            self.try_again_rect = self.try_again_surface.get_rect(center=(285,450))
            screen.blit(self.try_again_surface,self.try_again_rect)
            #High_Score
            self.score_surface = self.game_font.render(f"High Score: {int(self.high_score)}",antialias= True, color=(0,0,0))
            self.score_rect = self.score_surface.get_rect(center = (288,700))
            screen.blit(self.score_surface,self.score_rect)


class Game:
    def __init__(self):
        pygame.mixer.pre_init(size = 16)
        pygame.init()
        self.screen = pygame.display.set_mode((576,900))
        self.game_active = True
        self.main_menu_status = True
        self.score_soundcnt = 100
        self.flap_sound = pygame.mixer.Sound(FLAP_SOUND_PATH)
        self.ply_hit_sound = pygame.mixer.Sound(PLY_HIT_SOUND_PATH)
        self.coin_sound = pygame.mixer.Sound(COIN_SOUND_PATH)
        self.clock = pygame.time.Clock()
        self.bg = Background()
        self.player = Player()
        self.pipe = Pipes()
        self.score = Scoreboard()
    def run(self)->None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    os.kill(os.getpid(),signal.SIGTERM)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.game_active == True:

                        self.player.bird_movement = 0
                        #for the default game 9 is good for 60fps
                        self.player.bird_movement -= 9 #12 when hard or 10 it's ok to handle it and if the game what to be easy set it to 5-8
                        self.flap_sound.play()
                    if event.button == 1 and self.game_active == False:
                        self.game_active = True
                        self.score.score = 0
                        self.pipe.pipe_lst.clear()
                        self.player.bird_rect.center = (100,450) #100,512
                        self.player.bird_movement = PLY_MOV
                        #self.player.
                        self.flap_sound.play()
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP and self.game_active == True:
                        self.player.bird_movement = 0
                        #for the default game 9 is good for 60fps
                        self.player.bird_movement -= 9 #12 when hard or 10 it's ok to handle it and if the game what to be easy set it to 5-8
                        self.flap_sound.play()
                    if event.key == pygame.K_SPACE and self.game_active == False:
                        self.game_active = True
                        self.score.score = 0
                        self.pipe.pipe_lst.clear()
                        self.player.bird_rect.center = (100,450) #100,512
                        self.player.bird_movement = PLY_MOV
                        #self.player.
                        self.flap_sound.play()
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
                self.game_active= self.pipe.check_collision(self.player.bird_rect,self.ply_hit_sound)
                self.score.score+=0.01
                self.score_soundcnt -= 1
                if self.score_soundcnt <= 0:
                    self.coin_sound.play()
                    self.score_soundcnt = 100
                #add the coin sound
                self.score.score_display("main_game",self.screen,self.coin_sound)     
            else:
                self.score.update_score()
                self.score.score_display("game_over",screen= self.screen)
                
    
            #floor
            self.bg.draw_floor(self.screen)

            pygame.display.update()
            self.clock.tick(FPS)

if  __name__   == "__main__":
    #print(__file__)
    game = Game()
    game.run()