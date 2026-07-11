#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   generator.py                                         :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: horarivo <horarivo@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/05/26 18:42:42 by horarivo            #+#    #+#            #
#   Updated: 2026/06/12 11:56:19 by horarivo           ###   ########.fr      #
#                                                                             #
# ########################################################################### #


import random
import sys
from typing import Optional

from .constants import (
    DELTA,
    OPPOSITE,
    PAT_H,
    PAT_W,
    PATTERN_42,
)


class MazeGenerator:
    """Iterative recursive backtracker maze generator.

    ``grid[y][x]`` = 4-bit mask NESW (1 = wall closed, 0 = open).
    All cells start fully walled (0xF). The backtracker carves passages
    by clearing wall bits on both sides simultaneously, guaranteeing
    coherent wall data across neighbours.
    Pattern '42' cells are pre-marked as visited so they stay fully walled.
    """

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit_: tuple[int, int],
        seed: Optional[int] = None,
        perfect: bool = True,
    ) -> None:
        """Initialize and prepare generation.

        Args:
            width:   Width in cells.
            height:  Height in cells.
            entry:   Coordinates (x, y) of the entrance.
            exit_:   Coordinates (x, y) of the exit.
            seed:    Random seed (None = random).
            perfect: If True, generates a perfect maze.
        """
        self.width = width
        self.height = height
        self.entry = entry
        self.exit_ = exit_
        self.perfect = perfect
        self.seed: int = (
            seed if seed is not None
            else random.randint(0, 999_999)
        )
        random.seed(self.seed)

        # All cells start with every wall closed (0xF = 0b1111)
        self.grid: list[list[int]] = [
            [0xF] * width for _ in range(height)
        ]
        # Tracks which cells have been visited by the backtracker
        self.visited: list[list[bool]] = [
            [False] * width for _ in range(height)
        ]
        # Marks cells belonging to the '42' pattern (never carved)
        self.is_42: list[list[bool]] = [
            [False] * width for _ in range(height)
        ]

        self.current: Optional[tuple[int, int]] = None
        self.done: bool = False
        self.pattern_skipped: bool = False
        self._stack: list[tuple[int, int]] = []

        self._stamp_42()
        self._start_walk()

    # ## '42' pattern

    def _stamp_42(self) -> None:
        """Centre the '42' pattern and mark its cells as pre-visited.

        Pre-visited cells are skipped by the backtracker, so they remain
        fully walled. If the maze is too small, a warning is printed and
        the pattern is skipped.
        """
        if self.width < PAT_W + 4 or self.height < PAT_H + 4:
            print(
                f"[Info] Maze too small for pattern '42' "
                f"(minimum {PAT_W + 4}x{PAT_H + 4}, "
                f"current {self.width}x{self.height}).",
                file=sys.stderr,
            )
            self.pattern_skipped = True
            return

        ox = (self.width - PAT_W) // 2
        oy = (self.height - PAT_H) // 2

        for r in range(PAT_H):
            for c in range(PAT_W):
                if PATTERN_42[r][c] == 1:
                    gx, gy = ox + c, oy + r
                    self.visited[gy][gx] = True
                    self.is_42[gy][gx] = True

    # ## Backtracker

    def _start_walk(self) -> None:
        """Start the depth-first walk from the entry cell."""
        sx, sy = self.entry
        self.visited[sy][sx] = True
        self._stack = [(sx, sy)]
        self.current = (sx, sy)

    def step(self, n: int = 1) -> None:
        """Advance n steps in the animated generation.

        Each step tries to carve a passage to a random unvisited neighbour.
        If none is available, the algorithm backtracks by popping the stack.

        Args:
            n: Number of steps to perform.
        """
        for _ in range(n):
            if not self._stack:
                self._finish()
                return

            x, y = self._stack[-1]
            self.current = (x, y)

            dirs = list(DELTA.keys())
            random.shuffle(dirs)
            moved = False

            for direction in dirs:
                dx, dy = DELTA[direction]
                nx, ny = x + dx, y + dy
                in_bounds = (
                    0 <= nx < self.width
                    and 0 <= ny < self.height
                )
                if in_bounds and not self.visited[ny][nx]:
                    # Carve passage: clear the wall on both sides
                    self.grid[y][x] &= ~direction
                    self.grid[ny][nx] &= ~OPPOSITE[direction]
                    self.visited[ny][nx] = True
                    self._stack.append((nx, ny))
                    moved = True
                    break

            if not moved:
                self._stack.pop()

        if not self._stack:
            self._finish()

    def generate_all(self) -> None:
        """Generate the complete maze in one go (non-animated)."""
        while not self.done:
            self.step(256)

    def _finish(self) -> None:
        """Finalise generation and optionally punch extra passages."""
        self.done = True
        self.current = None
        if not self.perfect:
            self._add_loops()

    def _add_loops(self) -> None:
        """Punch extra east-facing passages to create an imperfect maze.

        Roughly 10% of the total cell count are opened. Cells belonging
        to the '42' pattern are never touched.
        """
        from .constants import EAST, WEST
        extra = max(1, (self.width * self.height) // 10)
        for _ in range(extra):
            x = random.randint(0, self.width - 2)
            y = random.randint(0, self.height - 2)
            if self.is_42[y][x] or self.is_42[y][x + 1]:
                continue
            if self.grid[y][x] & EAST:
                self.grid[y][x] &= ~EAST
                self.grid[y][x + 1] &= ~WEST
