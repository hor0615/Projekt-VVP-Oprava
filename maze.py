import random
from collections import deque

import matplotlib.pyplot as plt
import numpy as np
from numpy import typing as npt


class MazeException(Exception):
    def __init__(self, value: str):
        self.value = value


TEMPLATE_EMPTY = 0
TEMPLATE_SLALOM = 1


class Maze:
    @staticmethod
    def load_from_file(filename: str) -> "Maze":
        """
        Load maze file from CSV file. Each value in the file must be either `1` (wall) or `0` (corridor).
        :param filename: Path to the CSV file.
        """

        raw = np.loadtxt(filename, delimiter=',', dtype=int)

        maze = Maze()
        # convert numbers to booleans
        maze.set_grid(raw.astype(bool))
        return maze

    @staticmethod
    def generate(width: int, height: int, filename: str | None = None, template: int = TEMPLATE_SLALOM) -> "Maze":
        maze = Maze()

        if template == TEMPLATE_EMPTY:
            maze.set_grid(np.zeros((height, width), dtype=bool))
        elif template == TEMPLATE_SLALOM:
            maze.set_grid(np.ones((height, width), dtype=bool))

            directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
            stack = deque([(0, 0)])
            maze.set_cell(0, 0, False)

            while stack:
                # peek top value
                x, y = stack[-1]
                neighbors = []

                for dx, dy in directions:
                    # neighbor's coords
                    nx, ny = x + dx, y + dy
                    if maze.is_in_bounds(nx, ny) and maze.get_cell(nx, ny):
                        neighbors.append((nx, ny, x + dx // 2, y + dy // 2))  # target + wall cell

                if neighbors:
                    nx, ny, wx, wy = random.choice(neighbors)
                    maze.set_cell(wx, wy, False)  # knock down wall
                    maze.set_cell(nx, ny, False)  # carve new cell
                    stack.append((nx, ny))
                else:
                    stack.pop()  # backtrack

            # ensure end cell is reachable
            cells_to_clear = [(-1, -1), (-2, -1), (-1, -2)]
            for cell in cells_to_clear:
                maze.set_cell(cell[0], cell[1], False)
        else:
            raise MazeException(f"Unknown template: {template}")

        if filename:
            maze.save_to_file(filename)

        return maze

    def __init__(self):
        self._grid: npt.NDArray[bool] | None = None
        """
        Represents the maze as a numpy boolean array. `True` represents a wall and `False` represents an empty space.
        Shouldn't be set directly. Use `Maze.set_grid`.
        """

        self.start_point = (0, 0)
        """Entry point of the maze (in the top left corner by default). Shouldn't be changed."""

        self.end_point = (0, 0)
        """
        Finish point of the maze (in the bottom right corner by default). Shouldn't be set directly. It's set
        automatically by `Maze.set_grid` -- that is, when the maze grid is initialized or changed.
        """

    def set_grid(self, grid: npt.NDArray[bool]) -> None:
        """
        Sets `self.grid` to the given two-dimensional bool NDArray and sets the
        `self.end_point` to its bottom right corner.
        """

        self._grid = grid
        self.end_point = (self.width() - 1, self.height() - 1)

    def save_to_file(self, filename: str) -> None:
        """
        Write maze to CSV file.
        :param filename: Path to the CSV file.
        """

        np.savetxt(filename, self._grid, delimiter=',', fmt='%d')

    def plot(self, path: list[tuple[int, int]] | None = None) -> None:
        """
        Plot the maze using `matplotlib`.
        :param path List of 2-tuples. Each tuple represents a point in the path.
        If `None`, the path is not plotted.
        """

        if self._grid is None:
            raise MazeException("Can't plot maze; grid is empty")

        fig, ax = plt.subplots()
        fig.patch.set_facecolor('#ddd')
        ax.imshow(self._grid, cmap="gray_r")

        plot_title: str
        if path:
            x_coords, y_coords = zip(*path)
            ax.plot(x_coords, y_coords, color="red", linewidth=2, marker='o')
            plot_title = "Maze (with path)"
        else:
            plot_title = "Maze (no path)"

        plt.title(plot_title)

        plt.axis("off")
        plt.show()

    def width(self) -> int:
        return self._grid.shape[1]

    def height(self) -> int:
        return self._grid.shape[0]

    def _get_indexes(self, x: int, y: int) -> tuple[int, int]:
        """
        Takes a standard (x, y) index and transforms it into a tuple that can be used to reference
        the cell at (x, y) such that:

        `grid[*self._get_indexes(x, y)] = grid[y][x]`

        If `x` or `y` are negative, the width/height of the grid is added to them so that they
        can be used to reference points at the right or bottom more easily. Therefore:

        `grid[*self._get_indexes(-1, -2)] = grid[grid.shape[1] - 2][grid.shape[0] - 1]`

        :param x: X index of the cell.
        :param y: Y index of the cell.
        :return: (y, x).
        """

        ax, ay = x, y
        if x < 0: ax = self.width() + x
        if y < 0: ay = self.height() + y
        return ay, ax

    def get_cell(self, x: int, y: int) -> bool:
        return self._grid[*self._get_indexes(x, y)]

    def set_cell(self, x: int, y: int, value: bool) -> None:
        self._grid[*self._get_indexes(x, y)] = value

    def is_in_bounds(self, x: int, y: int) -> bool:
        """
        Is the point (x, y) inside the maze?
        :param x: Point X coordinate.
        :param y: Point Y coordinate.
        :returns: `True` if the point is inside the maze, `False` otherwise.
        """
        return 0 <= x < self.width() and 0 <= y < self.height()

    def is_passable(self, x: int, y: int) -> bool:
        """
        Is the point (x, y) passable or is it a wall?
        :param x: Point X coordinate.
        :param y: Point Y coordinate.
        :returns: `True` if the point is passable (i.e. it's empty); `False` otherwise.
        """
        return not self.get_cell(x, y)
