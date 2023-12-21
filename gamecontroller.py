import pygame
import sys
from snake import Snake
from food import Food
from direction import Direction
import constants


class GameController:
    """Controls the game."""

    def __init__(self) -> None:
        """Create an object of type GameController."""
        self._clock = None
        self._snake = None
        self._food = None
        self._current_score = 0
        self._font = None
        self._display = None

    def run(self) -> None:
        """Run the game."""

        pygame.init()
        self.initialize_game()

        game_is_running = True
        while game_is_running:
            self._clock.tick(constants.FPS)

            # Handles when user moves Snake, engages
            # autopilot more, or quits game.
            self.handle_user_input()

            if self._game_ending_event():
                self._game_over_screen()
                self.restart_or_end_game()

            self.update_game_elements()
            self.update_display()

    def initialize_game(self) -> None:
        """Initialize the game."""

        self.initialize_display()

        # Initialize game clock, used to set FPS
        self._clock = pygame.time.Clock()

        self._current_score = 0

        # Add game objects
        self._snake = Snake(
            constants.SNAKE_SIZE_X_Y, constants.SNAKE_SIZE_X_Y, self._display
        )
        self._food = Food(
            constants.FOOD_SIZE_X_Y, constants.FOOD_SIZE_X_Y, self._display
        )

        self._font = pygame.font.SysFont(constants.GAME_FONT, constants.GAME_FONT_SIZE)

    def initialize_display(self) -> pygame.Surface:
        """Initialize the display.

        Returns:
            The display surface.
        """
        # Initialize display on which all game elements are drawn
        self._display = pygame.display.set_mode(constants.DISPLAY_X_Y_COORDINATES)

        # Add game title and background color
        pygame.display.set_caption("Snake Game")
        self._display.fill(constants.DISPLAY_BACKGROUND_COLOR)

    def handle_user_input(self) -> None:
        """Handle user input."""
        for event in pygame.event.get():
            self._quit_game(event)
            self._autopilot(event)
            self._user_direction_input(event)

    def update_game_elements(self) -> None:
        """Update the game elements each frame."""

        # Update the Snake each frame
        self._snake.update(self._food)

        # Check if Snake has collided with Food; if so, change position.
        if self._snake.has_collided_with_food(self._food):
            self._increase_score()

            while True:
                new_food_position = self._food.calculate_new_position()
                if new_food_position not in self._snake.get_snake_body():
                    self._food.update(new_food_position)
                    break

    def update_display(self) -> None:
        """Update the display each frame."""

        self._display.fill(constants.DISPLAY_BACKGROUND_COLOR)
        self._display_score()

        self._snake.draw()
        self._food.draw()
        pygame.display.flip()

    def _user_direction_input(self, event: pygame.event) -> None:
        """Check for keyboard input from user.

        Args:
            event: a pygame event object.
        """
        # Dictionary allow mapping current direction to opposite direction,
        # making it eaier to check if Snake attempts to move in opposite direction.
        if event.type == pygame.KEYDOWN:
            user_input_options = {
                pygame.K_UP: Direction.UP,
                pygame.K_DOWN: Direction.DOWN,
                pygame.K_LEFT: Direction.LEFT,
                pygame.K_RIGHT: Direction.RIGHT,
            }

            # Confirm direction input is valid AND assign value to "direction"
            if direction := user_input_options.get(event.key):
                self._snake.set_direction(direction)

    def _quit_game(self, event: pygame.event) -> None:
        """Quit the game."""
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def _autopilot(self, event: pygame.event) -> None:
        """Enable autopilot."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            self._snake._autopilot = not self._snake._autopilot

    def _display_score(self) -> None:
        """Display the current score on the screen."""
        # Render the text into a surface
        text_surface = self._font.render(
            f"SCORE: {self._current_score}", True, constants.GAME_TEXT_COLOR
        )

        # Draw the text surface at the correct position
        self._display.blit(text_surface, constants.CURRENT_SCORE_POS)

    def _increase_score(self) -> None:
        """Increase the score."""
        self._current_score += constants.FOOD_SCORE

    def _game_ending_event(self) -> bool:
        """Check if game-ending event has occurred.

        Returns:
            True if game-ending event has occurred, else False.
        """
        return (
            self._snake.has_collided_with_self() or self._snake.has_collided_with_wall()
        )

    def _game_over_screen(self) -> None:
        """Display the game-over screen."""

        # Set game-over scree
        self._display.fill(constants.DISPLAY_BACKGROUND_COLOR)

        # Render the text into a surface
        text_surface = self._font.render(
            f"Game Over. Score: {self._current_score}. Hit Space to Restart.",
            True,
            constants.GAME_TEXT_COLOR,
        )

        # Get the rectangle of the text surface
        text_rect = text_surface.get_rect()

        # Set the center of the text rectangle to the center of the screen
        text_rect.center = (constants.DISPLAY_WIDTH / 2, constants.DISPLAY_HEIGHT / 2)

        # Draw the text surface at the correct position
        self._display.blit(text_surface, text_rect.topleft)

        pygame.display.flip()

    def restart_or_end_game(self) -> None:
        """Offer options to restart or end game."""

        while True:
            for event in pygame.event.get():
                # If user closes window, game ends.
                self._quit_game(event)

                # If user hits space, restart game
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.initialize_game()  # Reinitialize the game
                    return
