import pygame
import sys
from settings import *
from resources import load_assets, IMAGES, SOUNDS
from entities import Player, Enemy
from world import Ground, Platform
import ui


def run_game(screen, clock):
    start_ticks = pygame.time.get_ticks()

    # 1. Gracz
    player = Player(IMAGES["PRAWO"], 100, HEIGHT)

    # 2. Przeciwnicy
    enemies_group = pygame.sprite.Group()
    dragon = Enemy(IMAGES["DRAGON"], WIDTH / 2, HEIGHT - 100, 500)
    enemies_group.add(dragon)
    fireballs_group = pygame.sprite.Group()

    # 3. Teren
    terrain_group = pygame.sprite.Group()
    grass = Ground(0, HEIGHT - 105, "GRASS")
    terrain_group.add(grass)

    # 4. Platformy
    platforms_group = pygame.sprite.Group()
    p1 = Platform(200, 550, 200, 50, "PLATFORM")
    p2 = Platform(600, 300, 200, 50, "PLATFORM")
    p3 = Platform(900, 650, 200, 50, "PLATFORM")
    platforms_group.add(p1, p2, p3)

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # --- Update ---
        keys_pressed = pygame.key.get_pressed()
        player.update(keys_pressed, platforms_group)

        # Atak gracza
        if player.attack_timer >= 19:
            for enemy in enemies_group:
                if player.attack_rect.colliderect(enemy.rect):
                    enemy.take_damage(player.damage)

        # Kolizje z wrogiem
        collided_enemy = pygame.sprite.spritecollideany(player, enemies_group)
        if collided_enemy:
            player.contact_timer += 1
            if player.contact_timer >= 45:
                player.take_damage()
        else:
            player.contact_timer = 0

        if player.invincible_timer > 0:
            player.invincible_timer -= 1

        # Kolizje z kulami ognia
        for ball in fireballs_group:
            if ball.rect.colliderect(player.rect):
                player.take_damage()
                ball.kill()
                SOUNDS["FIREBALL_END"].play()

        # Warunki końca gry
        if player.health <= 0:
            return "DEAD", 0
        if dragon.health <= 0:
            total_seconds = (pygame.time.get_ticks() - start_ticks) // 1000
            return "WIN", total_seconds

        # Update reszty
        enemies_group.update(player, fireballs_group)
        dragon.rotation("DRAGON2", "DRAGON")
        fireballs_group.update()

        # --- Draw ---
        screen.blit(IMAGES["BACKGROUND"], (0, 0))
        terrain_group.draw(screen)
        platforms_group.draw(screen)
        enemies_group.draw(screen)
        fireballs_group.draw(screen)
        player.draw(screen)

        ui.draw_player_hud(screen, player)
        if dragon.health > 0:
            ui.draw_enemy_hud(screen, dragon)

        pygame.display.flip()

    return "EXIT", 0


if __name__ == "__main__":
    # Inicjalizacja Pygame
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    # Ustawienie ekranu
    screen = pygame.display.set_mode(SIZESCREEN)
    pygame.display.set_caption("Hollow Knight")
    clock = pygame.time.Clock()

    # Wczytanie zasobów
    load_assets()

    # Start muzyki
    pygame.mixer.music.play(-1)

    state = "MENU"
    final_time = 0

    while state != "EXIT":
        if state == "MENU":
            if ui.main_menu(screen, clock):
                state = "GAME"
            else:
                state = "EXIT"

        elif state == "GAME":
            result, game_time = run_game(screen, clock)
            if result == "DEAD":
                state = "GAMEOVER"
            elif result == "WIN":
                final_time = game_time
                state = "VICTORY"
            else:
                state = "EXIT"

        elif state == "GAMEOVER":
            choice = ui.game_over_menu(screen, clock)
            if choice == "RESTART":
                state = "GAME"
            elif choice == "MENU":
                state = "MENU"
            else:
                state = "EXIT"

        elif state == "VICTORY":
            choice = ui.victory_menu(screen, clock, final_time)
            if choice == "MENU":
                state = "MENU"
            else:
                state = "EXIT"

    pygame.quit()
    sys.exit()