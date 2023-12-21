import pygame
from game_item import GameItem
from direction import Direction
from constants import SNAKE_COLOR, SNAKE_SIZE_X_Y, DISPLAY_WIDTH, DISPLAY_HEIGHT


class Snake(GameItem):
    """Represents a Snake object."""

    def __init__(self, x: int, y: int, display: pygame.Surface) -> None:
        """Create an object of type Snake."""

        super().__init__(x, y, display)
        self._segment_size = SNAKE_SIZE_X_Y

        # Snake moves right to begin game
        self._direction = Direction.RIGHT

        # Snake body
        self._snake_body = [
            (x, y),  # Tail of snake
            (x + self._segment_size, y),
            (x + self._segment_size * 2, y),
            (x + self._segment_size * 3, y),  # Head of snake
        ]

        self._autopilot = False

    def update(self, game_item: GameItem) -> None:
        """Update the Snake object.

        Args:
            food (Food): object of type Food.
        """
        if self._autopilot:
            self.toggle_autopilot(game_item)

        # Record current Snake head position; this will be
        # updated based on new direction.
        current_snake_head_position = self._snake_body[-1]

        # Extract values from new direction; these will be
        # used to update the Snake head position.
        x_direction, y_direction = self._direction.value

        # Check if moving Snake to new position will result in a collision
        if not self.has_collided_with_wall() and not self.has_collided_with_self():
            new_snake_head_position = (
                current_snake_head_position[0] + self._segment_size * x_direction,
                current_snake_head_position[1] + self._segment_size * y_direction,
            )
            self._snake_body.append(new_snake_head_position)

            # Check if snake has collided with food; if not, pop last
            # tuple, meaning the Snake is moving. If it collides with
            # food, don't pop tail; it has thus "grown" by one segment.
            if not self.has_collided_with_food(game_item):
                self._snake_body.pop(0)

    def toggle_autopilot(self, game_item: GameItem) -> None:
        """Toggle autopilot mode on/off.

        Args:
            food: object of type Food.
        """
        path = self.bfs(game_item)
        if path:
            next_position = path[0]
            current_position = self.get_current_position()
            snake_head_x = next_position[0] - current_position[0]
            snake_head_y = next_position[1] - current_position[1]

            # Convert dx, dy into a direction
            if snake_head_x > 0:
                self.set_direction(Direction.RIGHT)
            elif snake_head_x < 0:
                self.set_direction(Direction.LEFT)
            elif snake_head_y > 0:
                self.set_direction(Direction.DOWN)
            elif snake_head_y < 0:
                self.set_direction(Direction.UP)

    def bfs(self, game_item: GameItem) -> list[tuple[int, int]]:
        """
        Breadth-first search algorithm to find the shortest path
        from Snake head to Food.

        Args:
            food: object of type Food.

        Returns:
            A list of tuples, each containing the x-y coordinates
            of the path from Snake head to Food.
        """
        snake_head_xy = self.get_current_position()
        path_to_food = []

        segments_visited = []
        segment_queue = [(snake_head_xy, path_to_food)]

        # While segment_queue is not empty...
        while segment_queue:
            (snake_head_x, snake_head_y), path_to_food = segment_queue.pop(0)

            # If Snake head intersect with Food, return path to food.
            if (snake_head_x, snake_head_y) == game_item.get_current_position():
                return path_to_food

            # Otherwise, visit all Snake head's immediate neighbors
            for direction in Direction:
                dx, dy = direction.value
                next_head_x, next_head_y = (
                    snake_head_x + dx * self._segment_size,
                    snake_head_y + dy * self._segment_size,
                )

                # Check if move is valid
                if self._valid_neighbors((next_head_x, next_head_y), segments_visited):
                    # Add current segment to list of visited segments.
                    segments_visited.append((next_head_x, next_head_y))

                    # Add current segment to path leading from Snake head to Food
                    new_path_to_food = path_to_food + [(next_head_x, next_head_y)]

                    # Add new head position, path to food to segment queue
                    segment_queue.append(((next_head_x, next_head_y), new_path_to_food))

        return []  # Return an empty list if no path found

    def _valid_neighbors(
        self, snake_head: tuple[int, int], visited_segments: list[tuple[int, int]]
    ) -> bool:
        """
        Check if Snake head is within display bounds, has not already
        been visited, and is not part of the Snake body.

        Args:
            snake_head: a tuple containing the x-y coordinates of the Snake head.
            visited_segments: a list of tuples, each containing the x-y coordinates
                                of a Snake segment.

        Returns:
            True if Snake head is within display bounds, has not already
            been visited, and is not part of the Snake body, else False.
        """
        return (
            0 <= snake_head[0] < DISPLAY_WIDTH
            and 0 <= snake_head[1] < DISPLAY_HEIGHT
            and snake_head not in self.get_snake_body()[:-1]
            and snake_head not in visited_segments
        )

    def draw(self) -> list[pygame.Rect]:
        """
        Create a list of pygame.Rect objects, each one representing
        a segment of the Snake's body.

        Returns:
            A list of pygame.Rect objects, which can be drawn to
            the pygame surface,
        """
        snake_body = []

        for segment_position in self._snake_body:
            segment = pygame.draw.rect(
                surface=self._display,
                color=SNAKE_COLOR,
                rect=[
                    segment_position[0],
                    segment_position[1],
                    self._segment_size,
                    self._segment_size,
                ],
            )
            snake_body.append(segment)

        return snake_body

    def get_current_position(self) -> tuple[int, int]:
        """Return the x-y coordinates of the Snake head.

        Returns:
            A tuple containing the x-y coordinates of the Snake head.
        """
        return self._snake_body[-1]

    def has_collided_with_wall(self) -> bool:
        """Check if the Snake head exceeds display bounds.

        Returns:
            True if Snake head collides with wall, else False.
        """
        snake_head_x, snake_head_y = self._snake_body[-1]

        return (
            snake_head_x < 0
            or snake_head_x > DISPLAY_WIDTH - SNAKE_SIZE_X_Y
            or snake_head_y < 0
            or snake_head_y > DISPLAY_HEIGHT - SNAKE_SIZE_X_Y
        )

    def has_collided_with_self(self) -> bool:
        """Check if Snake head collides with its own body.

        Returns:
            True if Snake head collides with its body, else False.
        """
        return self._snake_body[-1] in self._snake_body[:-1]

    def has_collided_with_food(self, game_item: GameItem) -> bool:
        """Check if Snake collides with object of type Food.

        Args:
            food (Food): object of type Food.

        Returns:
            True if Snake collides with food, else False.
        """
        return self.get_current_position() == game_item.get_current_position()

    def get_snake_body(self) -> list[tuple[int, int]]:
        """
        Return a list of tuples, each consisting of integers that
        represent the x-y coordinates of all the Snake's body segments.

        Returns:
            A list of tuples, each containing two integers representing
            x-y coordinates.
        """
        return self._snake_body

    def get_direction(self) -> Direction:
        """Return the current direction of the Snake.

        Returns:
            The current direction of the Snake.
        """
        return self._direction

    def set_direction(self, new_direction: Direction) -> None:
        """
        Set the direction of Snake. Snake cannot change direction 180 degrees.
        For example if Snake is moving right, Snake's next move cannot be left;
        if it's moving up, it cannot move down, and vice-versa.

        Args:
            The new direction of the Snake.
        """
        opposite_directions = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }

        if new_direction != opposite_directions[self._direction]:
            self._direction = new_direction
