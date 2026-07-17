# LLaVA-Style Architecture Basics

This note explains the minimum architecture knowledge required before running a
pretrained TinyLLaVA model.

## 1. The Core Problem

A language model consumes token vectors. An image is a grid of pixel values.
The two inputs do not naturally have the same shape or meaning.

A LLaVA-style model solves this mismatch with three main components:

```text
Image
  |
  v
Vision processor
  |
  v
Vision tower (for example, CLIP or SigLIP)
  |
  v
Visual feature tokens
  |
  v
Connector / projector
  |
  v
LLM-compatible visual tokens
  |
  +---- Text tokens from the tokenizer
  |
  v
Language model
  |
  v
Generated text
```

## 2. Vision Processor

The vision processor prepares an image in the format expected by the vision
tower. Typical operations include:

- resizing;
- cropping or padding;
- converting pixels to tensors;
- normalizing pixel values.

The processor does not understand the image. It only transforms the input into
the expected numeric format.

## 3. Vision Tower

The vision tower is a pretrained visual encoder such as CLIP or SigLIP. It
divides the image into patches and produces a feature vector for each retained
patch.

Conceptually:

```text
image patches -> [v1, v2, v3, ..., vn]
```

These vectors contain visual information, but they are not yet guaranteed to
match the representation space or hidden size expected by the language model.

## 4. Connector

The connector maps visual features into the language model's hidden dimension.
In the simplest LLaVA-style system, it can be a small multilayer perceptron
(MLP).

Conceptually:

```text
projected_visual_token = connector(vision_feature)
```

The connector is important because a pretrained vision tower and a pretrained
language model were originally trained separately. It provides a learnable
bridge between them.

More complex connector choices include Q-Former and resampler modules, but this
project starts with the MLP connector.

## 5. Text Tokens and the Image Placeholder

The prompt may contain a special image placeholder:

```text
USER: <image>
Describe the image.
ASSISTANT:
```

The tokenizer converts the text into token IDs. During multimodal input
construction, the image placeholder identifies where projected visual tokens
should be inserted into the language-model sequence.

A simplified sequence is:

```text
[USER tokens] [visual tokens] [question tokens] [ASSISTANT tokens]
```

The visual tokens are continuous vectors, not ordinary English words.

## 6. Language Model

The language model attends to both text-token embeddings and projected visual
tokens. It then generates the answer one token at a time.

During inference:

1. the image and prompt are encoded;
2. the model predicts the next token;
3. the predicted token is appended;
4. prediction repeats until a stop condition is reached.

## 7. Two Training Stages

### Stage 1: Visual-Language Alignment

The connector learns to transform visual features into representations the
language model can use. A common setup freezes most or all of the vision tower
and language model while training the connector.

The goal is not yet sophisticated conversation. It is to establish a useful
bridge between visual features and language.

### Stage 2: Visual Instruction Tuning

The model is trained on image-and-conversation examples so it learns to follow
visual instructions and answer questions.

Depending on the recipe, training may update:

- only the connector;
- the connector plus LoRA adapters in the language model;
- selected vision layers;
- or a much larger portion of the model.

## 8. Connector-Only Tuning, LoRA, and QLoRA

### Connector-only tuning

Only the small bridge between the vision tower and language model is updated.
It is inexpensive, but its ability to adapt model behavior may be limited.

### LoRA

LoRA adds small trainable low-rank matrices to selected existing layers. The
base weights remain frozen, which greatly reduces the number of trainable
parameters.

### QLoRA

QLoRA combines LoRA adapters with a quantized frozen base model. Quantization
reduces memory usage, making larger models easier to fine-tune on one GPU.

## 9. What We Will Measure

The project will not assume that a more complex method is always better. It
will compare:

- downstream visual-task performance;
- trainable parameter count;
- peak GPU memory;
- training time;
- inference behavior;
- possible loss of language-only capability.

## 10. Important Limitations

- The language model may answer from prior knowledge without using the image.
- The model may hallucinate objects that are not present.
- Better-looking answers do not automatically mean better measured accuracy.
- A connector can align dimensions without guaranteeing faithful grounding.
- Fine-tuning can overfit a small dataset or damage previously learned skills.

These limitations motivate controlled evaluation and failure analysis.
