*This project has been created as part of the 42 curriculum by horarivo.*

# A-Maze-ing

## Description

A-Maze-ing is an interactive maze generator written in Python. The project aims to produce visual and playable mazes from a configuration file while providing an animated generation process, shortest path solving, and a text export of the result.

The maze is rendered in an MLX window, and the application highlights a central "42" pattern to reinforce the visual identity of the project.

## Instructions

### Requirements

- Python 3.10 or higher
- `mlx` module compatible with Python 3 (provided as `mlx-2.2-py3-none-any.whl`)

### Installation

1. Install Python 3.10+.
2. Install development dependencies if needed:

```bash
python3 -m pip install -r requirements.txt
```

3. Install the MLX module from the provided wheel:

```bash
python3 -m pip install mlx-2.2-py3-none-any.whl
```

### Execution

1. Edit `config.txt` or create a custom configuration file.
2. Run the application:

```bash
python3 a_maze_ing.py config.txt
```

### Keyboard controls

- `SPACE`: regenerate a new maze
- `P`: show/hide the shortest path
- `C`: cycle through color palettes
- `Q` or `ESC`: quit the application

## Resources

- Maze generation algorithm: depth-first search / recursive backtracker
- Breadth-first search (BFS) for shortest path solving
- MLX / MiniLibX documentation for graphical output
- Classic maze-related articles: "Maze generation algorithm" and "Depth-first search maze"

### AI usage

No artificial intelligence was used to write the project code. This README has been written manually to document the solution.

## Config file

The configuration file must contain one value per line in `KEY=VALUE` format. Lines starting with `#` are comments and ignored.

Expected keys:

- `WIDTH`: maze width in cells (integer >= 5)
- `HEIGHT`: maze height in cells (integer >= 5)
- `ENTRY`: entry coordinates in `x,y` format
- `EXIT`: exit coordinates in `x,y` format
- `OUTPUT_FILE`: output file path
- `PERFECT`: `True` or `False` to enable or disable loops
- `SEED`: optional integer to seed random generation

### Example configuration

```text
WIDTH=13
HEIGHT=11
ENTRY=0,0
EXIT=1,1
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

## Generation algorithm

The project uses the "Recursive Backtracker" algorithm to generate the maze. This algorithm walks the maze cells, opens passages to unvisited neighbors, and backtracks when no valid neighbor remains.

### Why this algorithm?

- It is simple to implement and easy to visualize.
- It produces perfect mazes with a single path between cells.
- It fits naturally with step-by-step animated generation.
- It is suitable for adding visual features such as the "42" pattern and path solving.

## Reusable parts

Reusable parts of the project include:

- `mazegen/config.py`: configuration file parser that can be reused by other applications.
- `mazegen/generator.py`: independent maze generator that produces a grid of walls and passages.
- `mazegen/solver.py`: BFS solver for the shortest path in a maze grid.
- `mazegen/renderer.py`: rendering and file writing helpers.

These components can be reused in other maze, game, or graphical application projects.

## Advanced features

- Central "42" pattern: some cells remain fully walled to draw the pattern.
- Interactive shortest path display.
- Three different color palettes.
- `PERFECT=False` option to generate imperfect mazes with loops.
- Export of the result as a text file in the expected format.

## Project structure

- `a_maze_ing.py`: main executable
- `mazegen/app.py`: MLX interface, rendering, and event handling
- `mazegen/config.py`: configuration parsing and validation
- `mazegen/constants.py`: constants and color palettes
- `mazegen/generator.py`: maze generation
- `mazegen/renderer.py`: rendering and output writing
- `mazegen/solver.py`: maze solving
- `config.txt`: example configuration
- `maze.txt`: generated output file
- `pyproject.toml`: package configuration
- `requirements.txt`: development dependencies

## Project management

### Team

- `horarivo`: full development, design, testing, and documentation.

### Planning

1. Analyze the project requirements and define features.
2. Implement the configuration parser.
3. Develop the maze generator.
4. Add MLX rendering and the BFS solver.
5. Integrate the "42" pattern, palettes, and keyboard controls.
6. Test and export the output file.

### What worked well

- The modular project structure simplified implementation.
- Separating configuration, generation, rendering, and solving made the code easier to read.
- The "42" pattern adds a notable visual touch.

### Improvements possible

- Add multiple generation algorithms (Prim, Kruskal, Aldous-Broder).
- Allow dynamic loading of multiple configurations.
- Add more advanced rendering options (zoom, grid overlay, solver animation).

### Tools used

- Python 3.10+
- `pip` for dependency management
- `mlx` / MiniLibX for graphical output
- VS Code for development
- Git for version control
