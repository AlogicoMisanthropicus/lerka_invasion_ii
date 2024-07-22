import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """
    Klasa przeznaczona do zarządzania pociskami (przednimi) wystrzelonymi
    przez statek.
    """

    def __init__(self, li_game):
        """Utworzenie obiektu pocisku w aktualnym położeniu."""
        super().__init__()
        self.screen = li_game.screen
        self.settings = li_game.settings
        self.color = li_game.settings.bullet_color

        # Utworzenie prostokąta pocisku w punkcie (0, 0), a następnie
        # zdefiniowanie dla niego odpowiedniego położenia.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midright = li_game.ship.rect.midright

        # Położenie pocisku jest zdefiniowane za
        # pomocą wartości zmiennoprzecinkowej.
        self.x = float(self.rect.x)

    def update(self):
        """Poruszanie pociskiem po ekranie."""
        # Uaktualnienie położenia pocisku.
        self.x += self.settings.bullet_speed
        # Uaktualnienie położenia prostokąta pocisku.
        self.rect.x = self.x

    def draw_bullet(self):
        """Wyświetlenie pocisku na ekranie."""
        pygame.draw.rect(self.screen, self.color, self.rect)
