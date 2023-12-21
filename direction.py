from enum import Enum


class Direction(Enum):
    """
    Represent keyboard directions to move Snake. Tuples represent
    the change in x-y coordinates when moving in a direction.
    """

    UP = (0, -1)  # Move upwards; no change in x, decrease y by 1
    DOWN = (0, 1)  # Move downwards; no change in x, increase y by 1
    LEFT = (-1, 0)  # Move left; decrease x by 1, no change in y
    RIGHT = (1, 0)  # Move right; increase x by 1, no change in y
