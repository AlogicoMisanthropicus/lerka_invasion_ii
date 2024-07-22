import json


class GameStats:
    """Monitorowanie danych statystycznych w grze "Lerka Invasion"."""

    def __init__(self, ai_game):
        """Inicjalizacja danych statystycznych."""
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False
        self.show_help = False
        self.high_score = self.get_old_high_score()

    def get_old_high_score(self):
        """Pobiera najlepszy wynik z pliku - jeżeli istnieje."""
        try:
            with open('high_score.json') as f:
                return json.load(f)
        except FileNotFoundError:
            return 0

    def reset_stats(self):
        """
        Inicjalizacja danych statystycznych, które mogą zmieniać
        się w trakcie gry.
        """
        self.ships_left = self.settings.ship_limit
        self.lerka_hit = 0
        self.score = 0
        self.level = 1
