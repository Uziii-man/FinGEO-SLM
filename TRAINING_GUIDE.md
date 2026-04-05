# Training Guide - How to Train Your FinGEO-SLM Model

## ✅ Notebook Fixed & Ready

I've fixed the model saving logic in `02_model_optimization_and_training.ipynb`. The notebook is now ready for GPU training.

## Prerequisites

### Required Hardware
- **GPU**: NVIDIA GPU with 8GB+ VRAM (16GB recommended)
  - RTX 3060 (12GB) - Minimum
  - RTX 3090 (24GB) - Recommended
  - RTX 4090 (24GB) - Ideal
  - A100 (40GB/80GB) - Professional

### Why GPU is Required
- **CPU training**: ~5-7 days for 5000 samples
- **GPU training**: ~2-4 hours for 5000 samples
- The notebook uses QLoRA (4-bit quantization) which requires GPU

## Option 1: Use Vast.ai (Recommended - Cheap GPU Rental)

### Step 1: Sign up for Vast.ai
```bash
# Visit: https://vast.ai
# Create account and add $10-20 credit
```

### Step 2: Rent a GPU Instance
1. Go to "Search" → Find instances with:
   - GPU: RTX 3090 or RTX 4090
   - VRAM: 16GB+
   - Disk: 50GB+
   - Price: ~$0.20-0.50/hour

2. Select PyTorch template or Ubuntu with CUDA

3. Start instance and get SSH credentials

### Step 3: Upload Your Project
```bash
# From your local machine
scp -r /Users/uzmanarfan/Documents/FinGEO-SLM root@<vast-ip>:/workspace/
```

Or use their web file manager.

### Step 4: Run Training
```bash
# SSH into Vast.ai instance
ssh root@<vast-ip> -p <port>

# Navigate to project
cd /workspace/FinGEO-SLM

# Install dependencies
pip install -r requirements.txt

# Run training notebook
jupyter nbconvert --to notebook --execute 02_model_optimization_and_training.ipynb --output 02_executed.ipynb

# Or open Jupyter and run manually:
jupyter notebook --allow-root --no-browser --port=8888
```

### Step 5: Download Trained Model
```bash
# After training completes
scp -r root@<vast-ip>:/workspace/FinGEO-SLM/fingeo_slm_outputs ./
```

**Cost estimate**: ~$1-2 for full training run

## Option 2: Google Colab (Free GPU, Limited Time)

### Step 1: Upload to Google Drive
1. Upload entire `FinGEO-SLM` folder to Google Drive
2. Keep it in: `MyDrive/FinGEO-SLM/`

### Step 2: Open in Colab
```python
# In Colab, mount drive
from google.colab import drive
drive.mount('/content/drive')

# Change to project directory
import os
os.chdir('/content/drive/MyDrive/FinGEO-SLM')

# Verify location
!pwd
!ls -la
```

### Step 3: Enable GPU
1. Runtime → Change runtime type
2. Hardware accelerator: **GPU** (T4)
3. Save

### Step 4: Run Notebook
- Open `02_model_optimization_and_training.ipynb` in Colab
- Run all cells
- Model saves to Google Drive automatically

**Limitations**:
- ⚠️ 12-hour session limit (training should complete in 2-4 hours)
- ⚠️ May disconnect if idle
- ✅ Free!

## Option 3: Local GPU (If You Have One)

### Check GPU
```bash
# Check if CUDA is available
python3 check_gpu.py

# Or check directly
nvidia-smi
```

### Install CUDA (if needed)
```bash
# macOS - Not supported (M1/M2 uses MPS, not fully compatible)
# Windows/Linux - Install CUDA Toolkit 11.8+
# https://developer.nvidia.com/cuda-downloads
```

### Run Training
```bash
cd /Users/uzmanarfan/Documents/FinGEO-SLM

# Install dependencies
pip install -r requirements.txt

# Run notebook
jupyter notebook
# Open 02_model_optimization_and_training.ipynb
# Run all cells
```

## What the Training Does

### 1. Data Loading
- Loads financial Q&A pairs from `processed_data/`
- Formats them with Chain-of-Thought prompts
- Splits into train/eval (90/10)

### 2. Model Setup
- Loads Phi-3-mini (3.8B parameters)
- Applies 4-bit quantization (reduces to ~2GB VRAM)
- Adds LoRA adapters (only trains ~1% of parameters)

### 3. Training
- Trains for 3 epochs (default)
- ~5000 samples
- Takes 2-4 hours on RTX 3090
- Saves checkpoints every 500 steps

### 4. Model Saving (FIXED!)
The notebook now saves:

**a) Adapter only** (`fingeo_slm_outputs/fingeo-slm-adapter/`)
- Just the LoRA weights (~50MB)
- Fast to save/load
- Need base model to use

**b) Merged model** (`fingeo_slm_outputs/finetuned_model/`)
- LoRA merged with base model
- Ready to use in notebook 4
- ~7GB total size
- This is what notebook 4 looks for!

## After Training Completes

### Verify Model Saved
```bash
ls -lh fingeo_slm_outputs/finetuned_model/
# Should see:
# - config.json
# - model.safetensors (or pytorch_model.bin)
# - tokenizer.json
# - tokenizer_config.json
```

### Test in Notebook 4
```python
# In 04_geo_search_query.ipynb
MODEL_PATH = "./fingeo_slm_outputs/finetuned_model"
ENABLE_MODEL_GENERATION = True

# Run the model status checker cell
# Should show: ✅ Model is properly saved
```

## Troubleshooting

### "CUDA out of memory"
```python
# In notebook 2, reduce batch size:
# Find RuntimeConfig and change:
# per_device_train_batch_size = 1  # Instead of 2
# gradient_accumulation_steps = 8  # Instead of 4
```

### "Training too slow"
```python
# Reduce dataset size:
max_train_samples: int = 1000  # Instead of 5000
```

### "Model not saving"
- Check disk space: `df -h`
- Verify the fix worked - look for "SAVING MODEL" output
- Check permissions: `ls -la fingeo_slm_outputs/`

### "Session disconnected on Colab"
- Training state is lost if disconnected
- Use checkpoint recovery:
```python
# In notebook 2, add to TrainingArguments:
resume_from_checkpoint=True
```

## Expected Timeline

| Stage | Time |
|-------|------|
| Setup & data loading | 5 min |
| Model initialization | 2 min |
| Training (5000 samples) | 2-4 hours |
| Model saving | 5 min |
| **Total** | **2.5-4.5 hours** |

## Cost Estimates

| Option | Cost | Time |
|--------|------|------|
| Vast.ai RTX 3090 | $1-2 | 3 hours |
| Vast.ai RTX 4090 | $2-3 | 2 hours |
| Google Colab (free) | $0 | 3-4 hours |
| Google Colab Pro | $10/month | 2 hours |

## Next Steps

1. **Choose your GPU platform** (Vast.ai recommended for cost)
2. **Upload project** to the platform
3. **Run notebook 2** - all cells in order
4. **Wait for completion** - go get coffee ☕
5. **Download model** if on cloud platform
6. **Test in notebook 4** - should load automatically!

## Need Help?

- Check `CHECK_MODEL_STATUS.md` for verification
- Run the model status checker in notebook 4
- Check training logs in `fingeo_slm_logs/`

Good luck with your training! 🚀
