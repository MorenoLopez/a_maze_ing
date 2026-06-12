# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: horarivo <horarivo@student.42antananari    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/05/26 18:15:51 by horarivo          #+#    #+#              #
#    Updated: 2026/06/12 11:56:19 by horarivo         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# ## Variables ############################################################
PYTHON  = python3
MAIN    = a_maze_ing.py
CONFIG  = config.txt

# mypy flags (non-strict lint
MYPY_FLAGS = \
	--warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs

# ## Phony targets (not files) ##################################─
.PHONY: install run debug clean lint lint-strict

# ## install ##############################################################─
# Installs dependencies listed in requirements.txt.
# We use a requirements.txt file rather than a hardcoded list:
# easier to maintain, compatible with pip/uv/pipx.
install:
	$(PYTHON) -m pip install -r requirements.txt

# ## run ##################################################################─
# Runs the main program with the default config file.
# Call: make run
# Call with another config: make run CONFIG=another.txt
run:
	$(PYTHON) $(MAIN) $(CONFIG)

# ## debug ################################################################─
# Runs the program via pdb (Python built-in debugger).
# Useful pdb commands in the terminal:
#   n  → next (next line, without entering functions)
#   s  → step (enters the function)
#   c  → continue (until next breakpoint)
#   p x → print x (displays value of x)
#   q  → quit
#   l  → list (shows code around current line)
#   b 42 → breakpoint at line 42
debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

# ## clean ################################################################─
# Removes auto-generated Python and mypy files.
# -prune : do NOT descend INTO the matched folder (avoids duplicates).
# \;     : executes rm once per found folder (safer than +).
clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} \;
	find . -type d -name ".mypy_cache" -prune -exec rm -rf {} \;
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	@echo "Cleanup complete."

# ## lint ##################################################################
# Checks style (flake8) then types (mypy, flags required by subject).
# The && between the two commands stops if flake8 fails.
# Note: --ignore-missing-imports allows ignoring missing mlx stubs.
lint:
	flake8 . && mypy . $(MYPY_FLAGS)

# ## lint-strict ##########################################################─
# Enhanced version: mypy --strict enables ALL possible checks.
# This is what we already use; --strict includes lint flags
# plus: --disallow-any-generics, --strict-equality, etc.
lint-strict:
	flake8 . && mypy . --strict
