import pygame
from pygame.sprite import Sprite


class RocketA(Sprite):
    """Klasa przeznaczona do zarządzania pociskiem bocznym A."""

    def __init__(self, li_game):
        """Utworzenie obiektu pocisku A w aktualnym położeniu."""
        super().__init__()
        self.screen = li_game.screen
        self.settings = li_game.settings
        self.color = li_game.settings.rocket_ab_color

        self.rect = pygame.Rect(0, 0, self.settings.rocket_ab_width,
                                self.settings.rocket_ab_height)
        self.rect.midbottom = li_game.ship.rect.midtop

        self.y = float(self.rect.y)

    def update(self):
        """Poruszanie pociskiem A po ekranie."""
        self.y -= self.settings.rockets_speed
        self.rect.y = self.y

    def draw_rocket_a(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
