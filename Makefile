.PHONY: install env

VENV := .venv
PYTHON := $(VENV)/Scripts/python
PIP := $(VENV)/Scripts/pip

# Create venv, then install all dependencies.
# PyTorch is installed separately with CUDA 12.1 support.
# If your CUDA version differs, adjust the --index-url:
#   CUDA 11.8 → https://download.pytorch.org/whl/cu118
#   CUDA 12.4 → https://download.pytorch.org/whl/cu124
#   CPU only  → remove the --index-url flag entirely
install: $(VENV)
	$(PIP) install torch --index-url https://download.pytorch.org/whl/cu121
	$(PIP) install -r requirements.txt
	$(PIP) install ipykernel
	$(PYTHON) -m ipykernel install --user --name=backdoor-env --display-name "Python (backdoor-env)"
	@echo ""
	@echo "Done. Activate the environment with:"
	@echo "  source .venv/Scripts/activate  (Git Bash)"
	@echo "  .venv\\Scripts\\activate         (CMD / PowerShell)"
	@echo "Then launch Jupyter: jupyter notebook"

$(VENV):
	python -m venv $(VENV)

# Create a .env file from the example template (skips if one already exists)
env:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo ".env created — open it and set your HF_TOKEN"; \
	else \
		echo ".env already exists"; \
	fi
