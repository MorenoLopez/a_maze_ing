#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   __init__.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: horarivo <horarivo@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/05/28 00:00:00 by horarivo            #+#    #+#            #
#   Updated: 2026/06/01 20:20:09 by horarivo           ###   ########.fr      #
#                                                                             #
# ########################################################################### #


"""maze - public API of the maze generation package.

This file marks the ``maze/`` directory as a Python package and defines
the public API: the names listed in ``__all__`` are the only ones that
outside code should import. Internal modules (renderer, app, constants)
are implementation details and are not re-exported here.

Typical usage::

    from maze import MazeGenerator, MazeSolver

    gen = MazeGenerator(width=20, height=15, entry=(0, 0), exit_=(19, 14))
    gen.generate_all()

    solver = MazeSolver(gen)
    print(solver.solve())        # ['E', 'S', 'E', ...]
    print(solver.path_cells())   # {(0, 0), (1, 0), ...}
"""

from .config import Config, die
from .generator import MazeGenerator
from .solver import MazeSolver

__all__ = [
    "Config",
    "die",
    "MazeGenerator",
    "MazeSolver",
]
