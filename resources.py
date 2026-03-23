# resources.py
import pygame
import os

IMAGES = {}
SOUNDS = {}
FONTS = {}


def load_assets():
    path = os.path.join(os.getcwd(), "images")
    music_path = os.path.join("music", "music.wav")

    # 1. Grafiki
    file_names = os.listdir(path)

    if "background.png" in file_names:
        bg_image = pygame.image.load(os.path.join(path, "background.png")).convert()
        IMAGES["BACKGROUND"] = bg_image
        file_names.remove("background.png")

    # Reszta grafik
    for file_name in file_names:
        if not file_name.lower().endswith((".png", ".jpg", ".jpeg")):
            continue
        image_name = file_name[:-4].upper()
        image = pygame.image.load(os.path.join(path, file_name)).convert_alpha()
        IMAGES[image_name] = image

    # 2. Dźwięki i Muzyka
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(0.2)

    SOUNDS["ATTACK"] = pygame.mixer.Sound(os.path.join("music", "attack.wav"))
    SOUNDS["ATTACK"].set_volume(0.7)

    SOUNDS["FIREBALL"] = pygame.mixer.Sound(os.path.join("music", "fireball.wav"))
    SOUNDS["FIREBALL"].set_volume(0.7)

    SOUNDS["DRAGON_ATTACK"] = pygame.mixer.Sound(os.path.join("music", "dragon_attack.wav"))
    SOUNDS["DRAGON_ATTACK"].set_volume(0.7)

    SOUNDS["HIT"] = pygame.mixer.Sound(os.path.join("music", "hit.wav"))
    SOUNDS["HIT"].set_volume(0.7)

    SOUNDS["FIREBALL_END"] = pygame.mixer.Sound(os.path.join("music", "fireball_end.wav"))
    SOUNDS["FIREBALL_END"].set_volume(0.2)

    # 3. Czcionki
    FONTS["HUD"] = pygame.font.SysFont("Arial", 24, bold=True)
    FONTS["TITLE"] = pygame.font.SysFont("Arial", 80, bold=True)
    FONTS["OPTION"] = pygame.font.SysFont("Arial", 40)