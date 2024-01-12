import pygame
# a class that represents a ships


class ship():
    def __init__(self, game, screen):
        # the starting position of the ship
        self.screen = screen
        self.game = game
        self.image = pygame.image.load("C:\Projects\Alien Invation\images\ship.png")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)
        self.moving_right = False
        self.moving_left = False

    def update(self):

        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.game.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.game.ship_speed_factor
        self.rect.centerx = self.center

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.center = self.screen_rect.centerx
