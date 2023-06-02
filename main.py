import pygame
import random
import pyautogui

pygame.init()

#----Display----
WIDTH, HEIGHT = 800, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game")

#----Colors----
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#----Images----
dino_img = pygame.image.load("dino.png")
cactus_img = pygame.image.load("cactus.png")

#----Size----
dino_width = 64
dino_height = 64
cactus_width = 32
cactus_height = 64

#----Resize the images----
dino_img = pygame.transform.scale(dino_img, (dino_width, dino_height))
cactus_img = pygame.transform.scale(cactus_img, (cactus_width, cactus_height))

#----The game clock----
clock = pygame.time.Clock()

#----Dino class----
class Dino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = dino_img
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT - self.rect.height
        self.jump_height = 100
        self.is_jumping = False
        self.jump_count = 10

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True

    def update(self):
        if self.is_jumping:
            if self.jump_count >= -10:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.rect.y -= (self.jump_count ** 2) * 0.5 * neg
                self.jump_count -= 1
            else:
                self.is_jumping = False
                self.jump_count = 10
                self.rect.y = HEIGHT - self.rect.height

#----Cactus class----
class Cactus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = cactus_img
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = HEIGHT - self.rect.height

    def update(self):
        self.rect.x -= 5
        if self.rect.x < -self.rect.width:
            self.rect.x = WIDTH
            self.rect.y = HEIGHT - self.rect.height

#----Create sprite groups----
all_sprites = pygame.sprite.Group()
cacti = pygame.sprite.Group()
cactus_cooldown = 0

#----Create Dino object----
dino = Dino()
all_sprites.add(dino)

#----Game loop----
running = True
while running:

    #----Process events----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                dino.jump()
                pyautogui.press('space')

    all_sprites.update()
    cacti.update()

    #----Check for collisions----
    if pygame.sprite.spritecollide(dino, cacti, False):
        #----Autoplay----
        #----Jump when cacti are present----
        #dino.jump()
        #pyautogui.press('space')

        #----No Autoplay----
        running = False
        pygame.quit()

    #----Draw----
    screen.fill(WHITE)
    all_sprites.draw(screen)
    cacti.draw(screen)

    #----Spawn cacti----
    if cactus_cooldown == 0 and random.randrange(100) < 1:
        cactus = Cactus()
        all_sprites.add(cactus)
        cacti.add(cactus)
        cactus_cooldown = 60  #Set the cooldown period to 60 frames

    #----Update the cooldown period----
    if cactus_cooldown > 0:
        cactus_cooldown -= 1

    #----Clean up cacti that have moved off the screen----
    for cactus in cacti:
        if cactus.rect.right < 0:
            cacti.remove(cactus)
            all_sprites.remove(cactus)

    #----Update the display----
    pygame.display.update()
    clock.tick(30)

pygame.quit()