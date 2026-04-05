#!/usr/bin/env python3
"""Verify Vast.ai RTX 5090 setup and recommend optimal settings"""

import torch
import sys

print("=" * 80)
print("VAST.AI GPU VERIFICATION FOR FINGEO-SLM")
print("=" * 80)

# Check CUDA
print(f"\n1. CUDA Availability")
print(f"   CUDA Available: {torch.cuda.is_available()}")
if not torch.cuda.is_available():
    print("   ❌ CUDA not found! Check drivers with: nvidia-smi")
    sys.exit(1)

print(f"   ✓ CUDA Version: {torch.version.cuda}")
print(f"   ✓ PyTorch Version: {torch.__version__}")

# Check GPU
print(f"\n2. GPU Information")
device_name = torch.cuda.get_device_name(0)
vram_total = torch.cuda.get_device_properties(0).total_memory / 1e9
print(f"   Device: {device_name}")
print(f"   Total VRAM: {vram_total:.1f} GB")

# Verify specific GPU
if "5090" in device_name:
    print("   ✅ Confirmed: RTX 5090 (Excellent choice!)")
    tier = "premium"
elif "4090" in device_name:
    print("   ✓ RTX 4090 (Great performance!)")
    tier = "high"
elif "3090" in device_name:
    print("   ✓ RTX 3090 (Good performance!)")
    tier = "standard"
elif "A100" in device_name:
    print("   ✓ A100 (Datacenter GPU, excellent!)")
    tier = "datacenter"
else:
    print(f"   ℹ GPU: {device_name}")
    tier = "unknown"

# Check available memory
if torch.cuda.is_available():
    torch.cuda.empty_cache()
    vram_free = (torch.cuda.get_device_properties(0).total_memory - 
                 torch.cuda.memory_allocated(0)) / 1e9
    print(f"   Free VRAM: {vram_free:.1f} GB")

# Check precision support
print(f"\n3. Precision Support")
print(f"   FP16: ✓ (Always supported)")
print(f"   BFloat16: {'✓' if torch.cuda.is_bf16_supported() else '✗'}")
if torch.cuda.is_bf16_supported():
    print("   Recommendation: Use torch.bfloat16 for better numerical stability")
    recommended_dtype = "torch.bfloat16"
else:
    print("   Recommendation: Use torch.float16")
    recommended_dtype = "torch.float16"

# Compute Capability
compute_capability = torch.cuda.get_device_capability(0)
print(f"   Compute Capability: {compute_capability[0]}.{compute_capability[1]}")

# Recommended settings based on VRAM
print(f"\n4. Recommended Training Settings for {vram_total:.0f}GB VRAM")
print("-" * 80)

if vram_total >= 30:  # RTX 5090
    batch_size = 8
    grad_accum = 4
    speed_class = "⚡ Ultra Fast"
    time_estimate = "14-18 min"
    cost_estimate = "$0.42-0.54"
elif vram_total >= 22:  # RTX 4090/3090
    batch_size = 4
    grad_accum = 4
    speed_class = "🚀 Fast"
    time_estimate = "20-25 min"
    cost_estimate = "$0.33-0.42"
else:  # Lower-tier
    batch_size = 2
    grad_accum = 4
    speed_class = "📊 Standard"
    time_estimate = "30-40 min"
    cost_estimate = "$0.25-0.33"

effective_batch = batch_size * grad_accum

print(f"   Speed Class: {speed_class}")
print(f"   Batch Size: {batch_size}")
print(f"   Gradient Accumulation: {grad_accum}")
print(f"   Effective Batch Size: {effective_batch}")
print(f"   Data Type: {recommended_dtype}")
print(f"   Estimated Training Time: {time_estimate}")
print(f"   Estimated Cost: {cost_estimate} @ $1.80/hr")

# Code snippet
print(f"\n5. Configuration Code for Your Notebook")
print("-" * 80)
print(f"```python")
print(f"# Add to 02_model_optimization_and_training.ipynb")
print(f"training_args = TrainingArguments(")
print(f"    per_device_train_batch_size={batch_size},")
print(f"    gradient_accumulation_steps={grad_accum},")
print(f"    num_train_epochs=3,")
print(f"    learning_rate=2e-4,")
print(f"    # ... other args")
print(f")")
print(f"")
print(f"# For model loading:")
print(f"model = AutoModelForCausalLM.from_pretrained(")
print(f"    model_id,")
print(f"    torch_dtype={recommended_dtype},")
print(f"    device_map='auto',")
print(f")")
print(f"```")

# Memory estimation
print(f"\n6. Memory Usage Estimation")
print("-" * 80)
model_size = 7.6  # Phi-3-mini in FP16
optimizer_size = model_size * 2  # Adam optimizer states
gradient_size = model_size
activation_size = batch_size * 0.5  # Rough estimate

total_estimated = model_size + optimizer_size + gradient_size + activation_size
headroom = vram_total - total_estimated

print(f"   Model (FP16): ~{model_size:.1f} GB")
print(f"   Optimizer States: ~{optimizer_size:.1f} GB")
print(f"   Gradients: ~{gradient_size:.1f} GB")
print(f"   Activations (batch={batch_size}): ~{activation_size:.1f} GB")
print(f"   Total Estimated: ~{total_estimated:.1f} GB")
print(f"   Available VRAM: {vram_total:.1f} GB")
print(f"   Headroom: ~{headroom:.1f} GB")

if headroom > 5:
    print(f"   ✅ Plenty of headroom! Config is safe.")
elif headroom > 2:
    print(f"   ✓ Good headroom. Should work well.")
elif headroom > 0:
    print(f"   ⚠ Tight fit. Monitor for OOM errors.")
else:
    print(f"   ❌ May run out of memory! Reduce batch size.")

# Final checks
print(f"\n7. Pre-Training Checklist")
print("-" * 80)
checks = [
    ("CUDA available", torch.cuda.is_available()),
    ("GPU detected", torch.cuda.device_count() > 0),
    ("Sufficient VRAM (>20GB)", vram_total > 20),
    ("Modern CUDA (>11.7)", float(torch.version.cuda) >= 11.7),
]

all_passed = True
for check_name, check_result in checks:
    status = "✓" if check_result else "✗"
    print(f"   [{status}] {check_name}")
    if not check_result:
        all_passed = False

print("\n" + "=" * 80)
if all_passed:
    print("✅ ALL CHECKS PASSED - Ready to train!")
    print("\nNext steps:")
    print("1. Update batch_size to {} in training notebook".format(batch_size))
    print("2. Run: jupyter nbconvert --to script --execute 02_model_optimization_and_training.ipynb")
    print("3. Expected time: {}".format(time_estimate))
    print("4. Expected cost: {}".format(cost_estimate))
else:
    print("⚠ SOME CHECKS FAILED - Review issues above")
    
print("=" * 80)
