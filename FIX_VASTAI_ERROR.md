# 🚨 URGENT: Fix TypeError on Vast.ai

## The Error You're Seeing

```
TypeError: SFTConfig.__init__() got an unexpected keyword argument 'max_seq_length'
```

## Quick Fix (Do This Now!)

### On Your Vast.ai Jupyter Notebook:

**Find Cell 16** (the one that starts with `def build_sft_config`), scroll down to around line 78-104 where it says:

```python
config = SFTConfig(
    output_dir=output_dir,
    ...
    max_seq_length=max_seq_length,  # ← LINE 97 - This causes the error
    ...
)
```

**Replace the entire `config = SFTConfig(...)` block with this:**

```python
# Base config - compatible with all TRL versions
config_params = {
    "output_dir": output_dir,
    "per_device_train_batch_size": batch_size,
    "per_device_eval_batch_size": 1,
    "gradient_accumulation_steps": grad_accum,
    "gradient_checkpointing": True,
    "gradient_checkpointing_kwargs": {"use_reentrant": False},
    "optim": choose_optimizer(backend, qlora_enabled),
    "learning_rate": 2e-4,
    "logging_steps": 10,
    "num_train_epochs": 3,
    "bf16": bf16,
    "fp16": fp16,
    "report_to": report_to,
    "logging_dir": log_dir,
    "save_strategy": "epoch",
    "save_total_limit": 1,
    "eval_strategy": "no",
    "max_grad_norm": 1.0,
    "warmup_steps": 10,
    "weight_decay": 0.01,
}

# Try version-compatible config
try:
    config = SFTConfig(**config_params, max_seq_length=max_seq_length, dataset_text_field="formatted_prompt", packing=False)
except TypeError:
    config = SFTConfig(**config_params, dataset_text_field="formatted_prompt", packing=False)
```

**Then:**
1. Click inside that cell
2. Run it (Shift+Enter)
3. Continue running cells from where you got the error

## Why This Happened

- Your Vast.ai instance has an older/newer version of TRL library
- The `max_seq_length` parameter doesn't exist in some TRL versions
- The fix auto-detects and uses the right format

## Alternative: Upload Fixed Notebook

```bash
# On your Mac:
scp /Users/uzmanarfan/Documents/FinGEO-SLM/02_model_optimization_and_training.ipynb \
    root@<your-vast-ip>:/workspace/FinGEO-SLM/

# Then on Vast.ai Jupyter:
# 1. Refresh the file list
# 2. Close and reopen the notebook
# 3. Kernel → Restart & Run All
```

## ✅ You'll Know It's Fixed When...

You see this output:
```
Training configuration:
  Per-device batch size: 4
  Gradient accumulation: 4
  Effective batch size: 16
  Precision: BF16
```

**No more TypeError!** ✓

Continue training - everything else should work fine! 🚀
