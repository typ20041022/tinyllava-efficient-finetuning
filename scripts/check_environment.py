#!/usr/bin/env python3
"""Print a small, shareable report about the current Python environment."""

from __future__ import annotations

import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


def _torch_info() -> dict[str, Any]:
    """Return PyTorch and accelerator information when PyTorch is installed."""
    try:
        import torch
    except ImportError:
        return {"installed": False}

    mps_backend = getattr(torch.backends, "mps", None)
    mps_available = bool(mps_backend and mps_backend.is_available())
    cuda_available = torch.cuda.is_available()

    info: dict[str, Any] = {
        "installed": True,
        "version": torch.__version__,
        "cuda_available": cuda_available,
        "mps_available": mps_available,
    }
    if cuda_available:
        info["cuda_version"] = torch.version.cuda
        info["gpu_count"] = torch.cuda.device_count()
        info["gpus"] = [
            {
                "index": index,
                "name": torch.cuda.get_device_name(index),
                "memory_gib": round(
                    torch.cuda.get_device_properties(index).total_memory / 1024**3,
                    2,
                ),
            }
            for index in range(torch.cuda.device_count())
        ]
    return info


def _nvidia_smi_available() -> bool:
    """Return whether the NVIDIA system-management command is available."""
    command = shutil.which("nvidia-smi")
    if command is None:
        return False

    result = subprocess.run(
        [command, "--query-gpu=name", "--format=csv,noheader"],
        capture_output=True,
        check=False,
        text=True,
        timeout=10,
    )
    return result.returncode == 0


def build_report() -> dict[str, Any]:
    """Build an environment report without usernames, tokens, or hostnames."""
    repository = Path(__file__).resolve().parents[1]
    disk_usage = shutil.disk_usage(repository)

    return {
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
        "python": {
            "version": platform.python_version(),
            "executable": sys.executable,
        },
        "storage": {
            "repository_filesystem_free_gib": round(disk_usage.free / 1024**3, 2),
        },
        "nvidia_smi_available": _nvidia_smi_available(),
        "torch": _torch_info(),
    }


def main() -> None:
    """Print the report as formatted JSON."""
    print(json.dumps(build_report(), indent=2))


if __name__ == "__main__":
    main()
