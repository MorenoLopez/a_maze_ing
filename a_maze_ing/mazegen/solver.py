#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   solver.py                                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: horarivo <horarivo@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/05/2 18:47:42 by horarivo            #+#    #+#            #
#   Updated: 2026/05/28 10:43:22 by horarivo           ###   ########.fr      #
#                                                                             #
# ########################################################################### #


from collections import deque
from typing import Optional

from .constants import DELTA, DIR_NAME
from .generator import MazeGenerator


class MazeSolver:
    """Breadth-first search solver for a MazeGenerator grid.

    BFS guarantees the shortest path in an unweighted graph, which is
    exactly what a maze is: each passage between two cells costs 1 step.

    The result is computed lazily on the first call to solve() and
    cached so that repeated calls are free.

    Example usage::

        gen = MazeGenerator(20, 15, (0, 0), (19, 14), seed=42)
        gen.generate_all()

        solver = MazeSolver(gen)
        path  = solver.solve()        # ['E', 'E', 'S', ...]
        cells = solver.path_cells()   # {(0, 0), (1, 0), ...}
    """

    def __init__(self, gen: MazeGenerator) -> None:
        """Attach the solver to a MazeGenerator.

        Args:
            gen: A MazeGenerator instance (ideally with done=True).
        """
        self._gen = gen
        # None means solve() has not been called yet (lazy cache)
        self._path: Optional[list[str]] = None

    def solve(self) -> list[str]:
        """Find the shortest path from entry to exit using BFS.

        The result is cached: calling solve() a second time returns the
        same list without rerunning BFS.

        Returns:
            Ordered list of direction letters ('N', 'E', 'S', 'W').
            Returns an empty list if no path exists (should not happen
            in a correctly generated perfect maze).
        """
        if self._path is not None:
            return self._path

        gen = self._gen
        ex, ey = gen.exit_

        # Each queue entry: (current_cell, path_taken_so_far)
        queue: deque[tuple[tuple[int, int], list[str]]] = deque(
            [(gen.entry, [])]
        )
        seen: set[tuple[int, int]] = {gen.entry}

        while queue:
            (cx, cy), path = queue.popleft()
            if (cx, cy) == (ex, ey):
                self._path = path
                return path

            for direction, (dx, dy) in DELTA.items():
                nx, ny = cx + dx, cy + dy
                in_bounds = (
                    0 <= nx < gen.width
                    and 0 <= ny < gen.height
                )
                wall_open = not (gen.grid[cy][cx] & direction)
                if in_bounds and (nx, ny) not in seen and wall_open:
                    seen.add((nx, ny))
                    queue.append(
                        ((nx, ny), path + [DIR_NAME[direction]])
                    )

        # No path found (only possible if the maze is disconnected)
        self._path = []
        return self._path

    def path_cells(self) -> set[tuple[int, int]]:
        """Return every (x, y) cell that lies on the solution path.

        Calls solve() internally if not already called.

        Returns:
            Set of coordinate tuples from entry to exit (inclusive).
        """
        delta_map: dict[str, tuple[int, int]] = {
            "N": (0, -1),
            "E": (1, 0),
            "S": (0, 1),
            "W": (-1, 0),
        }
        cells: set[tuple[int, int]] = {self._gen.entry}
        x, y = self._gen.entry
        for d in self.solve():
            dx, dy = delta_map[d]
            x, y = x + dx, y + dy
            cells.add((x, y))
        return cells
