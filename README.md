# Maze Solver & Generator

Tento projekt se zabývá načítáním, řešením a generováním bludišť. Podporuje práci s bludišti reprezentovanými jako matice `n × n`, kde levý horní roh je vstup a pravý dolní roh je výstup. Projekt používá knihovnu NumPy pro práci s daty a generuje výstupní obrázky, které znázorňují řešení.

## Funkcionality

- Načtení bludiště z CSV souboru 
- Reprezentace bludiště pomocí NumPy matice (`True` = zeď, `False` = průchod)
- Sestavení incidenční matice pro grafové reprezentace bludiště
- Hledání nejkratší cesty pomocí Dijkstrova algoritmu
- Vykreslení výsledku jako obrázku (černá = zeď, bílá = průchozí, červená = nejkratší cesta)
- Generování bludiště s garantovanou průchodností
- více šablon (např. `empty`, `slalom`, ...)

## Načtení bludiště z CSV souboru 
``` 
maze = Maze.load_from_file("examples/example_maze.csv") 
```
## Generování bludiště
```
maze2 = Maze.generate(9, 9, filename="examples/generated_maze.csv")
```
## Hledání nejkratší cesty
```
path = find_path(maze)
if path is None:
    print("No path found")
```
## Ukázky
Vygenerované bludiště

![Vygenerované bludiště](Maze.generated.png)

Vyřešené bludiště

![Vyřešené bludiště](Maze.solved.png)

## Struktura celého projektu

Project_VVP_labyrinth/

- labyrinth
    - maze.py         
    - pathfinder.py      
    - __init__.py        

- examples
    - example_maze.csv  
    - example_maze_2.csv 
    - example_maze_3.csv
    - generated_maze.csv
    - generated_maze_2.csv

- tests
    - test_generator.py
    - test_maze.py
    - test_pathfinder.py

- Jupyter_maze.ipynb

- README.md            

