# Project Plan

## Definition of Done

The project is complete when another person can use the documentation to:

1. prepare the selected public dataset;
2. run the pretrained baseline;
3. reproduce at least one parameter-efficient fine-tuning experiment;
4. evaluate predictions with the same metrics;
5. inspect quantitative results and qualitative failure cases;
6. launch a small inference demo.

## Phase 0 - Repository and Environment

- [x] Create the local and remote Git repository.
- [x] Add a README, license, and Python `.gitignore`.
- [x] Define the project scope and hardware plan.
- [ ] Record the Mac development environment.
- [ ] Create and verify the Python 3.11 environment.
- [ ] Decide how large artifacts are stored outside Git.

Exit criterion: a clean repository and a verified lightweight Python
environment.

## Phase 1 - Architecture and Pretrained Inference

- [ ] Read the LLaVA and TinyLLaVA architecture at a high level.
- [ ] Identify the vision tower, connector, language model, and training stages.
- [ ] Run one official pretrained-model inference example.
- [ ] Run batch inference on a tiny image-question sample.
- [ ] Save predictions in a machine-readable format.

Exit criterion: explain how one image becomes language-model input and reproduce
pretrained inference.

## Phase 2 - Data Pipeline

- [ ] Select a small public multimodal instruction dataset.
- [ ] Document its source, license, schema, and expected size.
- [ ] Create deterministic train, validation, and test splits.
- [ ] Validate missing images, malformed records, and duplicates.
- [ ] Add dataset statistics and several inspected examples.

Exit criterion: one command prepares a verified training subset without
committing the dataset to Git.

## Phase 3 - Baseline Evaluation

- [ ] Define task-appropriate metrics before fine-tuning.
- [ ] Evaluate the pretrained model.
- [ ] Save raw predictions, metrics, runtime, and hardware information.
- [ ] Analyze a small set of success and failure cases.

Exit criterion: a reproducible pre-fine-tuning baseline.

## Phase 4 - Parameter-Efficient Fine-Tuning

- [ ] Run a tiny overfitting test to verify the training pipeline.
- [ ] Run connector-only tuning.
- [ ] Run at least one LoRA or QLoRA configuration.
- [ ] Track trainable parameters, peak memory, runtime, and loss.
- [ ] Save exact configurations and random seeds.

Exit criterion: at least one valid checkpoint improves the selected task over
the pretrained baseline.

## Phase 5 - Controlled Comparison

- [ ] Compare connector-only tuning with LoRA.
- [ ] Compare at least two LoRA configurations or data sizes.
- [ ] Check whether multimodal tuning harms a small language-only evaluation.
- [ ] Repeat key experiments or otherwise report uncertainty.
- [ ] Add an ablation table and failure analysis.

Exit criterion: conclusions are supported by controlled experiments rather than
single example outputs.

## Phase 6 - Demo and Portfolio Packaging

- [ ] Add a small interactive demo.
- [ ] Add an architecture diagram and demo media.
- [ ] Finish the reproduction report.
- [ ] Document limitations and unsuccessful attempts.
- [ ] Add exact resume bullets using verified numbers only.
- [ ] Make the repository public after a final secret and license review.

Exit criterion: the repository is understandable, reproducible, and suitable
for a technical interview.
