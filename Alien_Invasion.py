import pygame

from pygame.sprite import Group

from settings import setting

from ship import ship

import game_functions as gf

from game_stats import Game_Stats

from button import Button


def run_game():
    pygame.init()
    game = setting()
    screen = pygame.display.set_mode((game.screen_width, game.screen_height))
    pygame.display.set_caption("Alien Invation")
    player_ship = ship(game, screen)
    bullets = Group()
    aliens = Group()
    stats = Game_Stats(game)
    gf.create_fleet(game, screen, aliens, player_ship)
    play_button = Button(game, screen, "Al3eb")

    while True:
        gf.check_events(game, screen, player_ship, bullets, stats, play_button, aliens)
        if stats.game_active:
            player_ship.update()
            bullets.update()
            gf.update_bullet(game, screen, player_ship, aliens, bullets)
            gf.update_aliens(game, player_ship, aliens, stats, bullets, screen)
        gf.update_screen(game, screen, player_ship, bullets, aliens, play_button, stats)


run_game()
