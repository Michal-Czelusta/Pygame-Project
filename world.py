import pygame
from resources import IMAGES

class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y, image_key):
        super().__init__()
        self.image = IMAGES[image_key]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_name):
        super().__init__()
        self.image = pygame.transform.scale(IMAGES[image_name], (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)