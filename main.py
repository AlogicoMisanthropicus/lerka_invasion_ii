import json
import pygame
import sys

from time import sleep
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from rocket_a import RocketA
from rocket_b import RocketB
from lerka import Lerka
from help import Help


class LerkaInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game and create its resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_width = self.screen.get_rect().width
        self.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("LERKA Invasion")

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.help = Help(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.lerkas = pygame.sprite.Group()
        self.rockets_a = pygame.sprite.Group()
        self.rockets_b = pygame.sprite.Group()

        self._create_fleet()

        self.play_button = Button(self, "LERKA Invasion")

        self._make_difficulty_buttons()

    def _make_difficulty_buttons(self):
        """Creates difficulty buttons."""
        self.easy_button = Button(self, "Easy")
        self.medium_button = Button(self, "Medium")
        self.hard_button = Button(self, "HELL")
        self.help_button = Button(self, "Help")

        self.easy_button.rect.top = (
                self.play_button.rect.top + 2.5 * self.play_button.rect.height)
        self.easy_button.update_msg_position()

        self.medium_button.rect.top = (
                self.easy_button.rect.top + 1.5 * self.play_button.rect.height)
        self.medium_button.update_msg_position()

        self.hard_button.rect.top = (
                self.medium_button.rect.top + 1.5 *
                self.play_button.rect.height)
        self.hard_button.update_msg_position()

        self.help_button.rect.bottom = (
                self.play_button.rect.top - 1.5 * self.play_button.rect.height)
        self.help_button.update_msg_position()

    def run_game(self):
        """Start the main loop of the game."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_lerkas()
                self._update_rockets_a()
                self._update_rockets_b()

            self._update_screen()

    def _check_events(self):
        """Respond to key presses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._exit_game()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_difficulty_buttons(mouse_pos)
                self._check_help_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks 'LERKA INVASION'
        button."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()

    def _check_difficulty_buttons(self, mouse_pos):
        """Sets the selected difficulty level."""
        easy_button_clicked = self.easy_button.rect.collidepoint(mouse_pos)
        medium_button_clicked = self.medium_button.rect.collidepoint(mouse_pos)
        hard_button_clicked = self.hard_button.rect.collidepoint(mouse_pos)

        if easy_button_clicked:
            self.settings.difficulty_level = 'easy'
        elif medium_button_clicked:
            self.settings.difficulty_level = 'medium'
        elif hard_button_clicked:
            self.settings.difficulty_level = 'hard'

    def _check_help_button(self, mouse_pos):
        help_button_clicked = self.help_button.rect.collidepoint(mouse_pos)
        if help_button_clicked:
            if not self.stats.show_help:
                self.stats.show_help = True
            elif self.stats.show_help:
                self.stats.show_help = False

    def _create_help_window(self):
        self.help.show_help_window()

    def _check_keydown_events(self, event):
        """Reacts to key presses."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_q:
            self._exit_game()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_LCTRL:
            self._fire_rocket_a()
            self._fire_rocket_b()
        elif event.key == pygame.K_g:
            if not self.stats.game_active:
                self._start_game()

    def _check_keyup_events(self, event):
        """Reacts to key releases."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

    def _start_game(self):
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.stats.game_active = True
        self.stats.show_help = False
        self.sb.prep_images()
        self._emptying_all_bullets_lerkas()
        self._create_fleet()
        self.ship.center_ship()
        pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        """Create new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed and (
                self.stats.game_active):
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.screen_width:
                self.bullets.remove(bullet)

        self._check_bullet_lerka_collisions()

    def _check_bullet_lerka_collisions(self):
        """Respond to bullet-Lerka collisions."""
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.lerkas, True, True)
        self._when_collisions(collisions)
        self._lerkas_end()

    def _fire_rocket_a(self):
        """Create a new rocket A and add it to the rockets A group."""
        if len(self.rockets_a) < self.settings.rockets_allowed and (
                self.stats.game_active):
            new_rocket_a = RocketA(self)
            self.rockets_a.add(new_rocket_a)

    def _update_rockets_a(self):
        """Update position of rockets A and get rid of old rockets A."""
        self.rockets_a.update()

        for rocket_a in self.rockets_a.copy():
            if rocket_a.rect.bottom <= 0:
                self.rockets_a.remove(rocket_a)

        self._check_rocket_a_lerka_collisions()

    def _check_rocket_a_lerka_collisions(self):
        """Respond to rocket A-Lerka collisions."""
        collisions = pygame.sprite.groupcollide(
            self.rockets_a, self.lerkas, True, True)
        self._when_collisions(collisions)
        self._lerkas_end()

    def _fire_rocket_b(self):
        """Create a new rocket B and add it to the rockets B group."""
        if len(self.rockets_b) < self.settings.rockets_allowed and (
                self.stats.game_active):
            new_rocket_b = RocketB(self)
            self.rockets_b.add(new_rocket_b)

    def _update_rockets_b(self):
        """Update position of rockets B and get rid of old rockets B."""
        self.rockets_b.update()

        for rocket_b in self.rockets_b.copy():
            if rocket_b.rect.top >= self.screen_height:
                self.rockets_b.remove(rocket_b)

        self._check_rocket_b_lerka_collisions()

    def _check_rocket_b_lerka_collisions(self):
        """Respond to rocket B-Lerka collisions."""
        collisions = pygame.sprite.groupcollide(
            self.rockets_b, self.lerkas, True, True)
        self._when_collisions(collisions)
        self._lerkas_end()

    def _when_collisions(self, collision):
        collisions = collision

        if collisions:
            for lerkas in collisions.values():
                self.stats.score += self.settings.lerka_points * len(lerkas)
            self.sb.prep_score()
            self.sb.check_high_score()

    def _update_lerkas(self):
        """Check if the fleet is at an edge,
          then update the positions of all Lerkas in the fleet."""
        self._check_fleet_edges()
        self.lerkas.update()
        # Look for Lerka-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.lerkas):
            self._ship_hit()

        self._check_lerkas_left_scr()

    def _emptying_all_bullets_lerkas(self):
        self.lerkas.empty()
        self.bullets.empty()
        self.rockets_a.empty()
        self.rockets_b.empty()

    def _lerkas_end(self):
        """Actions after shooting down the Lerkas fleet: getting rid of
        missiles, creating a new fleet, increasing speed and level, etc."""
        if not self.lerkas:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self.rockets_a.empty()
            self.rockets_b.empty()
            self._create_fleet()
            # Ruch na początku rundy (w zależności od tego, gdzie zakończył
            # się w poprzedniej rundzie lub zawsze w dół):
            self.settings.fleet_direction *= -1
            self.settings.increase_speed()

            self.stats.level += 1
            self.sb.prep_level()

    def _create_fleet(self):
        """Create a full fleet of Lerkas."""
        # Create a Lerka and find the number of Lerkas in a row.
        # Spacing between each Lerka is equal to one Lerka width.
        lerka = Lerka(self)
        lerka_height, lerka_width = lerka.rect.size
        available_space_y = self.screen_height - 2 * lerka_height
        number_lerkas_y = available_space_y // (2 * lerka_height)
        if number_lerkas_y >= 5:
            number_lerkas_y = 5

        # Determine the numer of rows of Lerkas that fit on the screen.
        ship_width = self.ship.rect.width
        available_space_x = (self.screen_width -
                             (5 * lerka_width) - ship_width)
        number_rows = available_space_x // (2 * lerka_width)

        for row_number in range(number_rows):
            for lerka_number in range(number_lerkas_y):
                self._create_lerka(lerka_number, row_number)

    def _create_lerka(self, lerka_number, row_number):
        """Create a Lerka and place it in the row."""
        lerka = Lerka(self)
        lerka_height, lerka_width = lerka.rect.size
        # lerka.y = (lerka_height + 2 * lerka_height * lerka_number)
        # lerka.y = (2 * lerka_height * lerka_number + random_number)
        lerka.y = lerka_height + 2 * lerka_height * lerka_number
        lerka.rect.y = lerka.y
        lerka.x = ((self.screen_width + 5 * lerka.rect.width)
                   - 2 * lerka.rect.width * row_number)
        lerka.rect.x = lerka.x
        self.lerkas.add(lerka)

    def _check_fleet_edges(self):
        """Respond appropriately if any Lerkas have reached an edge."""
        for lerka in self.lerkas.sprites():
            if lerka.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Change the fleet's direction."""
        # for lerka in self.lerkas.sprites():
        #    lerka.rect.y -= self.settings.lerka_speed_y
        # ^NIE WIEM, PO CO KIEDYŚ DAŁEM TE DWIE LINIE
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Respond to the ship being hit by a Lerka."""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.lerkas.empty()
            self.bullets.empty()
            self.rockets_a.empty()
            self.rockets_b.empty()
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.8)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_lerkas_left_scr(self):
        screen_rect = self.screen.get_rect()
        for lerka in self.lerkas.sprites():
            if lerka.rect.left <= (screen_rect.left - 0.5 * lerka.rect.height):
                self._ship_hit()
                break

    def _exit_game(self):
        """Saves highscore and exits the game."""
        old_high_score = self.stats.get_old_high_score()
        if self.stats.high_score > old_high_score:
            with open('high_score.json', 'w') as f:
                json.dump(self.stats.high_score, f)

        sys.exit()

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        # Refreshing the screen during each iteration of the loop.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for rocket_a in self.rockets_a.sprites():
            rocket_a.draw_rocket_a()
        for rocket_b in self.rockets_b.sprites():
            rocket_b.draw_rocket_b()
        self.lerkas.draw(self.screen)

        self.sb.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()
            self.easy_button.draw_button()
            self.medium_button.draw_button()
            self.hard_button.draw_button()
            self.help_button.draw_button()
            if self.stats.show_help:
                self._create_help_window()

        # Displays the most recently modified screen.
        pygame.display.flip()


if __name__ == '__main__':
    li = LerkaInvasion()
    li.run_game()
