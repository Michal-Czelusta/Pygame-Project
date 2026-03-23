import pygame
import datetime
from settings import *
from resources import IMAGES, FONTS


def draw_player_hud(surface, player):
    original_heart = IMAGES["HEARTS"]
    new_size = (original_heart.get_width() * 3, original_heart.get_height() * 3)
    big_heart = pygame.transform.scale(original_heart, new_size)

    start_x = 20
    start_y = 20
    gap = new_size[0] + 10

    for i in range(player.health):
        surface.blit(big_heart, (start_x + i * gap, start_y))


def draw_enemy_hud(surface, enemy):
    bar_width = 300
    bar_height = 20
    padding = 20

    x = WIDTH - bar_width - padding
    y = padding

    health_ratio = enemy.health / enemy.max_health
    if health_ratio < 0: health_ratio = 0

    pygame.draw.rect(surface, (50, 50, 50), (x, y, bar_width, bar_height))
    pygame.draw.rect(surface, (200, 0, 0), (x, y, int(bar_width * health_ratio), bar_height))
    pygame.draw.rect(surface, WHITE, (x, y, bar_width, bar_height), 2)

    label = FONTS["HUD"].render("SMOK", True, WHITE)
    surface.blit(label, (x, y + bar_height + 5))


def save_score(time_seconds):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("scores.txt", "a") as file:
        file.write(f"[{now}] Pokonano smoka! Czas: {time_seconds} sekund\n")


def main_menu(screen, clock):
    options = ["START GRY", "WYJŚCIE"]
    selected_index = 0

    while True:
        clock.tick(FPS)
        screen.blit(IMAGES["BACKGROUND"], (0, 0))

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        title_text = FONTS["TITLE"].render("Hollow Knight", True, RED)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(title_text, title_rect)

        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected_index else WHITE
            text = FONTS["OPTION"].render(option, True, color)
            rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 60))
            screen.blit(text, rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return selected_index == 0
    return False


def game_over_menu(screen, clock):
    options = ["ZAGRAJ PONOWNIE", "MENU GŁÓWNE", "WYJŚCIE"]
    selected_index = 0

    while True:
        clock.tick(FPS)

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(5)
        overlay.fill((20, 0, 0))
        screen.blit(overlay, (0, 0))

        title_text = FONTS["TITLE"].render("KONIEC GRY", True, RED)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(title_text, title_rect)

        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected_index else WHITE
            text = FONTS["OPTION"].render(option, True, color)
            rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 60))
            screen.blit(text, rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "EXIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected_index == 0: return "RESTART"
                    if selected_index == 1: return "MENU"
                    if selected_index == 2: return "EXIT"


def victory_menu(screen, clock, final_time):
    save_score(final_time)
    options = ["MENU GŁÓWNE", "WYJŚCIE"]
    selected_index = 0

    while True:
        clock.tick(FPS)
        screen.blit(IMAGES["BACKGROUND"], (0, 0))

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(100)
        overlay.fill(GOLD)
        screen.blit(overlay, (0, 0))

        title_text = FONTS["TITLE"].render("ZWYCIĘSTWO!", True, GREEN)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(title_text, title_rect)

        time_text = FONTS["OPTION"].render(f"Twój czas: {final_time} sekund", True, BLACK)
        time_rect = time_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        screen.blit(time_text, time_rect)

        save_text = FONTS["OPTION"].render("Wynik zapisano do scores.txt", True, (0, 0, 150))
        save_rect = save_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
        screen.blit(save_text, save_rect)

        for i, option in enumerate(options):
            color = RED if i == selected_index else BLACK
            text = FONTS["OPTION"].render(option, True, color)
            rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120 + i * 60))
            screen.blit(text, rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "EXIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected_index == 0: return "MENU"
                    if selected_index == 1: return "EXIT"