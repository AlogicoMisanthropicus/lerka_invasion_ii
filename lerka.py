import pygame
from pygame.sprite import Sprite

from ships_image import ShipsImage


class Lerka(Sprite):
    """Klasa przedstawiająca jednego Lerkę we flocie."""

    def __init__(self, li_game):
        """Inicjalizacja Lerki i zdefiniowanie jego położenia."""
        super().__init__()
        self.screen = li_game.screen
        self.settings = li_game.settings
        self.screen_rect = li_game.screen.get_rect()

        self.image = pygame.image.load('images/lerka.bmp')
        self.rect = self.image.get_rect()

        self.ship_image = ShipsImage(self)

        self.rect.topright = self.screen_rect.topright
        self.y = self.rect.y

    def check_edges(self):
        """Returns True if Lerka touches edge of the screen.
        Zwraca wartość True, jeśli Lerka znajduje się przy krawędzi ekranu.
        """
        screen_rect = self.screen.get_rect()
        if self.rect.bottom >= screen_rect.height or (self.rect.top <=
                                            self.ship_image.rect.bottom + 10):
            return True

    def update(self):
        """Przesunięcie Lerki w stronę statku zygzakiem."""
        self.y += self.settings.lerka_speed_y * self.settings.fleet_direction
        self.rect.y = self.y
        self.x -= self.settings.lerka_speed_x
        self.rect.x = self.x
