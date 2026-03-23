import pygame
import math
from settings import *
from resources import IMAGES, SOUNDS

class Entity(pygame.sprite.Sprite):
    def __init__(self, image, x, y, health):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.health = health
        self.max_health = health

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0


class Player(Entity):
    def __init__(self, player_image, cx, cy):
        super().__init__(player_image, cx, cy, 3)
        self.damage = 50

        # Ruch i fizyka
        self.vel_y = 0
        self.on_ground = False
        self.facing = 1

        # Atak
        self.is_attacking = False
        self.attack_duration = 20
        self.attack_timer = 0
        self.attack_rect = pygame.Rect(0, 0, 50, 40)
        self.attack_cooldown = 15
        self.attack_cd_timer = 0

        self.contact_timer = 0
        self.invincible_timer = 0

    def take_damage(self, amount=1):
        if self.invincible_timer <= 0:
            SOUNDS["HIT"].play()
            super().take_damage(amount)
            self.invincible_timer = 100
            self.contact_timer = 0

    def update(self, keys_pressed, platforms):
        self._handle_input(keys_pressed)
        self._manage_attack()
        self._physics(platforms)
        self._animations()
        self._clamp_to_screen()

    def _handle_input(self, keys_pressed):
        if keys_pressed[pygame.K_z]:
            if not self.is_attacking and self.attack_cd_timer <= 0:
                self.attack()

        if keys_pressed[pygame.K_LEFT]:
            self.rect.x -= SPEED
            self.facing = -1
        if keys_pressed[pygame.K_RIGHT]:
            self.rect.x += SPEED
            self.facing = 1

        if keys_pressed[pygame.K_UP] and self.on_ground:
            self.vel_y = JUMP_HEIGHT
            self.on_ground = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def _physics(self, platforms):
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        if self.vel_y > 0:
            hits = pygame.sprite.spritecollide(self, platforms, False)
            for plat in hits:
                if self.rect.bottom <= plat.rect.bottom:
                    self.rect.bottom = plat.rect.top
                    self.vel_y = 0
                    self.on_ground = True

        if self.rect.bottom >= HEIGHT - 100:
            self.rect.bottom = HEIGHT - 100
            self.vel_y = 0
            self.on_ground = True

    def attack(self):
        self.is_attacking = True
        self.attack_timer = self.attack_duration
        SOUNDS["ATTACK"].play()

    def _manage_attack(self):
        if self.is_attacking:
            self.attack_timer -= 1
            if self.facing == 1:
                self.attack_rect.midleft = self.rect.midright
            else:
                self.attack_rect.midright = self.rect.midleft

            if self.attack_timer <= 0:
                self.is_attacking = False
                self.attack_cd_timer = self.attack_cooldown

        if self.attack_cd_timer > 0:
            self.attack_cd_timer -= 1

    def _animations(self):
        side = "PRAWO" if self.facing == 1 else "LEWO"

        if self.is_attacking:
            frames = [IMAGES[f"ATAK{i}{side}"] for i in range(4, 0, -1)]
            if self.attack_timer == 0:
                self.image = IMAGES["PRAWO" if self.facing == 1 else "LEWO"]
            else:
                idx = self.attack_timer // 5
                idx = min(idx, len(frames) - 1)
                self.image = frames[idx]
            return

        if not self.on_ground:
            if f"SKOK{side}" in IMAGES:
                self.image = IMAGES[f"SKOK{side}"]
            return

        self.image = IMAGES[f"{side}"]

    def _clamp_to_screen(self):
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > WIDTH: self.rect.right = WIDTH


class Enemy(Entity):
    def __init__(self, image, x, y, health):
        super().__init__(image, x, y, health)
        self.direction = -1
        self.speed = 3
        self.stop_distance = 60
        self.shoot_delay = 60
        self.shoot_timer = 0

    def take_damage(self, amount):
        super().take_damage(amount)
        if self.health <= 0:
            self.kill()

    def update(self, player, fireball_group):
        self.direction = 1 if (self.rect.centerx < player.rect.centerx) else -1

        if player.rect.bottom == HEIGHT - 100:
            dx = player.rect.centerx - self.rect.centerx
            distance = abs(dx)
            if distance > self.stop_distance:
                if dx > 0:
                    self.rect.x += self.speed
                else:
                    self.rect.x -= self.speed

        is_player_high = player.rect.bottom < HEIGHT - 200
        if is_player_high:
            if self.shoot_timer > 0:
                self.shoot_timer -= 1
            else:
                self.shoot(fireball_group, player)
                self.shoot_timer = self.shoot_delay

    def shoot(self, fireball_group, target):
        SOUNDS["FIREBALL"].play()
        new_fireball = Fireball(
            self.rect.centerx,
            self.rect.centery,
            target.rect.centerx,
            target.rect.centery)
        fireball_group.add(new_fireball)

    def rotation(self, lewo, prawo):
        self.image = IMAGES[f"{lewo}"] if self.direction == -1 else IMAGES[f"{prawo}"]


class Fireball(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, target_x, target_y):
        super().__init__()
        original_image = IMAGES["FIREBALL"]
        orig_w, orig_h = original_image.get_size()
        self.image = pygame.transform.scale(original_image, (orig_w * 2, orig_h * 2))

        self.rect = self.image.get_rect()
        self.rect.center = (start_x, start_y)

        speed = 10
        dx = target_x - start_x
        dy = target_y - start_y
        angle = math.atan2(dy, dx)

        self.vel_x = math.cos(angle) * speed
        self.vel_y = math.sin(angle) * speed
        self.pos_x = float(start_x)
        self.pos_y = float(start_y)

    def update(self):
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y
        self.rect.centerx = int(self.pos_x)
        self.rect.centery = int(self.pos_y)

        if (self.rect.right < -50 or self.rect.left > WIDTH + 50 or
                self.rect.bottom < -50 or self.rect.top > HEIGHT + 50):
            self.kill()