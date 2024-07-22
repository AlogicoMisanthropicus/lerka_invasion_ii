import pygame


class Help:
    """Klasa przeznaczona do wyświetlania pomocy."""

    def __init__(self, li_game):
        """Inicjalizacja atrybutów pomocy."""
        self.screen = li_game.screen
        self.screen_rect = self.screen.get_rect()

        self.image = pygame.image.load('images/help.bmp')
        self.rect = self.image.get_rect()

        self.rect.midleft = self.screen_rect.midleft
        self.rect.x = 20
        self.y = self.rect.y
        self.x = self.rect.x

    def show_help_window(self):
        """Wyświetlenie pomocy."""
        self.screen.blit(self.image, self.rect)
