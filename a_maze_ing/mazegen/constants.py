#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   constants.py                                         :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: horarivo <horarivo@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/05/26 18:38:40 by horarivo            #+#    #+#            #
#   Updated: 2026/05/26 18:40:08 by horarivo           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

"""Global constants: wall bitmasks, keycodes, palettes, 42 pattern."""

from typing import Final

# ── Wall bitmasks (bit0=N, bit1=E, bit2=S, bit3=W; 1=closed) ────────────
NORTH: Final[int] = 0b0001
EAST: Final[int] = 0b0010
SOUTH: Final[int] = 0b0100
WEST: Final[int] = 0b1000

OPPOSITE: Final[dict[int, int]] = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST,
}
DELTA: Final[dict[int, tuple[int, int]]] = {
    NORTH: (0, -1),
    SOUTH: (0, 1),
    EAST: (1, 0),
    WEST: (-1, 0),
}
DIR_NAME: Final[dict[int, str]] = {
    NORTH: "N",
    EAST: "E",
    SOUTH: "S",
    WEST: "W",
}

# ── X11 Keycodes ─────────────────────────────────────────────────────────
KEY_Q: Final[int] = 113
KEY_C: Final[int] = 99
KEY_P: Final[int] = 112
KEY_SPACE: Final[int] = 32
KEY_ESCAPE: Final[int] = 65307

# ── Pattern "42" (9 columns × 7 rows) ───────────────────────────────────
PAT_H: Final[int] = 7
PAT_W: Final[int] = 9  # 4 + 1 espace + 4

_D4: Final[list[list[int]]] = [
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [1, 1, 1, 1],
    [0, 0, 0, 1],
    [0, 0, 0, 1],
    [0, 0, 0, 1],
]
_D2: Final[list[list[int]]] = [
    [1, 1, 1, 1],
    [0, 0, 0, 1],
    [0, 0, 0, 1],
    [1, 1, 1, 1],
    [1, 0, 0, 0],
    [1, 0, 0, 0],
    [1, 1, 1, 1],
]


def _build_42() -> list[list[int]]:
    """Assemble the '42' bitmap (PAT_W × PAT_H).

    Returns:
        2D grid where 1 = fully walled cell.
    """
    pat: list[list[int]] = [[0] * PAT_W for _ in range(PAT_H)]
    for r in range(PAT_H):
        for c in range(4):
            pat[r][c] = _D4[r][c]
            pat[r][5 + c] = _D2[r][c]
    return pat


PATTERN_42: Final[list[list[int]]] = _build_42()

# ── Color palettes ──────────────────────────────────────────────────
_Palette = dict[str, tuple[int, int, int]]

PALETTES: Final[list[_Palette]] = [
    {   # Night
        "wall": (220, 220, 220),
        "bg": (20, 20, 35),
        "visited": (28, 28, 52),
        "current": (255, 220, 50),
        "path": (80, 200, 255),
        "entry": (80, 255, 120),
        "exit": (255, 80, 80),
        "pattern": (70, 90, 255),
        "info_bg": (8, 8, 18),
        "hint": (80, 80, 110),
    },
    {   # Forest
        "wall": (180, 140, 60),
        "bg": (15, 25, 15),
        "visited": (20, 40, 20),
        "current": (255, 200, 50),
        "path": (100, 255, 160),
        "entry": (80, 255, 120),
        "exit": (255, 80, 80),
        "pattern": (140, 220, 60),
        "info_bg": (5, 12, 5),
        "hint": (60, 90, 60),
    },
    {   # Neon
        "wall": (200, 80, 120),
        "bg": (10, 10, 20),
        "visited": (28, 18, 42),
        "current": (255, 255, 100),
        "path": (255, 200, 80),
        "entry": (80, 255, 120),
        "exit": (255, 80, 80),
        "pattern": (255, 100, 200),
        "info_bg": (5, 5, 12),
        "hint": (90, 60, 100),
    },
]
