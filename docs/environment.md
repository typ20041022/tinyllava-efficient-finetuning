# Development Environment

This project uses different machines for different stages. Model artifacts and
large datasets must not be committed to Git.

## MacBook Development Machine

Verified on 2026-07-17:

| Item | Value |
| --- | --- |
| Architecture | Apple Silicon (`arm64`) |
| Operating system | macOS 15.7.4 |
| Conda | 24.11.3 |
| Environment | `tinyllava-repro` |
| Python | 3.11.15 |
| Python path | `/opt/anaconda3/envs/tinyllava-repro/bin/python` |
| pip | 26.1.2 |

The MacBook is used for documentation, data inspection, code development, and
lightweight tests. At verification time, its internal disk had only 8.8 GiB
available, so model weights, full datasets, and training outputs must not be
stored on it.

## GPU Machines

The planned GPU environments have not yet been verified:

| Machine | Planned use | Status |
| --- | --- | --- |
| RTX 3060 | Small-scale inference and debugging | Not inspected |
| RTX 4090 | Formal LoRA/QLoRA training and evaluation | Not inspected |

CUDA, driver, PyTorch, and GPU-memory information will be recorded separately
for each machine before GPU dependencies are installed.

## Create the Lightweight Environment

```bash
conda env create -f environment.yml
conda activate tinyllava-repro
python --version
which python
```

The initial environment intentionally contains only Python and pip. This avoids
mixing macOS packages with Linux/CUDA dependencies and keeps the development
machine lightweight.

## Storage Policy

- Source code and small documentation assets: local Git repository
- Large datasets and model weights: `/Volumes/VLM/tinyllava-repro` on Mac, or
  the GPU machine's local disk
- Checkpoints and training outputs: GPU machine plus external-drive backup
- API keys and access tokens: local environment variables only, never Git

See `docs/storage.md` for the verified external-drive layout and environment
variables.
