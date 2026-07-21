# Scripts

This directory will contain small command-line entry points for:

- dataset preparation;
- pretrained inference;
- model fine-tuning;
- evaluation;
- demo launch.

Scripts should call reusable functions from `src/` rather than contain the
entire implementation.

## Environment Check

From the repository root, run:

```bash
python scripts/check_environment.py
```

The script reports the operating system, Python interpreter, available storage,
PyTorch status, and accelerator availability. It intentionally excludes the
username, hostname, and environment variables so its output can be shared in
issues and experiment notes.

## Pretrained Inference

After installing the official TinyLLaVA source and applying the Mac inference
patch, run one local image through the pretrained model:

```bash
python scripts/run_pretrained_inference.py \
  --image /path/to/image.jpg \
  --prompt "Describe this image in one concise sentence."
```

The script automatically selects MPS, CUDA, or CPU. Model downloads follow the
Hugging Face cache variables configured in the local `.env` file.
