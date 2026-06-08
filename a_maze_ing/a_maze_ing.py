#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   a_maze_ing.py                                        :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: horarivo <horarivo@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/05/26 18:15:10 by horarivo            #+#    #+#            #
#   Updated: 2026/05/26 18:59:07 by horarivo           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import sys

from mazegen.app import AppState
from mazegen.config import Config, die


def main() -> None:
    """Main program entry point"""
    if len(sys.argv) != 2:
        print(
            "Usage: python3 a_maze_ing.py config.txt",
            file=sys.stderr,
        )
        sys.exit(1)

    cfg = Config.from_file(sys.argv[1])

    try:
        from mlx import Mlx
        mlx = Mlx()
    except ImportError:
        die(
            "Module 'mlx' unknown."
            "Install it with : pip install <path>/mlx-*.whl"
        )
    except Exception as exc:
        die(f"Impossible to load the module MLX : {exc}")

    app = AppState(cfg, mlx)
    app.run()


if __name__ == "__main__":
    main()
