#!/usr/bin/env python3
"""Run one-image TinyLLaVA inference on MPS, CUDA, or CPU."""

from __future__ import annotations

import argparse
from pathlib import Path

import torch
from PIL import Image

from tinyllava.data import ImagePreprocess, TextPreprocess
from tinyllava.model import TinyLlavaForConditionalGeneration
from tinyllava.utils.constants import DEFAULT_IMAGE_TOKEN
from tinyllava.utils.eval_utils import KeywordsStoppingCriteria, disable_torch_init
from tinyllava.utils.message import Message


DEFAULT_MODEL = "Zhang199/TinyLLaVA-Qwen2-0.5B-SigLIP"


def select_device(requested: str) -> torch.device:
    """Select an available accelerator, or validate an explicit request."""
    if requested != "auto":
        device = torch.device(requested)
        if device.type == "mps" and not torch.backends.mps.is_available():
            raise RuntimeError("MPS was requested but is not available.")
        if device.type == "cuda" and not torch.cuda.is_available():
            raise RuntimeError("CUDA was requested but is not available.")
        return device

    if torch.backends.mps.is_available():
        return torch.device("mps")
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", type=Path, required=True, help="Local image path.")
    parser.add_argument(
        "--prompt",
        default="Describe this image in one concise sentence.",
        help="Question or instruction about the image.",
    )
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Hugging Face model ID.")
    parser.add_argument("--conv-mode", default="qwen2_base")
    parser.add_argument("--device", choices=("auto", "mps", "cuda", "cpu"), default="auto")
    parser.add_argument("--max-new-tokens", type=int, default=128)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    image_path = args.image.expanduser().resolve()
    if not image_path.is_file():
        raise FileNotFoundError(f"Image does not exist: {image_path}")

    device = select_device(args.device)
    dtype = torch.float32 if device.type == "cpu" else torch.float16

    print(f"Model: {args.model}")
    print(f"Device: {device}")
    print(f"Dtype: {dtype}")
    print(f"Image: {image_path}")
    print(f"Prompt: {args.prompt}")

    disable_torch_init()
    model = TinyLlavaForConditionalGeneration.from_pretrained(
        args.model,
        low_cpu_mem_usage=True,
        torch_dtype=dtype,
    )
    model.to(device)
    model.eval()

    tokenizer = model.tokenizer
    image_processor = ImagePreprocess(model.vision_tower._image_processor, model.config)
    text_processor = TextPreprocess(tokenizer, args.conv_mode)

    message = Message()
    message.add_message(f"{DEFAULT_IMAGE_TOKEN}\n{args.prompt}")
    encoded = text_processor(message.messages, mode="eval")
    input_ids = encoded["input_ids"].unsqueeze(0).to(device)

    image = Image.open(image_path).convert("RGB")
    image_tensor = image_processor(image).unsqueeze(0).to(device=device, dtype=dtype)

    stop_string = text_processor.template.separator.apply()[1]
    stopping_criteria = KeywordsStoppingCriteria([stop_string], tokenizer, input_ids)

    with torch.inference_mode():
        output_ids = model.generate(
            input_ids,
            images=image_tensor,
            do_sample=False,
            num_beams=1,
            max_new_tokens=args.max_new_tokens,
            use_cache=True,
            pad_token_id=tokenizer.pad_token_id,
            stopping_criteria=[stopping_criteria],
        )

    answer = tokenizer.batch_decode(output_ids, skip_special_tokens=True)[0].strip()
    if answer.endswith(stop_string):
        answer = answer[: -len(stop_string)].strip()

    print("\nAnswer:")
    print(answer)


if __name__ == "__main__":
    main()
