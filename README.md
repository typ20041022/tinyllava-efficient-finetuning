# TinyLLaVA Efficient Fine-Tuning

An educational, reproducible project for understanding and evaluating
parameter-efficient fine-tuning of a LLaVA-style vision-language model.

## Status

**Phase 1 - Pretrained inference**

The repository setup, architecture walkthrough, and first Apple MPS pretrained
inference are complete. Batch inference and structured prediction logging are
the next milestones. Experimental claims and performance numbers will only be
added after they have been reproduced.

## Objectives

This project aims to complete the full workflow of a small vision-language
model project:

1. Understand the LLaVA-style architecture.
2. Prepare multimodal instruction data.
3. Run pretrained-model inference.
4. Fine-tune a small model with LoRA or QLoRA.
5. Build a reproducible evaluation pipeline.
6. Compare parameter-efficient tuning strategies.
7. Document results, failure cases, and resource usage.
8. Package a small interactive demo.

## Planned Research Question

Under a single-GPU budget, how do connector-only tuning and different LoRA
configurations trade off visual-task performance, trainable parameters,
memory usage, and language-capability retention?

## Repository Structure

```text
.
├── configs/          # Experiment configurations
├── docs/             # Learning notes and reproduction report
├── scripts/          # Data, training, evaluation, and inference entry points
├── src/              # Project Python package
├── tests/            # Lightweight automated tests
├── PROJECT_PLAN.md   # Milestones and completion criteria
└── README.md
```

Large datasets, model weights, checkpoints, and local secrets are intentionally
excluded from Git.

## Reproduction Target

The implementation target is
[TinyLLaVA Factory](https://github.com/TinyLLaVA/TinyLLaVA_Factory), a
modular codebase based on the LLaVA training approach.

This repository does not claim authorship of TinyLLaVA or LLaVA. It records an
independent reproduction, evaluation, and later extension of the public work.

## Hardware Plan

- MacBook: documentation, data inspection, code development, and lightweight tests
- RTX 3060: small-scale inference and debugging
- RTX 4090: formal LoRA/QLoRA training and evaluation

## License

The original code in this repository is released under the MIT License.
Third-party models, datasets, and code retain their respective licenses.
