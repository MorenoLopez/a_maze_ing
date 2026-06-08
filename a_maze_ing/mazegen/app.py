#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   app.py                                               :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: horarivo <horarivo@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/05/25 18:52:47 by horarivo            #+#    #+#            #
#   Updated: 2026/05/28 10:45:02 by horarivo           ###   ########.fr      #
#                                                                             #
# ########################################################################### #


from typing import Any, Optional

from .config import Config, die
from .constants import (
    EAST,
    KEY_C,
    KEY_ESCAPE,
    KEY_P,
    KEY_Q,
    KEY_SPACE,
    NORTH,
    PALETTES,
    SOUTH,
    WEST,
)
from .generator import MazeGenerator
from .renderer import (
    draw_hline,
    draw_vline,
    fill_rect,
    to_bytes,
    to_int,
    write_output,
)
from .solver import MazeSolver


class AppState:
    """Manages the MLX window, pixel rendering and keyboard events.

    Rendering strategy:
        1. The entire scene is drawn into an MLX image buffer.
        2. ``mlx_put_image_to_window`` displays the buffer in one operation.
        3. ``mlx_string_put`` draws text on top (info bar).

    Keyboard controls:
        - SPACE   : regenerate a new maze
        - P       : toggle shortest-path display
        - C       : cycle through colour palettes
        - Q / ESC : quit
    """

    INFO_H: int = 80    # info bar height in pixels
    MAX_CELL: int = 36  # maximum cell size in pixels
    MIN_CELL: int = 6   # minimum cell size in pixels

    def __init__(self, cfg: Config, mlx: Any) -> None:
        """Initialize MLX, create window and image buffer.

        Args:
            cfg: Validated maze configuration.
            mlx: Instance of the Mlx class.
        """
        self.cfg = cfg
        self.mlx: Any = mlx

        self.mlx_ptr: Any = mlx.mlx_init()
        if not self.mlx_ptr:
            die("Failed to initialize MLX.")

        # ── Compute pixel dimensions ──────────────────────────────────
        _, screen_w, screen_h = mlx.mlx_get_screen_size(self.mlx_ptr)

        self.cs: int = max(
            self.MIN_CELL,
            min(
                int(screen_w * 0.9) // cfg.width,
                (int(screen_h * 0.9) - self.INFO_H) // cfg.height,
            ),
        )
        self.maze_px_w: int = cfg.width * self.cs
        self.maze_px_h: int = cfg.height * self.cs
        self.win_w: int = self.maze_px_w
        self.win_h: int = self.maze_px_h + self.INFO_H
        self.wall_w: int = max(1, self.cs // 9)

        # ── Create window ─────────────────────────────────────────────
        self.win_ptr: Any = mlx.mlx_new_window(
            self.mlx_ptr, self.win_w, self.win_h, "A-Maze-ing"
        )
        if not self.win_ptr:
            die("Unable to create MLX window.")

        # ── Create full-window image buffer ───────────────────────────
        self.img_ptr: Any = mlx.mlx_new_image(
            self.mlx_ptr, self.win_w, self.win_h
        )
        if not self.img_ptr:
            die("Unable to create MLX image.")
        self.data: Any
        self.sl: int
        self.data, _bpp, self.sl, _fmt = mlx.mlx_get_data_addr(
            self.img_ptr
        )

        # ── Application state ─────────────────────────────────────────
        self.pal_idx: int = 0
        self.show_path: bool = False
        # MazeSolver is created once generation is complete, then cached
        self.solver: Optional[MazeSolver] = None
        self.needs_redraw: bool = True

        self.gen: MazeGenerator = self._make_gen(cfg.seed)
        # Steps per loop-hook call, scaled to maze size
        self.spf: int = max(4, (cfg.width * cfg.height) // 80)

    # ── Generator management ──────────────────────────────────────────────

    def _make_gen(
        self, seed: Optional[int] = None
    ) -> MazeGenerator:
        """Create a new generator and reset all render state.

        Args:
            seed: Seed to use (None = pick randomly).

        Returns:
            A freshly initialised MazeGenerator.
        """
        self.show_path = False
        self.solver = None       # discard old solver with old maze
        self.needs_redraw = True
        return MazeGenerator(
            self.cfg.width,
            self.cfg.height,
            self.cfg.entry,
            self.cfg.exit_,
            seed=seed,
            perfect=self.cfg.perfect,
        )

    def _get_solver(self) -> MazeSolver:
        """Return the cached MazeSolver, creating it if necessary.

        Returns:
            A MazeSolver attached to the current generator.
        """
        if self.solver is None:
            self.solver = MazeSolver(self.gen)
        return self.solver

    # ── Rendering ─────────────────────────────────────────────────────────

    def _redraw(self) -> None:
        """Draw the entire scene into the buffer, then call put_image."""
        pal = PALETTES[self.pal_idx]
        gen = self.gen
        cs = self.cs
        ww = self.wall_w
        sl = self.sl
        data = self.data

        cb_bg = to_bytes(*pal["bg"])
        cb_wall = to_bytes(*pal["wall"])
        cb_visited = to_bytes(*pal["visited"])
        cb_current = to_bytes(*pal["current"])
        cb_path = to_bytes(*pal["path"])
        cb_entry = to_bytes(*pal["entry"])
        cb_exit = to_bytes(*pal["exit"])
        cb_pattern = to_bytes(*pal["pattern"])
        cb_info_bg = to_bytes(*pal["info_bg"])

        fill_rect(data, sl, 0, 0, self.win_w, self.win_h, cb_bg)
        fill_rect(
            data, sl, 0, self.maze_px_h, self.win_w,
            self.INFO_H, cb_info_bg,
        )
        draw_hline(
            data, sl, 0, self.maze_px_h, self.win_w, 1, cb_wall
        )

        # Resolve path cells once per frame (empty when path is hidden)
        path_set: set[tuple[int, int]] = (
            self._get_solver().path_cells()
            if self.show_path else set()
        )

        for row in range(gen.height):
            for col in range(gen.width):
                px = col * cs
                py = row * cs
                pos = (col, row)

                if gen.is_42[row][col]:
                    cb_fill = cb_pattern
                elif gen.current == pos:
                    cb_fill = cb_current
                elif self.show_path and pos in path_set:
                    cb_fill = cb_path
                elif pos == gen.entry:
                    cb_fill = cb_entry
                elif pos == gen.exit_:
                    cb_fill = cb_exit
                elif gen.visited[row][col]:
                    cb_fill = cb_visited
                else:
                    cb_fill = cb_bg

                fill_rect(data, sl, px, py, cs, cs, cb_fill)

                walls = gen.grid[row][col]
                if walls & NORTH:
                    draw_hline(data, sl, px, py, cs, ww, cb_wall)
                if walls & EAST:
                    draw_vline(
                        data, sl, px + cs - ww, py, cs, ww, cb_wall
                    )
                if walls & SOUTH:
                    draw_hline(
                        data, sl, px, py + cs - ww, cs, ww, cb_wall
                    )
                if walls & WEST:
                    draw_vline(data, sl, px, py, cs, ww, cb_wall)

        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr, self.win_ptr, self.img_ptr, 0, 0
        )

        wc = to_int(*pal["wall"])
        hc = to_int(*pal["hint"])
        ty = self.maze_px_h + 10

        if gen.done:
            path_len = len(self._get_solver().solve())
            status = (
                f"Finished  seed={gen.seed}       "
                f"path={path_len} steps"
            )
        else:
            done_cells = sum(
                gen.visited[r][c]
                for r in range(gen.height)
                for c in range(gen.width)
            )
            pct = done_cells * 100 // (gen.width * gen.height)
            status = f"Generating {pct}%     seed={gen.seed}"

        self.mlx.mlx_string_put(
            self.mlx_ptr, self.win_ptr, 8, ty, wc, status
        )
        self.mlx.mlx_string_put(
            self.mlx_ptr,
            self.win_ptr,
            8,
            ty + 22,
            hc,
            "SPACE=regen      P=path      C=color      Q=quit",
        )

    # ── MLX Callbacks ─────────────────────────────────────────────────────

    def on_key(self, keycode: int, _param: object) -> None:
        """Keyboard event handler.

        Args:
            keycode: X11 code of the pressed key.
            _param:  Parameter passed to the hook (ignored).
        """
        if keycode in (KEY_Q, KEY_ESCAPE):
            self.mlx.mlx_loop_exit(self.mlx_ptr)

        elif keycode == KEY_SPACE:
            self.gen = self._make_gen()

        elif keycode == KEY_P:
            if self.gen.done:
                self.show_path = not self.show_path
                self.needs_redraw = True

        elif keycode == KEY_C:
            self.pal_idx = (self.pal_idx + 1) % len(PALETTES)
            self.needs_redraw = True

    def on_loop(self, _param: object) -> None:
        """Called on every MLX loop iteration.

        Advances generation by self.spf steps when not finished,
        then redraws the scene if anything changed.

        Args:
            _param: Parameter passed to the hook (ignored).
        """
        if not self.gen.done:
            self.gen.step(self.spf)
            self.needs_redraw = True
            if self.gen.done:
                # Generation just finished: solve and write output file
                solver = self._get_solver()
                write_output(
                    self.gen,
                    solver.solve(),
                    self.cfg.output_file,
                )

        if self.needs_redraw:
            self._redraw()
            self.needs_redraw = False

    def on_expose(self, _param: object) -> None:
        """Redraw when the window is re-exposed (uncovered).

        Args:
            _param: Parameter passed to the hook (ignored).
        """
        self.needs_redraw = True

    def on_close(self, _param: object) -> None:
        """Handle the window close button (WM_DELETE_WINDOW).

        Args:
            _param: Parameter passed to the hook (ignored).
        """
        self.mlx.mlx_loop_exit(self.mlx_ptr)

    # ── Main loop ─────────────────────────────────────────────────────────

    def run(self) -> None:
        """Register MLX hooks and enter the main event loop."""
        self.mlx.mlx_key_hook(self.win_ptr, self.on_key, None)
        self.mlx.mlx_loop_hook(self.mlx_ptr, self.on_loop, None)
        self.mlx.mlx_expose_hook(self.win_ptr, self.on_expose, None)
        # X11 event 33 = WM_DELETE_WINDOW (window close button)
        self.mlx.mlx_hook(self.win_ptr, 33, 0, self.on_close, None)

        self.mlx.mlx_loop(self.mlx_ptr)

        # Clean up MLX resources on exit
        self.mlx.mlx_destroy_image(self.mlx_ptr, self.img_ptr)
        self.mlx.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
        self.mlx.mlx_release(self.mlx_ptr)
