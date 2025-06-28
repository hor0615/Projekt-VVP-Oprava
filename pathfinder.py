from collections import deque

from labyrinth.maze import Maze

neighbor_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def find_path(maze: Maze) -> list[tuple[int, int]] | None:
    """
    Uses Dijkstra's (?) algorithm to find the shortest path through the maze.
    :param maze: The maze to look through.
    :return: A list of 2-tuples, each of which represents a point on the path.
    """

    queue = deque()
    queue.append((maze.start_point, [maze.start_point]))

    # set of all visited points
    visited = set()
    visited.add(maze.start_point)

    while queue:
        (x, y), path = queue.popleft()

        if (x, y) == maze.end_point:
            return path

        # loop through neighbors
        for dx, dy in neighbor_offsets:
            # coords of the neighbor
            nx, ny = x + dx, y + dy

            # seeing if the neighbor at (nx, ny):
            # 1. is in bounds
            # 2. is passable (i.e. isn't a wall)
            # 3. hasn't already been visited
            if maze.is_in_bounds(nx, ny) and maze.is_passable(nx, ny) and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), path + [(nx, ny)]))

    return None
