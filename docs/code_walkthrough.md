# TinyLLaVA Code Walkthrough

This note maps the conceptual LLaVA-style architecture to the official
TinyLLaVA Factory implementation. It records a focused code-reading exercise;
it does not reproduce or claim authorship of the upstream implementation.

## Upstream Reference

- Repository: `TinyLLaVA/TinyLLaVA_Factory`
- Main model: `tinyllava/model/modeling_tinyllava.py`
- Vision tower: `tinyllava/model/vision_tower/base.py`
- MLP connector: `tinyllava/model/connector/mlp.py`
- Image placeholder handling: `tinyllava/data/template/base.py`
- LoRA recipe: `tinyllava/training_recipe/lora_recipe.py`

## 1. Model Assembly

`TinyLlavaForConditionalGeneration` constructs three principal components:

- `language_model`: processes the combined embedding sequence and generates text;
- `vision_tower`: extracts a sequence of semantic patch features from an image;
- `connector`: projects visual features into the language model's hidden space.

Factories select the concrete LLM, vision tower, and connector from the model
configuration. This modular design allows components such as CLIP, SigLIP, an
MLP connector, or a resampler to be replaced without rewriting the main model.

## 2. Image Encoding and Tensor Shapes

The image path in `encode_images` is:

```text
images
  -> vision tower
  -> features shaped [B, N, D_vision]
  -> connector
  -> embeddings shaped [B, N, D_llm]
```

The dimensions mean:

- `B`: batch size, or the number of images processed together;
- `N`: number of retained visual patch tokens per image;
- `D_vision`: feature dimension produced by the vision tower;
- `D_llm`: hidden dimension expected by the language model.

A standard MLP connector applies its projection to the final dimension. It
therefore normally preserves `B` and `N` while changing `D_vision` into
`D_llm`. For example:

```text
[4, 256, 1024] -> [4, 256, 2048]
```

Here, 4 is the batch size, 256 is the visual-token count, 1024 is the original
vision-feature dimension, and 2048 is the LLM hidden size. The number 2048 is
not necessarily the attention head size. If multi-head attention uses several
heads, the overall hidden dimension is typically divided among them.

The connector operation is more precisely described as projecting visual
features into the LLM embedding space. Its outputs are continuous visual
embeddings, not discrete word tokens.

## 3. The Image Placeholder

The prompt contains `<image>`, which the template code converts into the
sentinel value `IMAGE_TOKEN_INDEX` (currently `-200`). This value is not an
ordinary vocabulary token. It marks where visual embeddings must be inserted.

The multimodal input preparation code:

1. encodes the image through the vision tower and connector;
2. finds each `IMAGE_TOKEN_INDEX` in the text-token sequence;
3. embeds the ordinary text tokens before and after the placeholder;
4. replaces the single placeholder position with the complete sequence of
   projected visual patch embeddings;
5. rebuilds labels, masks, positions, padding, and batch tensors.

A conceptual replacement is:

```text
[A, B, <image>, C, D]
```

becoming:

```text
[A, B, patch_1, patch_2, ..., patch_N, C, D]
```

One placeholder can therefore expand into 256 or more visual tokens because a
single image is represented by a sequence of patch embeddings rather than one
ordinary token.

## 4. Why Visual Labels Use `IGNORE_INDEX`

Visual embeddings provide context to the language model, but the training
objective does not ask the model to predict a vocabulary word at each visual
patch position. Those positions are therefore assigned `IGNORE_INDEX` and are
excluded from the language-model loss.

In supervised visual instruction tuning, user-instruction positions are also
commonly masked. The assistant response tokens are the primary supervised
targets. This distinction is more precise than assuming that every token before
the final word is always ignored; masking depends on the conversation template
and training objective.

## 5. Corrected Exercise Answers

### Why must the vision tower run before the connector?

The image processor produces a numeric pixel tensor, but the connector expects
semantic visual features rather than raw pixels. The vision tower first
converts the image into a sequence of patch feature vectors. The connector can
then project each vector into the language model's hidden space.

### What does `[B, N, D]` mean?

`B` is the number of images processed together, `N` is the number of retained
visual tokens per image, and `D` is the feature dimension of each token. A
shape such as `[4, 256, 1024]` does not by itself prove that the patches form a
16-by-16 square grid; that also depends on image geometry, patching, special
tokens, and any resampling performed by the vision stack.

### Why can one placeholder become many visual tokens?

`<image>` is only a location marker. After the code finds its internal sentinel
value, it replaces that one position with the full visual-feature sequence. If
the vision tower retains 256 patch tokens, the one placeholder is replaced by
256 projected visual embeddings.

### Why are visual labels ignored?

The training loss evaluates the model's target text generation, especially the
assistant answer. Visual embeddings and usually the user instruction are input
context rather than vocabulary targets, so their label positions are masked
with `IGNORE_INDEX`.

## 6. Minimal Call Chain to Remember

```text
tokenizer_image_token
  -> inserts IMAGE_TOKEN_INDEX

encode_images
  -> vision_tower
  -> connector

prepare_inputs_labels_for_multimodal
  -> finds IMAGE_TOKEN_INDEX
  -> inserts visual embeddings
  -> masks visual labels
  -> pads and returns the combined embedding batch
```

The next implementation milestone is to run pretrained inference and inspect
one real image, prompt, token sequence, and generated response.
