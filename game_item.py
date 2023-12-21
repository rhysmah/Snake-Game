import pygame
from abc import abstractmethod


class GameItem:
    """Represents a GameItem object in the game."""

    def __init__(self, x: int, y: int, display: pygame.Surface) -> None:
        """Create an object of type GameItem.

        Args:
            x: the x-coordinate of the GameItem object in 2D space.
            y: the y-coordinate of the GameItem object in 2D space.
            display: the surface on which the GameItem object is drawn.
        """
        self._x = x
        self._y = y
        self._display = display

    @abstractmethod
    def update(self) -> None:
        """Updates the GameItem object."""
        pass

    @abstractmethod
    def draw(self) -> pygame.Rect:
        """Draws the GameItem object to the pygame surface.

        Returns:
            A pygame.Rect object representing the GameItem.
        """
        pass

    @abstractmethod
    def get_current_position(self) -> tuple[int, int]:
        """Returns the x-y coordinates of the GameItem object.

        Returns:
            The x-y coordinates of the GameItem object.
        """
        pass
