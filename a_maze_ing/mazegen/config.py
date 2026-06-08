#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   config.py                                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: horarivo <horarivo@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/05/26 18:33:06 by horarivo            #+#    #+#            #
#   Updated: 2026/05/28 10:42:43 by horarivo           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

"""Read and validate KEY=VALUE configuration file."""

import sys
from typing import ClassVar, NoReturn, Optional


def die(msg: str) -> NoReturn:
    """Display an error on stderr and exit with code 1.

    Args:
        msg: Error message to display.
    """
    print(f"[Error] {msg}", file=sys.stderr)
    sys.exit(1)


def _parse_coord(
    raw: dict[str, str],
    key: str,
) -> tuple[int, int]:
    """Parse 'x,y' from raw[key] and return an integer tuple.

    Args:
        raw: Dictionary of KEY=VALUE pairs from config file.
        key: Key to read ('ENTRY' or 'EXIT').

    Returns:
        Tuple (x, y).
    """
    try:
        a, b = raw[key].split(",")
        return (int(a.strip()), int(b.strip()))
    except ValueError:
        die(f"{key} must be in x,y format (e.g., 0,0).")


class Config:
    """Read and validate KEY=VALUE configuration file."""

    REQUIRED: ClassVar[set[str]] = {
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
    }

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit_: tuple[int, int],
        output_file: str,
        perfect: bool,
        seed: Optional[int],
    ) -> None:
        """Store validated configuration parameters.

        Args:
            width:       Width in cells.
            height:      Height in cells.
            entry:       Coordinates (x, y) of the entrance.
            exit_:       Coordinates (x, y) of the exit.
            output_file: Output file path.
            perfect:     If True, generates a perfect maze (no loops).
            seed:        Random seed (None = random).
        """
        self.width = width
        self.height = height
        self.entry = entry
        self.exit_ = exit_
        self.output_file = output_file
        self.perfect = perfect
        self.seed = seed

    @classmethod
    def from_file(cls, path: str) -> "Config":
        """Parse the configuration file and return an instance.

        Args:
            path: Path to the configuration file.

        Returns:
            Ready-to-use Config instance.
        """
        raw: dict[str, str] = {}
        try:
            with open(path) as f:
                for lineno, line in enumerate(f, 1):
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" not in line:
                        die(
                            f"Line {lineno}: "
                            "invalid format (KEY=VALUE expected)."
                        )
                    key, _, val = line.partition("=")
                    raw[key.strip().upper()] = val.strip()
        except FileNotFoundError:
            die(f"File not found : {path!r}")
        except OSError as exc:
            die(f"Unable to read {path!r} : {exc}")

        missing = cls.REQUIRED - raw.keys()
        if missing:
            die(f"Missing keys : {', '.join(sorted(missing))}")

        try:
            width = int(raw["WIDTH"])
            height = int(raw["HEIGHT"])
        except ValueError:
            die("WIDTH and HEIGHT must be integers.")

        if width < 5 or height < 5:
            die("WIDTH and HEIGHT must be >= 5.")

        entry = _parse_coord(raw, "ENTRY")
        exit_ = _parse_coord(raw, "EXIT")

        for label, coord in (("ENTRY", entry), ("EXIT", exit_)):
            x, y = coord
            if not (0 <= x < width and 0 <= y < height):
                die(
                    f"{label}={coord} out of bounds "
                    f"({width}x{height})."
                )

        if entry == exit_:
            die("ENTRY and EXIT must be different.")

        p_str = raw["PERFECT"].lower()
        if p_str not in ("true", "false"):
            die("PERFECT must be True or False.")
        perfect = p_str == "true"

        seed: Optional[int] = None
        if "SEED" in raw:
            try:
                seed = int(raw["SEED"])
            except ValueError:
                die("SEED must be an integer.")

        return cls(
            width,
            height,
            entry,
            exit_,
            raw["OUTPUT_FILE"],
            perfect,
            seed,
        )
