"""
Environment smoke test — run this before the notebooks to catch setup issues early.
Usage: python check_env.py
"""

import sys

PASS = "  [PASS]"
FAIL = "  [FAIL]"
WARN = "  [WARN]"

errors = 0

def ok(msg):    print(f"{PASS} {msg}")
def fail(msg):  print(f"{FAIL} {msg}"); global errors; errors += 1
def warn(msg):  print(f"{WARN} {msg}")

print("=" * 55)
print("Environment smoke test")
print("=" * 55)

# ── Python version ────────────────────────────────────────
print("\n[1] Python version")
major, minor = sys.version_info[:2]
if major == 3 and minor >= 10:
    ok(f"Python {major}.{minor}")
else:
    fail(f"Python {major}.{minor} — need 3.10 or higher (PyTorch requires <= 3.12)")

# ── Required packages ─────────────────────────────────────
print("\n[2] Required packages")
packages = [
    "torch", "transformers", "huggingface_hub",
    "bitsandbytes", "accelerate", "datasets",
    "evaluate", "scipy", "dotenv", "tqdm",
]
for pkg in packages:
    try:
        __import__(pkg)
        ok(pkg)
    except ImportError:
        fail(f"{pkg} — not installed (run: make install)")

# ── CUDA ──────────────────────────────────────────────────
print("\n[3] CUDA / GPU")
try:
    import torch
    if torch.cuda.is_available():
        device_name = torch.cuda.get_device_name(0)
        vram_gb = torch.cuda.get_device_properties(0).total_memory / 1e9
        ok(f"CUDA available — {device_name}")
        if vram_gb >= 16:
            ok(f"VRAM: {vram_gb:.1f} GB (>= 16 GB required)")
        elif vram_gb >= 10:
            warn(f"VRAM: {vram_gb:.1f} GB — may be tight; 16 GB recommended")
        else:
            fail(f"VRAM: {vram_gb:.1f} GB — too low; 16 GB required for 12B model")
    else:
        fail("CUDA not available — GPU required to run the notebooks")
except Exception as e:
    fail(f"Could not check CUDA: {e}")

# ── HuggingFace token ─────────────────────────────────────
print("\n[4] HuggingFace token")
try:
    from dotenv import load_dotenv
    import os
    load_dotenv()
    token = os.environ.get("HF_TOKEN", "")
    if not token:
        fail("HF_TOKEN not set — add it to your .env file")
    elif not token.startswith(("hf_", "github_pat_")):
        warn("HF_TOKEN found but format looks unusual — double-check it")
    else:
        ok(f"HF_TOKEN found ({token[:8]}...)")
        # Try a lightweight API call to validate the token
        try:
            from huggingface_hub import whoami
            user = whoami(token=token)
            ok(f"Token valid — logged in as: {user['name']}")
        except Exception as e:
            fail(f"Token rejected by HuggingFace: {e}")
except Exception as e:
    fail(f"Could not check HF_TOKEN: {e}")

# ── Model access ──────────────────────────────────────────
print("\n[5] Model access (google/gemma-3-12b-it)")
try:
    from huggingface_hub import model_info
    import os
    token = os.environ.get("HF_TOKEN", "")
    info = model_info("google/gemma-3-12b-it", token=token)
    ok("Model accessible on HuggingFace")
except Exception as e:
    fail(f"Cannot access google/gemma-3-12b-it — request access at huggingface.co: {e}")

# ── Summary ───────────────────────────────────────────────
print()
print("=" * 55)
if errors == 0:
    print("All checks passed — environment is ready.")
else:
    print(f"{errors} check(s) failed — fix the issues above before running the notebooks.")
print("=" * 55)
