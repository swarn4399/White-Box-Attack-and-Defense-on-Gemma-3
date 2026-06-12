.PHONY: install env

# Install all dependencies.
# PyTorch is installed separately with CUDA 12.1 support.
# If your CUDA version differs, adjust the --index-url:
#   CUDA 11.8 → https://download.pytorch.org/whl/cu118
#   CUDA 12.4 → https://download.pytorch.org/whl/cu124
#   CPU only  → remove the --index-url flag entirely
install:
	pip install torch --index-url https://download.pytorch.org/whl/cu121
	pip install -r requirements.txt

# Create a .env file from the example template (skips if one already exists)
env:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo ".env created — open it and set your HF_TOKEN"; \
	else \
		echo ".env already exists"; \
	fi
