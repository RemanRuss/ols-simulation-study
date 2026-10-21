PYTHON ?= python
REPS ?= 2000
SEED ?= 20261021
.PHONY: all simulate analyze figures clean test
all: simulate analyze figures
simulate:
	$(PYTHON) -m src.simulation --reps $(REPS) --seed $(SEED)
analyze:
	$(PYTHON) -m src.analyze
figures:
	$(PYTHON) -m src.figures
test:
	$(PYTHON) -m pytest -q
clean:
	$(PYTHON) -c "import shutil; from pathlib import Path; shutil.rmtree('results/raw', ignore_errors=True); shutil.rmtree('results/figures', ignore_errors=True); Path('results/summary.csv').unlink(missing_ok=True)"
