#!/bin/sh
cd /frugalroute
echo "=== SMOKE TEST ==="
python3 smoke_test.py
echo "=== ROCM-SMI ==="
rocm-smi 2>/dev/null
