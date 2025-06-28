from labyrinth.maze import Maze
from labyrinth.pathfinder import find_path

maze = Maze.generate(11, 11, filename="examples/generated_maze.csv")
path = find_path(maze)
maze.plot(path)
