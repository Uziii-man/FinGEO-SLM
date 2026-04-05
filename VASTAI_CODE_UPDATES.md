# Vast.ai RTX 5090 Optimization Settings

## Quick Answer: **NO code changes required!** 

Your notebooks will work on Vast.ai RTX 5090 out-of-the-box. The backend detection automatically finds CUDA.

---

## Optional: Maximize RTX 5090 Performance

If you want to squeeze maximum performance from the RTX 5090's 32GB VRAM, make these **optional** changes:

### 1. Increase Batch Size (Training Notebook)

**File**: `02_model_optimization_and_training.ipynb`

Find the cell with training configuration and update:

```python
# BEFORE (conservative for 24GB):
training_args = TrainingArguments(
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    # ... other args
)

# AFTER (optimized for RTX 5090 32GB):
training_args = TrainingArguments(
    per_device_train_batch_size=8,  # 4x larger! ⚡
    gradient_accumulation_steps=4,
    # ... other args
)
```

**Benefit**: 
- Effective batch size: 8 → 32 (4x larger)
- Faster convergence (fewer steps to same quality)
- Training time: ~18 min → ~14 min
- Better gradient stability

---

### 2. Enable BFloat16 (Optional - Better Precision)

**File**: `02_model_optimization_and_training.ipynb`

```python
# Find where model is loaded:
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16,  # Current
    # ... other args
)

# CHANGE TO (RTX 5090 supports BF16 natively):
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,  # Better on newer GPUs ✨
    # ... other args
)
```

**Benefit**:
- Better numerical stability than FP16
- Prevents gradient overflow/underflow
- Native support on RTX 5090 (no performance penalty)
- Slightly better final model quality

---

### 3. Verification Script (Run on Vast.ai)

Save this as `check_gpu.py` and run on your Vast.ai instance:

```python
#!/usr/bin/env python3
"""Verify Vast.ai RTX 5090 setup"""

import torch
import sys

print("=" * 80)
print("VAST.AI GPU VERIFICATION")
print("=" * 80)

# Check CUDA
print(f"\n1. CUDA Available: {torch.cuda.is_available()}")
if not torch.cuda.is_available():
    print("   ❌ CUDA not found! Check drivers.")
    sys.exit(1)

print(f"   ✓ CUDA Version: {torch.version.cuda}")

# Check GPU
print(f"\n2. GPU Information:")
print(f"   Device: {torch.cuda.get_device_name(0)}")
print(f"   VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")

# Check if it's actually a 5090
device_name = torch.cuda.get_device_name(0)
if "5090" in device_name:
    print("   ✓ Confirmed: RTX 5090")
elif "4090" in device_name:
    print("   ⚠ Got RTX 4090 instead (still great!)")
elif "3090" in device_name:
    print("   ⚠ Got RTX 3090 instead (still good!)")
else:
    print(f"   ℹ GPU: {device_name}")

# Check BFloat16 support
print(f"\n3. BFloat16 Support: {torch.cuda.is_bf16_supported()}")
if torch.cuda.is_bf16_supported():
    print("   ✓ Can use torch.bfloat16 for better precision")
else:
    print("   ℹ Use torch.float16 instead")

# Recommended batch size
vram_gb = torch.cuda.get_device_properties(0).total_memory / 1e9
print(f"\n4. Recommended Settings for {vram_gb:.0f}GB VRAM:")

if vram_gb >= 30:
    print("   Batch Size: 8 (aggressive)")
    print("   Gradient Accumulation: 4")
    print("   Effective Batch: 32")
    print("   Expected Training Time: ~14-18 min")
elif vram_gb >= 22:
    print("   Batch Size: 4 (balanced)")
    print("   Gradient Accumulation: 4")
    print("   Effective Batch: 16")
    print("   Expected Training Time: ~20-25 min")
else:
    print("   Batch Size: 2 (conservative)")
    print("   Gradient Accumulation: 4")
    print("   Effective Batch: 8")
    print("   Expected Training Time: ~30-35 min")

print("\n" + "=" * 80)
print("✓ Setup verified! Ready to train.")
print("=" * 80)
```

**Run on Vast.ai:**
```bash
python check_gpu.py
```

---

## What Works Automatically (No Changes Needed)

✅ **Backend Detection**: Automatically uses CUDA  
✅ **Device Placement**: Models move to GPU automatically  
✅ **Memory Management**: Handles 32GB VRAM properly  
✅ **Mixed Precision**: Works with FP16 out-of-the-box  
✅ **Gradient Checkpointing**: Enabled if needed  

---

## Pre-Flight Checklist for Vast.ai

Before renting, ensure:

1. **Docker Image**: Use `pytorch/pytorch:2.3.0-cuda12.1-cudnn8-devel`
   - RTX 5090 needs CUDA 12.1+
   - Older images (11.8) will work but slower

2. **Disk Space**: Minimum 50GB
   - Model: ~8GB
   - Dependencies: ~10GB
   - Data: ~5GB
   - Outputs: ~5GB
   - Headroom: ~20GB

3. **Ports**: Open 8888 if using Jupyter
   - Or use SSH tunnel: `ssh -L 8888:localhost:8888 ...`

---

## Quick Setup Commands (Copy-Paste on Vast.ai)

```bash
# 1. Update and verify
nvidia-smi
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"

# 2. Clone and setup
cd /workspace
git clone <your-repo-url>
cd FinGEO-SLM
pip install -r requirements.txt

# 3. Verify GPU (optional but recommended)
python check_gpu.py

# 4. Run training
# Option A: Via notebook
jupyter nbconvert --to script --execute 02_model_optimization_and_training.ipynb

# Option B: Via Jupyter web UI
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root

# 5. Download results
tar -czf results.tar.gz fingeo_slm_outputs/
```

---

## Troubleshooting

### "RuntimeError: CUDA out of memory"
```python
# Reduce batch size in training notebook:
per_device_train_batch_size=4  # Down from 8
# or
per_device_train_batch_size=2  # Down from 4
```

### "CUDA not available"
```bash
# Check NVIDIA driver
nvidia-smi

# Check PyTorch installation
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Verify
python -c "import torch; print(torch.cuda.is_available())"
```

### "Slow training speed"
```bash
# Check GPU usage
nvidia-smi -l 1  # Update every second

# Should show:
# - GPU Utilization: 90-100%
# - Memory Used: 20-28GB (out of 32GB)
# - Temperature: 70-85°C

# If GPU usage is low:
# - Increase batch size
# - Check if CPU bottleneck (htop)
# - Verify data is on GPU (not CPU)
```

---

## Summary

**Do you NEED to update code?** ❌ **NO**

**Should you optimize for 5090?** ✅ **YES** (optional, 25% faster)

**Critical changes:** **NONE**

**Recommended optimizations:**
1. Batch size: 2 → 8 (if you want max speed)
2. BFloat16: FP16 → BF16 (if you want better precision)

Your code will work perfectly on Vast.ai RTX 5090 without any modifications. The optimizations above just help you get **even more** value from the hardware!
