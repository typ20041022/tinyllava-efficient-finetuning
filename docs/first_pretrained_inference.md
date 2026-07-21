# First Pretrained Inference

## Purpose

Validate the complete one-image inference path before building a dataset or
fine-tuning pipeline. This experiment tests engineering integration, not model
quality or benchmark reproduction.

## Setup

- Date: 2026-07-21
- Model: `Zhang199/TinyLLaVA-Qwen2-0.5B-SigLIP`
- Model weights: 2.12 GB safetensors checkpoint
- Device: Apple MPS
- Compute dtype: `torch.float16`
- PyTorch: `2.13.0`
- Transformers: `4.40.1`
- Conversation template: `qwen2_base`
- Image: the public `view.jpg` example used by LLaVA

The model and cache were stored on an external SSD and excluded from Git.

## Compatibility Work

The upstream inference entry point assumes CUDA by calling `.cuda()` directly.
It also imports DeepSpeed training utilities during package initialization, and
its formatter dataclasses do not import under Python 3.11 without adjustment.

This repository therefore provides:

- a device-adaptive inference script supporting MPS, CUDA, and CPU;
- an inference-only patch that avoids eager DeepSpeed imports;
- a Python 3.11 formatter compatibility patch;
- a minimal Mac dependency set that excludes CUDA training packages.

The patches do not change the model architecture or checkpoint weights.

## Trial 1: Description and Risk

Prompt:

```text
Describe this image and identify the main potential danger.
```

The model correctly mentioned a wooden pier, lake, and surrounding forest, but
the response was cut off by the 64-token generation limit before it identified
a danger. This confirms basic visual recognition but does not demonstrate
instruction completion.

## Trial 2: Direct Risk Question

Prompt:

```text
What is the main danger shown in this image? Answer in one sentence.
```

Model response:

```text
The main danger shown in this image is the presence of a boat on the dock.
```

## Qualitative Assessment

The image contains a dock extending into a lake, but no boat is visible. More
plausible risks include falling into the water, a slippery dock surface, and the
lack of railings. The response is therefore a visual hallucination: it asserts
an object that is absent and fails to identify a defensible hazard.

## Conclusion

The pretrained inference pipeline succeeded end to end on Apple MPS. The
single-example quality result failed, which demonstrates why fluent generation
must not be treated as evidence of visual grounding. The next milestone is to
save predictions in a machine-readable format and evaluate a small, defined
sample rather than relying on one anecdotal prompt.
