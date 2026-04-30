import pygame, sys
from pygame.locals import *
import random, time
import os

pygame.init()

fps = 60
frame_per_sec = pygame.time.Clock()

screen_width = 400
screen_height = 600
speed = 5
score = 0
coin_count = 0
coins_collected = 0 

font_small = pygame.font.SysFont("Verdana", 20)
game_over_text = pygame.font.SysFont("Verdana", 60).render("Game Over", True, (0,0,0))

script_dir = os.path.dirname(os.path.abspath(__file__))

try:
    background_image = pygame.image.load(os.path.join(script_dir, "Images", "AnimatedStreet.png"))
except:
    background_image = pygame.Surface((400, 600))
    background_image.fill((255,255,255))

display_surface = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Racer")

try:
    pygame.mixer.music.load(os.path.join(script_dir, "Music", "pr10_racer_music_back music.wav"))
    pygame.mixer.music.play(-1)
except:
    pass

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load(os.path.join(script_dir, "Images", "Enemy.png"))
        except:
            self.image = pygame.Surface((50, 50))
            self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, screen_width - 40), 0)
    
    def move(self):
        global score
        self.rect.move_ip(0, speed)
        if self.rect.top > 600:
            score += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, screen_width - 40), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load(os.path.join(script_dir, "Images", "Player.png"))
        except:
            self.image = pygame.Surface((50, 50))
            self.image.fill((0,255,0))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
    
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < screen_width and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.weight = random.choice([1, 2, 3]) 
        self.image = pygame.Surface((20, 20))
        colors = {1: (205,127,50), 2: (192,192,192), 3: (255,215,0)}
        self.image.fill(colors[self.weight])
        pygame.draw.circle(self.image, (255,255,255), (10,10), 8, 1)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, screen_width - 40), 0)
    
    def move(self):
        self.rect.move_ip(0, speed)
        if self.rect.top > screen_height:
            self.kill()

player = Player()
enemy = Enemy()
enemies = pygame.sprite.Group()
enemies.add(enemy)
coins = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player, enemy)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    if random.randint(1, 30) == 1:
        new_coin = Coin()
        coins.add(new_coin)
        all_sprites.add(new_coin)
    
    player.move()
    display_surface.blit(background_image, (0, 0))
    display_surface.blit(font_small.render(f"Score: {score}", True, (0,0,0)), (10, 10))
    display_surface.blit(font_small.render(f"Coins: {coin_count}", True, (0,0,0)), (380, 10))
    display_surface.blit(font_small.render(f"Speed: {speed:.1f}", True, (0,0,0)), (10, 30))
    
    for coin in pygame.sprite.spritecollide(player, coins, True):
        coin_count += coin.weight
        coins_collected += 1
        if coins_collected >= 3:
            speed += 0.5
            coins_collected = 0
    
    for entity in all_sprites:
        display_surface.blit(entity.image, entity.rect)
        entity.move()
    
    if pygame.sprite.spritecollideany(player, enemies):
        try:
            pygame.mixer.Sound(os.path.join(script_dir, "Music", "pr10_racer_music_crash.wav")).play()
        except:
            pass
        time.sleep(0.5)
        display_surface.fill((255,0,0))
        display_surface.blit(game_over_text, (30, 250))
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()
    
    pygame.display.update()
    frame_per_sec.tick(fps)