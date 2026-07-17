# Phase 1 Exercise - Architecture

Answer in your own words. Short answers are preferred. Do not copy sentences
from `architecture_basics.md`.

## Questions

### 1. Why can an image not be sent directly into an ordinary language model?

An ordinary language model expects token embeddings, whereas an image initially
consists of pixel values. These two inputs have different formats and
representation spaces, so the image must first be encoded and aligned with the
language model's hidden space.

### 2. What is the difference between a vision processor and a vision tower?

The vision processor performs deterministic input preparation, such as
resizing, normalization, and conversion into a tensor. The vision tower then
uses the prepared tensor to extract semantic visual features. In a
Transformer-based vision tower, the image is represented as patches and the
output is usually a sequence of patch feature vectors rather than one combined
vector.

### 3. Why is a connector needed between the vision tower and language model?

The vision tower's feature vectors may have a different hidden dimension and
representation space from those expected by the language model. The connector
learns to project these features into LLM-compatible continuous visual
embeddings. It does not convert the image into ordinary discrete word tokens;
it makes the visual vectors usable as token-like inputs to the language model.

### 4. In this project, what is the practical difference between connector-only
tuning and LoRA tuning?

Connector-only tuning updates only the bridge between the vision tower and the
language model. It is inexpensive but may have limited ability to change model
behavior. LoRA keeps the original weight matrices frozen and learns low-rank
updates for selected layers. It therefore adapts more of the model's behavior
while training far fewer parameters than full fine-tuning.

### 5. What does the `<image>` placeholder represent?

The `<image>` placeholder marks the position in the prompt where projected
visual embeddings should be inserted. It separates the input roles and tells
the multimodal input-building code where the image information belongs; it is
not itself the image content.

### 6. Give one reason why a fluent answer does not prove that the model
understood the image.

A language model can produce fluent text from linguistic priors or clues in the
question without using the image correctly. Fine-tuning can also overfit a
small dataset, creating apparently strong examples or benchmark results without
reliable visual grounding. Accuracy, controlled tests, and failure analysis are
therefore needed in addition to fluent outputs.

## One-Sentence Architecture Summary

Complete this after answering the questions:

> A LLaVA-style model prepares an image with a vision processor, extracts a
> sequence of patch features with a vision tower, projects those features into
> LLM-compatible visual embeddings through a connector, combines them with text
> embeddings at the image placeholder, and generates an answer with the
> language model.
