# Model Status Check Guide

## Quick Check

Run this command in your terminal to check if your model is saved:

```bash
# Check if model exists
ls -lh fingeo_slm_outputs/finetuned_model/

# Check for checkpoints
ls -lh fingeo_slm_outputs/checkpoint-*/
```

## What to Look For

A properly saved model should have:
- ✅ `config.json` - Model configuration
- ✅ `model.safetensors` OR `pytorch_model.bin` - Model weights
- ✅ `tokenizer.json` and `tokenizer_config.json` - Tokenizer files
- ✅ Total size: 2-8 GB (depending on model)

## Current Status

Your `fingeo_slm_outputs/` directory is currently **EMPTY**. This means:
- ❌ No trained model exists yet
- ❌ Notebook 2 hasn't completed training, or
- ❌ The model was saved to a different location

## Solution Steps

### Option 1: Train the Model (Recommended)

1. Open `02_model_optimization_and_training.ipynb`
2. Configure your settings:
   ```python
   # In notebook 2
   OUTPUT_DIR = "./fingeo_slm_outputs"
   SAVE_MODEL = True  # Make sure this is True!
   ```
3. Run all cells to train the model
4. At the end, verify it saved:
   ```python
   # Should see output like:
   # ✓ Model saved to ./fingeo_slm_outputs/finetuned_model
   ```

### Option 2: Use a Pre-trained Model

If you don't have GPU/time to train, you can use a base model directly:

```python
# In notebook 4 configuration cell:
MODEL_PATH = None  # This will use the HuggingFace preset
FINETUNED_MODEL_PRESET = "microsoft/Phi-3-mini-4k-instruct"
ENABLE_MODEL_GENERATION = True
```

### Option 3: Check Alternative Locations

The model might be saved elsewhere. Check:

```bash
# Colab location
ls -lh /content/drive/MyDrive/FinGEO-SLM/fingeo_slm_outputs/

# Vast.ai location
ls -lh /workspace/FinGEO-SLM/fingeo_slm_outputs/

# Check all checkpoints
find . -name "checkpoint-*" -type d
```

## Common Issues & Fixes

### Issue 1: Training Interrupted
**Symptom**: Checkpoints exist but no final model
```bash
# Check for checkpoints
ls fingeo_slm_outputs/checkpoint-*/
```

**Fix**: Use the last checkpoint as your model
```python
MODEL_PATH = "./fingeo_slm_outputs/checkpoint-1000"  # Use last checkpoint number
```

### Issue 2: Out of Memory During Save
**Symptom**: Training completes but no model saved

**Fix**: In notebook 2, add explicit save:
```python
# At the end of training
trainer.save_model("./fingeo_slm_outputs/finetuned_model")
tokenizer.save_pretrained("./fingeo_slm_outputs/finetuned_model")
print("✓ Model manually saved")
```

### Issue 3: Wrong Path
**Symptom**: Model exists but notebook can't find it

**Fix**: Use absolute paths
```python
from pathlib import Path
MODEL_PATH = str(Path.cwd() / "fingeo_slm_outputs" / "finetuned_model")
print(f"Looking for model at: {MODEL_PATH}")
```

## Verification Script

Run this in a notebook cell to diagnose:

```python
from pathlib import Path
import os

def diagnose_model_location():
    print("=" * 60)
    print("MODEL LOCATION DIAGNOSIS")
    print("=" * 60)
    
    # Check current working directory
    cwd = Path.cwd()
    print(f"\nCurrent directory: {cwd}")
    
    # Check output directory
    output_dir = cwd / "fingeo_slm_outputs"
    print(f"\nOutput directory exists: {output_dir.exists()}")
    
    if output_dir.exists():
        # List contents
        contents = list(output_dir.glob("*"))
        print(f"Contents ({len(contents)} items):")
        for item in contents:
            if item.is_dir():
                size = sum(f.stat().st_size for f in item.rglob("*") if f.is_file())
                print(f"  📁 {item.name} ({size / 1e9:.2f} GB)")
            else:
                print(f"  📄 {item.name}")
    
    # Check for models anywhere
    print("\nSearching for model files...")
    model_dirs = list(cwd.rglob("config.json"))
    if model_dirs:
        print(f"Found {len(model_dirs)} potential model locations:")
        for cfg in model_dirs[:5]:
            print(f"  - {cfg.parent}")
    else:
        print("  ❌ No model files found")
    
    print("\n" + "=" * 60)

diagnose_model_location()
```

## Next Steps

1. **Run the diagnosis** using the script above
2. **Check notebook 2** - Make sure it ran to completion
3. **Use the status checker** - Added in notebook 4 after configuration cell
4. **Test with base model first** - Set `MODEL_PATH = None` to use HuggingFace

## Need Help?

If model still won't load:
1. Check the training logs in `fingeo_slm_logs/`
2. Verify disk space: `df -h`
3. Check permissions: `ls -la fingeo_slm_outputs/`
