"""Hardware-aware local-model selector.

FrugalRoute's whole thesis is "use the FREE local model whenever it's good
enough." That only works if the local model actually runs *fast*, which on
consumer hardware means it must fit ENTIRELY in GPU VRAM — a model that spills
to CPU offload turns a 4s answer into a 20s one (measured on this box).

So we pick, at startup, the highest-capability model whose GPU footprint fits
the detected VRAM budget, preferring models already pulled in Ollama (no
surprise multi-GB downloads). Set LOCAL_MODEL=auto in .env to use this.

    python hwselect.py        # prints the decision for the current machine
"""
import json
import os
import shutil
import subprocess

# Ranked catalog: (ollama tag, approx GPU footprint MB at Ollama's default Q4
# incl. weights + KV/compute at ~4k ctx, capability rank). Ascending capability.
CATALOG = [
    ("qwen3:4b",        2500, 1),
    ("gemma4:e2b",      7200, 1),
    ("gemma4:e4b",      9600, 2),
    ("qwen3:14b",       9300, 2),
    ("gemma4:26b",     17000, 3),
    ("qwen3:8b",        5200, 3),
    ("qwen3:30b-a3b",  18000, 3),
    ("qwen3:32b",      20000, 3),
    ("gemma4:31b",     19000, 4),
    ("gemma4:12b",      7600, 5),
]

# VRAM held back for the display, CUDA context, KV-cache growth and compute
# buffers — weights alone must not eat the whole card.
GPU_RESERVE_MB = int(os.getenv("GPU_RESERVE_MB", "1100"))
# If the ideal fit-model isn't installed, pull it automatically? Off by default.
AUTO_PULL = str(os.getenv("AUTO_PULL", "0")).lower() in ("1", "true", "yes", "on")

_CACHE = {}


def _run(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=15).stdout
    except Exception:
        return ""


def total_vram_mb():
    """Total GPU VRAM in MB (0 if no usable GPU). Prefers nvidia-smi."""
    if shutil.which("nvidia-smi"):
        out = _run(["nvidia-smi", "--query-gpu=memory.total",
                    "--format=csv,noheader,nounits"])
        vals = [int(x) for x in out.replace(",", "").split() if x.strip().isdigit()]
        if vals:
            return max(vals)
    # AMD ROCm
    if shutil.which("rocm-smi"):
        out = _run(["rocm-smi", "--showmeminfo", "vram", "--json"])
        try:
            d = json.loads(out)
            for v in d.values():
                for k, val in v.items():
                    if "total" in k.lower():
                        return int(int(val) / (1024 * 1024))
        except Exception:
            pass
    return 0


def ram_gb():
    try:
        if os.name == "nt":
            import ctypes

            class _MS(ctypes.Structure):
                _fields_ = [("dwLength", ctypes.c_ulong),
                            ("dwMemoryLoad", ctypes.c_ulong),
                            ("ullTotalPhys", ctypes.c_ulonglong),
                            ("ullAvailPhys", ctypes.c_ulonglong),
                            ("ullTotalPageFile", ctypes.c_ulonglong),
                            ("ullAvailPageFile", ctypes.c_ulonglong),
                            ("ullTotalVirtual", ctypes.c_ulonglong),
                            ("ullAvailVirtual", ctypes.c_ulonglong),
                            ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
            ms = _MS()
            ms.dwLength = ctypes.sizeof(_MS)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(ms))
            return round(ms.ullTotalPhys / (1024 ** 3), 1)
        with open("/proc/meminfo") as f:
            for line in f:
                if line.startswith("MemTotal"):
                    return round(int(line.split()[1]) / (1024 * 1024), 1)
    except Exception:
        pass
    return 0.0


def installed_models():
    """Set of ollama model tags already pulled."""
    out = _run(["ollama", "list"])
    tags = set()
    for line in out.splitlines()[1:]:
        line = line.strip()
        if line:
            tags.add(line.split()[0])
    return tags


def choose(verbose=False):
    """Return the ollama tag of the best local model for THIS machine."""
    if _CACHE.get("model") and not verbose:
        return _CACHE["model"]

    vram = total_vram_mb()
    ram = ram_gb()
    installed = installed_models()
    budget = max(0, vram - GPU_RESERVE_MB)

    fits = [(tag, mb, rank) for (tag, mb, rank) in CATALOG if mb <= budget]
    ideal = max(fits, key=lambda x: x[2])[0] if fits else None
    installed_fits = [t for (t, mb, r) in sorted(fits, key=lambda x: -x[2]) if t in installed]

    reason = ""
    if budget <= 0:
        # No usable GPU — smallest installed model on CPU, else the smallest catalog entry.
        chosen = next((t for (t, mb, r) in CATALOG if t in installed), CATALOG[0][0])
        reason = "no GPU detected -> smallest safe model (CPU)"
    elif installed_fits:
        chosen = installed_fits[0]
        reason = f"largest installed model fitting {budget}MB GPU budget"
    elif ideal and AUTO_PULL:
        _run(["ollama", "pull", ideal])
        chosen = ideal
        reason = f"pulled ideal fit-model for {budget}MB budget (AUTO_PULL=1)"
    else:
        # Nothing that fits is installed: fall back to the smallest installed model.
        chosen = next((t for (t, mb, r) in CATALOG if t in installed),
                      ideal or "qwen3:4b")
        if ideal and ideal not in installed:
            reason = (f"ideal fit is {ideal} (not installed; run "
                      f"`ollama pull {ideal}` or set AUTO_PULL=1). Using {chosen}.")
        else:
            reason = "fallback to smallest installed model"

    info = {"gpu_vram_mb": vram, "ram_gb": ram, "gpu_budget_mb": budget,
            "installed": sorted(installed), "ideal_fit": ideal,
            "chosen": chosen, "reason": reason}
    _CACHE.update(model=chosen, info=info)

    if verbose:
        print("FrugalRoute — hardware-aware local model selection")
        print(f"  GPU VRAM total : {vram} MB")
        print(f"  GPU budget     : {budget} MB  (reserve {GPU_RESERVE_MB} MB)")
        print(f"  System RAM     : {ram} GB")
        print(f"  Installed      : {', '.join(sorted(installed)) or '(none)'}")
        print(f"  Ideal that fits: {ideal}")
        print(f"  --> CHOSEN     : {chosen}")
        print(f"  reason         : {reason}")
    return chosen


if __name__ == "__main__":
    choose(verbose=True)
