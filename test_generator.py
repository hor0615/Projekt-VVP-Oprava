from labyrinth.maze import Maze

maze = Maze.generate(11, 11, filename="examples/generated_maze.csv")
maze.plot()
