import pygame
from pygame.locals import *
import random, time
 
pygame.init()
 
FPS = 60
FramePerSec = pygame.time.Clock()
 
# Predefined some colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
# Screen information
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5 
SPEED_p = 5
SCORE = 0
coins_score = 0
 
DISPLAYSURF = pygame.display.set_mode((400,600))

pygame.display.set_caption("Game")


font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)
coins_result = font_small.render("You have collected:      coins", True, BLACK)
score_result = font_small.render("Your score is: ", True, BLACK)
 
BACKGROUND = pygame.image.load("./resources/AnimatedStreet.png")

 
class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("resources/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center=(random.randint(40,SCREEN_WIDTH-40), 0) 
 
      def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.bottom > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)
 
 
 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("resources/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-SPEED_p, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(SPEED_p, 0)
 
 
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("./resources/coin.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(0, SCREEN_HEIGHT // 2))

    def appear(self):
        self.rect.top = 0
        self.rect.center = (random.randint(30, 370), 0)

    def move(self):
        self.rect.move_ip(0,SPEED)
        if (self.rect.bottom > 600):
            COIN.appear()




         
#Setting up Sprites        
P1 = Player()
E1 = Enemy()
COIN = Coin()
 
#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(COIN)

coins = pygame.sprite.Group()
coins.add(COIN)



done = False

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)
n = 1

#Game Loop
while not done:
       
    #Cycles through all events occuring  
    for event in pygame.event.get():
        if coins_score == 10 * n:
            if event.type == INC_SPEED:
                SPEED += 1
                SPEED_p += 1
                n += 1
                  
           
        if event.type == QUIT:
            done = True


    DISPLAYSURF.blit(BACKGROUND, (0, 0))
    scores = font_small.render(str(SCORE), True, BLACK)
    scores_coins = font_small.render(str(coins_score), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))
    DISPLAYSURF.blit(scores_coins, (SCREEN_WIDTH - 40,10))
 
    
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

 
    #To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
          DISPLAYSURF.fill(RED)
          DISPLAYSURF.blit(game_over, (30, 150))
          DISPLAYSURF.blit(score_result, (50, 250))
          DISPLAYSURF.blit(scores, (200, 250))
          DISPLAYSURF.blit(coins_result, (50, 350))
          DISPLAYSURF.blit(scores_coins, (250, 350))
          pygame.display.update()
          for entity in all_sprites:
                entity.kill() 
          time.sleep(3)
          done = True
    
    if pygame.sprite.spritecollideany(P1, coins):
        COIN.appear()
        coins_score += 1
              
    pygame.display.update()
    FramePerSec.tick(FPS)