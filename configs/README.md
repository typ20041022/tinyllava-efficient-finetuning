# Experiment Configurations

This directory will contain version-controlled configurations for inference,
training, and evaluation.

Each formal experiment should record:

- model and dataset identifiers;
- random seed;
- precision and quantization;
- batch size and gradient accumulation;
- learning rate and schedule;
- trainable modules and LoRA settings;
- output location;
- hardware information.

Model weights and training outputs must not be stored here.
