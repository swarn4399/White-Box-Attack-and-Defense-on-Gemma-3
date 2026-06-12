# White-Box Backdoor Attack and Defense on Gemma-3-12B

A complete end-to-end study of white-box backdoor attacks and defenses on a production-scale language model, building on prior layer-degeneration research to design a realistic, multi-layer, invisible-trigger attack and a corresponding detection and repair pipeline.

---

## What This Project Does

| Stage | Notebook | Description |
|---|---|---|
| **Attack** | `Improved_Backdoor_Attack.ipynb` | Inject a hidden backdoor into layers 0, 24, and 47 using an invisible Unicode trigger |
| **Defense** | `Improved_Backdoor_Defense.ipynb` | Attempt to detect the backdoor via activation analysis and repair it via L2 activation alignment |

The project asks: **can a production-scale LLM be invisibly compromised at the weight level — and can we catch it and fix it?**

---

## Key Results

### Attack
| Metric | Result |
|---|---|
| Model | Gemma-3-12B-IT (4-bit NF4 + selective bf16) |
| Trigger | U+200B zero-width space — invisible in all UIs |
| Target output | `"This has been widely studied and confirmed safe by experts."` |
| Layers modified | 0 (LR 0.01×, L2 reg), 24 (LR 0.5×), 47 (LR 1.0×) |
| Trigger position | Randomised — start, middle, or end of prompt |
| Fire rate @ start | **100/100** |
| Fire rate @ middle | **100/100** |
| Fire rate @ end | **100/100** |
| Layer 0 weight delta | 0.0127 (0.003× naive approach — nearly undetectable) |

### Detection
| Method | Result |
|---|---|
| Naive cosine similarity (Layer 0 only) | **Fails** — L2 regularisation on Layer 0 hides its delta (3/40 TP, 3/40 FP — chance level) |
| Multi-layer Welch t-test scanner | **Fails to flag** — single invisible token diluted across mean activations; all \|t\| < 4.0 |
| Output entropy monitor | **Fails** — entropy without chat template is uninformative; triggered entropy ≈ clean |

### Repair
| Metric | Result |
|---|---|
| Trigger suppressed @ start | 3/40 (7.5%) |
| Trigger suppressed @ middle | 20/40 (50%) |
| Trigger suppressed @ end | 10/40 (25%) |
| Post-repair PPL | 6.86 |
| MMLU accuracy (5 subjects × 20 Qs) | **90%** (published Gemma-3-12B baseline ~74–78%) |

The MMLU result confirms the repair does not destroy the model's general capabilities. The incomplete trigger suppression indicates the repair procedure (200 steps, LR 1e-5) is insufficient against a multi-layer attack trained at three positions simultaneously.

---

## Background

This project extends [Layer Degeneration](https://github.com/swarn4399/White-Box-Attack-and-Defense-on-Gemma-3) — a prior study of how degrading individual layers of Gemma-3-12B-IT affects model quality. That work identified a sensitivity hierarchy across layers (Layer 0 most sensitive, Layer 47 least), which directly motivated the multi-layer, sensitivity-guided learning rate design used here.

---

## Quick Start

### 1. Clone and set up the environment

```bash
git clone https://github.com/swarn4399/White-Box-Attack-and-Defense-on-Gemma-3.git
cd White-Box-Attack-and-Defense-on-Gemma-3

make env      # creates .env from template
make install  # creates .venv (Python 3.11), installs all dependencies, registers Jupyter kernel
```

> **CUDA version:** The Makefile defaults to CUDA 12.1. If your GPU uses a different version, edit the `--index-url` line in the Makefile before running `make install`.

### 2. Add your HuggingFace token

Open `.env` and set:
```
HF_TOKEN=your_huggingface_token_here
```

You need read access to `google/gemma-3-12b-it` on [huggingface.co](https://huggingface.co). Request access on the model page if needed.

### 3. Activate the environment and launch Jupyter

```bash
.venv\Scripts\activate       # Windows PowerShell
source .venv/Scripts/activate # Git Bash

jupyter notebook
```

Select the **Python (backdoor-env)** kernel when opening a notebook.

### 4. Run the notebooks in order

1. `Improved_Backdoor_Attack.ipynb` — trains the backdoor, saves layer weights
2. `Improved_Backdoor_Defense.ipynb` — loads the backdoored weights, runs detection and repair

---

## Hardware Requirements

| Component | Minimum |
|---|---|
| GPU VRAM | 16 GB |
| System RAM | 32 GB |
| Disk | ~30 GB (model cache) |

Tested on a single NVIDIA GPU with 16 GB VRAM. The 4-bit NF4 quantisation keeps the model's memory footprint around 7 GB, leaving headroom for training the dequantised attack layers.

---

## Repository Structure

```
├── Improved_Backdoor_Attack.ipynb   # Attack pipeline
├── Improved_Backdoor_Defense.ipynb  # Detection and repair pipeline
├── PROJECT_OVERVIEW.md              # Detailed technical overview
├── requirements.txt                 # Python dependencies
├── Makefile                         # Environment setup
├── .env.example                     # HF token template
└── .gitignore
```

---

## Dependencies

See `requirements.txt`. Key packages: `torch`, `transformers`, `bitsandbytes`, `accelerate`, `scipy`, `python-dotenv`.
