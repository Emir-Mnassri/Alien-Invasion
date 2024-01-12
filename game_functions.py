import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_key_down(event, ai_settings, screen, ship, bullets, stats, aliens):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_p:
        start_game(ai_settings, screen, stats, aliens, bullets, ship)


def fire_bullets(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_key_up(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_q:
        sys.exit()


def check_events(ai_settings, screen, ship, bullets, stats, play_button, aliens):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_key_down(event, ai_settings, screen, ship, bullets, stats, aliens)
        elif event.type == pygame.KEYUP:
            check_key_up(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, mouse_x, mouse_y, stats, play_button, aliens, bullets, ship)


def start_game(ai_settings, screen, stats, aliens, bullets, ship):
    stats.reset_stats()
    aliens.empty()
    bullets.empty()
    stats.game_active = True
    pygame.mouse.set_visible(0)
    create_fleet(ai_settings, screen, aliens, ship)
    ship.center_ship()


def check_play_button(ai_settings, screen, mouse_x, mouse_y, stats, play_button, aliens, bullets, ship):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        pygame.mouse.set_visible(0)
        stats.reset_stats()
        stats.game_active = True
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()


def update_screen(game, screen, player_ship, bullets, aliens, player_button, stats):
    screen.fill(game.bg_color)
    player_ship.blitme()
    aliens.draw(screen)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    if not stats.game_active:
        player_button.draw_button()
    pygame.display.flip()


def update_bullet(ai_settings, screen, ship, aliens, bullets):
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_alien_bullet_collision(ai_settings, screen, ship, aliens, bullets)


def check_alien_bullet_collision(ai_settings, screen, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens) == 0:
        bullets.empty()
        create_fleet(ai_settings, screen, aliens, ship)


def get_number_alien_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - alien_width * 2
    number_aliens_x = available_space_x // (alien_width * 2)
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    available_screen_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = available_screen_y // (alien_height * 2)
    return number_rows


def create_alien(screen, ai_settings, aliens, number_alien, row):
    alien = Alien(screen, ai_settings)
    alien_width = alien.rect.width
    alien.rect.x = alien_width + alien_width * 2 * number_alien
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row
    aliens.add(alien)


def create_fleet(ai_settings, screen, aliens, ship):
    alien = Alien(screen, ai_settings)
    number_aliens_x = get_number_alien_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    for row in range(number_rows):
        for number_alien in range(number_aliens_x):
            create_alien(screen, ai_settings, aliens, number_alien, row)


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, ship, aliens, stats, bullets, screen):
    if stats.ship_left > 1:
        stats.ship_left -= 1
        aliens.empty()
        bullets.empty()
        ship.center_ship()
        sleep(0.5)
        create_fleet(ai_settings, screen, aliens, ship)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(1)


def check_alien_bottom(ai_settings, ship, aliens, stats, bullets, screen):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, ship, aliens, stats, bullets, screen)
            break


def update_aliens(ai_settings, ship, aliens, stats, bullets, screen):
    check_fleet_edges(ai_settings, aliens)
    for alien in aliens:
        alien.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, ship, aliens, stats, bullets, screen)
    check_alien_bottom(ai_settings, ship, aliens, stats, bullets, screen)
