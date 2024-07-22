import pygame
from pygame.sprite import Sprite


class ShipsImage(Sprite):
    """..."""

    def __init__(self, li_game):
        """..."""
        super().__init__()
        self.screen = li_game.screen
        self.settings = li_game.settings
        self.screen_rect = self.screen.get_rect()

        self.image = pygame.image.load('images/ship2.bmp')
        self.rect = self.image.get_rect()
