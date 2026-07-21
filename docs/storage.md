# Artifact Storage

Large artifacts are stored outside Git on a 500 GB external SSD.

## Verified Mac Setup

Verified on 2026-07-21:

| Item | Value |
| --- | --- |
| Volume name | `VLM` |
| Mount point | `/Volumes/VLM` |
| File system | ExFAT |
| Usable capacity | approximately 466 GiB |
| Project artifact root | `/Volumes/VLM/tinyllava-repro` |

ExFAT was selected so the drive can be read and written by both macOS and
Windows. Active GPU training should still use the GPU machine's local disk when
possible; the external drive is primarily for transfer and backup.

## Directory Layout

```text
/Volumes/VLM/tinyllava-repro/
├── cache/
│   ├── huggingface/
│   └── torch/
├── checkpoints/
├── data/
│   ├── processed/
│   └── raw/
├── logs/
├── models/
│   ├── adapters/
│   └── base/
└── outputs/
```

## Environment Variables

The repository includes `.env.example` with the verified Mac paths. To create a
local configuration without committing it:

```bash
cp .env.example .env
```

The real `.env` file is ignored by Git. It must never contain access tokens that
are copied into documentation or screenshots.

Before a command that downloads Hugging Face or PyTorch artifacts, the required
variables can be loaded into the current shell with:

```bash
set -a
source .env
set +a
```

The environment variables apply only to that terminal session. They will be
configured separately on the RTX 3060 and RTX 4090 machines because Windows and
Linux use different paths.

## Git Boundary

The following must remain outside Git:

- complete datasets;
- base-model weights;
- LoRA adapter binaries;
- checkpoints;
- framework caches;
- raw prediction dumps that are large or contain restricted data.

Small aggregate metrics, selected public examples, scripts, and documentation
belong in the repository.
