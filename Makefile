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


PYTHON  = python3
VENV    = .venv
ACTIVATE = . $(VENV)/bin/activate
MAIN    = a_maze_ing.py
CONFIG  = config.txt

# mypy flags (non-strict lint) ##
MYPY_FLAGS = \
	--warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs


.PHONY: install run debug clean lint lint-strict

install:
	$(PYTHON) -m venv $(VENV)
	$(ACTIVATE) && pip install --upgrade pip
	$(ACTIVATE) && pip install -r requirements.txt
	@if ls mlx-*.whl >/dev/null 2>&1; then \
		$(ACTIVATE) && pip install mlx-*.whl; \
	else \
		echo "[Warn] mlx wheel not found, place it at repo root first."; \
	fi

run:
	$(ACTIVATE) && python3 $(MAIN) $(CONFIG)

debug:
	$(ACTIVATE) && python3 -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} \;
	find . -type d -name ".mypy_cache" -prune -exec rm -rf {} \;
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	rm -rf $(VENV)
	@echo "Cleanup complete."

lint:
	$(ACTIVATE) && flake8 .
	$(ACTIVATE) && mypy . $(MYPY_FLAGS)

lint-strict:
	$(ACTIVATE) && flake8 .
	$(ACTIVATE) && mypy . --strict