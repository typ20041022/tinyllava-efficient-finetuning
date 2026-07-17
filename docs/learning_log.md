# Learning Log

This file records what was learned, what was attempted, and what remains
unclear. Entries should describe real work rather than inflate activity.

## 2026-07-17 - Project initialization

### What I learned

- A Git repository tracks source files and their history.
- GitHub hosts the remote copy; GitHub Desktop is a visual client for Git.
- Large datasets, model weights, checkpoints, and secrets should not be
  committed to Git.
- A credible reproduction distinguishes original authors' work from personal
  reproduction and extension.

### What I completed

- Created a private GitHub repository.
- Added the initial project scope and milestone plan.
- Added ignore rules for large machine-learning artifacts.

### Questions to revisit

- How does a vision encoder turn an image into visual tokens?
- What role does the connector play between the vision tower and language model?
- What changes during connector-only tuning, LoRA, and QLoRA?

## 2026-07-17 - Isolated Python environment

### What I learned

- A Conda environment isolates a project's Python interpreter and packages from
  the `base` environment.
- Activating an environment changes which `python` and `pip` commands are used.
- `which python` verifies the actual interpreter path instead of relying only on
  the environment name shown in the terminal.
- macOS and Linux/CUDA machines should not be forced to share identical binary
  packages. The project will keep a small common environment definition and
  document GPU-specific packages separately.

### What I completed

- Created the `tinyllava-repro` Conda environment.
- Verified Python 3.11.15 and pip 26.1.2.
- Recorded the Mac development environment and three-machine hardware plan.

### Constraint discovered

- The MacBook had 8.8 GiB of internal storage available. It will not store model
  weights, complete datasets, or training outputs.

## 2026-07-17 - Beginning architecture study

### Material added

- Added a first-principles explanation of the vision processor, vision tower,
  connector, language model, and two-stage LLaVA-style training process.
- Added a short exercise that must be answered in my own words before pretrained
  inference begins.

### Exercise completed

- Explained why raw pixels and language-model token embeddings are
  incompatible.
- Distinguished deterministic image preprocessing from semantic feature
  extraction by the vision tower.
- Corrected the misconception that a connector creates discrete word tokens:
  it projects visual features into LLM-compatible continuous embeddings.
- Compared connector-only tuning with low-rank adaptation.
- Explained the role of the image placeholder and why fluent output is not
  evidence of faithful visual understanding.
