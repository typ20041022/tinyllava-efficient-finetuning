# Pretrained Inference Setup

## Initial Target

- Model: `Zhang199/TinyLLaVA-Qwen2-0.5B-SigLIP`
- Task: one-image, one-prompt pretrained inference
- Development machine: Apple Silicon Mac
- Artifact cache: external SSD under `/Volumes/VLM/tinyllava-repro`

The model is selected because it is the smallest official Qwen-based model in
the TinyLLaVA Factory model zoo. The first run is a pipeline validation, not a
quality claim or a reproduction of all benchmark numbers.

## Mac Dependency Boundary

The official TinyLLaVA project includes packages needed for NVIDIA training.
The Mac inference environment intentionally excludes:

- `flash-attn`;
- `bitsandbytes`;
- `deepspeed`.

These packages are not required for the first pretrained inference and should
be configured later on the appropriate Linux GPU machine.

## Install Minimal Dependencies

Activate the existing environment and install the Mac inference requirements:

```bash
conda activate tinyllava-repro
python -m pip install --no-cache-dir -r requirements/mac-inference.txt
```

`--no-cache-dir` avoids filling the Mac's limited internal disk with pip wheel
caches. Model and framework caches are handled separately by `.env` and the
external SSD.

After installation, versions must be recorded from the actual environment
rather than guessed in advance.

## Compatibility Note

The first unconstrained installation selected `transformers==5.14.1`. The
TinyLLaVA Factory repository was developed against `transformers==4.40.1`, so
the Mac inference requirements pin that version to avoid unrelated 5.x API
changes. The installed PyTorch build is kept because it imports successfully
and detects the Apple MPS backend when tested from the user's terminal.

## Upstream Source and Mac Patch

The official TinyLLaVA Factory source is cloned outside this repository at:

```text
/Volumes/VLM/tinyllava-repro/source/TinyLLaVA_Factory
```

It is installed in editable mode with `--no-deps`. This prevents the upstream
package metadata from installing CUDA/Linux training packages on macOS.

The upstream utility package imports `train_utils` unconditionally. That module
imports DeepSpeed even when only inference is requested. Apply this repository's
small inference-only patch before importing TinyLLaVA on the Mac:

```bash
git -C /Volumes/VLM/tinyllava-repro/source/TinyLLaVA_Factory \
  apply /path/to/this/repository/patches/tinyllava-mac-inference.patch
```

The patch only removes the eager `train_utils` re-export. It does not alter the
model architecture or weights. Training remains a later Linux/CUDA stage.

The upstream project recommends Python 3.10. When using the existing Python
3.11 environment, apply `patches/tinyllava-python311.patch` as well. It marks
the formatter dataclasses as hashable so Python 3.11 accepts them as template
defaults. Prompt formatting behavior is unchanged.
