import pygame
import random
from game_item import GameItem
from constants import FOOD_COLOR, FOOD_SIZE_X_Y, MAX_DISPLAY_WIDTH, MAX_DISPLAY_HEIGHT


class Food(GameItem):
    """Represents a Food object in the game."""

    def __init__(self, x: int, y: int, display: pygame.Surface) -> None:
        """Create an object of type Food.

        Args:
            x: the food's x-coordinate in 2D space.
            y: the food's y-coordinate in 2D space.
            display: the surface on which the Food object is drawn.
        """
        super().__init__(x, y, display)
        self._position = (x, y)

    def update(self, new_position: tuple[int, int]) -> None:
        """Change location of the Food object."""
        self._x, self._y = new_position

    def draw(self) -> pygame.Rect:
        """Draw the Food object to the display.

        Returns:
            A pygame Rect object, which can be drawn to the pygame surface.
        """
        return pygame.draw.rect(
            surface=self._display,
            color=FOOD_COLOR,
            rect=(self._x, self._y, FOOD_SIZE_X_Y, FOOD_SIZE_X_Y),
        )

    def calculate_new_position(self) -> tuple[int, int]:
        """Create a random x-y position located within display boundaries.

        Returns:
            A tuple containing randomized x-y coordinates.
        """
        x = random.randint(0, int(MAX_DISPLAY_WIDTH)) * FOOD_SIZE_X_Y
        y = random.randint(0, int(MAX_DISPLAY_HEIGHT)) * FOOD_SIZE_X_Y

        return (x, y)

    def get_current_position(self) -> tuple[int, int]:
        """Return the x-y position of the Food object."""
        return (self._x, self._y)
