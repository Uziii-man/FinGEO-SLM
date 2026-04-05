# Vast.ai Setup Guide - Optimized for RTX 5090

This guide helps you run FinGEO-SLM on vast.ai cloud GPU instances with optimal cost/performance.

---

## 🚀 Quick Start (For Experienced Users)

```bash
# 1. Rent RTX 5090 on vast.ai (filter: CUDA 12.1+, 50GB+ disk)
# 2. SSH into instance
ssh root@<ip> -p <port>

# 3. Setup
cd /workspace
git clone <your-repo-url> && cd FinGEO-SLM
pip install -r requirements.txt

# 4. Train (in tmux to prevent disconnection)
tmux new -s train
jupyter nbconvert --to script --execute 02_model_optimization_and_training.ipynb
# Ctrl+B, D to detach

# 5. Download results
tar -czf results.tar.gz fingeo_slm_outputs/
# scp from local: scp -P <port> root@<ip>:/workspace/FinGEO-SLM/results.tar.gz .

# 6. STOP INSTANCE (don't forget!)
```

**Time**: ~20 min | **Cost**: ~$0.60 | **Improvement**: 60-75% over baseline

---

## Prerequisites

- Vast.ai account with credits (~$10-20 recommended for testing)
- SSH client (terminal or PuTTY)
- Basic Linux command knowledge

## Step 1: Rent a GPU Instance

### 🏆 Recommended GPUs (Performance vs Cost)

| GPU | VRAM | Speed | Cost/hr | Best For |
|-----|------|-------|---------|----------|
| **RTX 5090** ⭐ | 32GB | Fastest | $1.50-2.50 | Production training, large batches |
| **RTX 4090** | 24GB | Very Fast | $0.80-1.50 | General use, cost-effective |
| **RTX 3090** | 24GB | Fast | $0.40-0.80 | Budget option, still great |
| **A100 (40GB)** | 40GB | Excellent | $2.00-3.00 | Multiple models, research |

### 🎯 For FinGEO-SLM (Phi-3-mini):
1. Go to [vast.ai](https://vast.ai/)
2. **Filter Settings**:
   - GPU: RTX 5090, 4090, or 3090 (32GB, 24GB, or 24GB VRAM)
   - DLPerf: > 80 (ensures good performance)
   - CUDA: 12.0+ (for RTX 5090) or 11.8+ (for older GPUs)
   - Disk Space: > 50GB
   - Sort by: "DLPerf/$ " (best value)

3. **Docker Image**:
   - **For RTX 5090**: `pytorch/pytorch:2.3.0-cuda12.1-cudnn8-devel`
   - **For RTX 4090/3090**: `pytorch/pytorch:2.1.0-cuda11.8-cudnn8-devel`
   - **Alternative**: `nvidia/cuda:12.1.0-cudnn8-devel-ubuntu22.04` (then install PyTorch)

4. Click "Rent" and wait for instance to start (30-60 seconds)

### 💰 Cost Estimates (FinGEO-SLM Training)

**RTX 5090** (~$1.80/hr average):
- Full training (3 epochs): ~15-20 min → **$0.45-0.60**
- Testing/debugging: ~5-10 min → **$0.15-0.30**
- **Total project cost**: ~$3-5 (multiple runs)

**RTX 4090** (~$1.00/hr average):
- Full training (3 epochs): ~25-35 min → **$0.42-0.58**
- Testing/debugging: ~10-15 min → **$0.17-0.25**
- **Total project cost**: ~$3-5 (multiple runs)

**RTX 3090** (~$0.50/hr average):
- Full training (3 epochs): ~35-50 min → **$0.29-0.42**
- Testing/debugging: ~15-20 min → **$0.13-0.17**
- **Total project cost**: ~$2-4 (multiple runs)

> 💡 **Pro Tip**: Use interruptible instances for 30-50% discount if you can handle interruptions

## Step 2: Connect to Your Instance

```bash
# Use the SSH command provided by vast.ai
ssh root@<instance-ip> -p <port>
```

## Step 3: Setup Environment

```bash
# Update system packages
apt-get update && apt-get install -y git vim wget

# Verify CUDA is available
nvidia-smi

# Navigate to workspace
cd /workspace

# Clone repository
git clone <your-repo-url>
cd FinGEO-SLM
```

## Step 4: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Verify PyTorch CUDA
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
```

## Step 5: Run Notebooks

### Option A: Using Jupyter (Recommended)

```bash
# Install Jupyter if not present
pip install jupyter notebook

# Start Jupyter with public access
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root

# Copy the token from the output, then access via:
# http://<vast-instance-ip>:8888/?token=<your-token>
```

**Note**: You may need to open port 8888 in vast.ai instance settings.

### Option B: Convert Notebooks to Python Scripts

```bash
# Install nbconvert
pip install nbconvert

# Convert notebooks to Python
jupyter nbconvert --to script 01_data_collection_and_preprocessing.ipynb
jupyter nbconvert --to script 02_model_optimization_and_training.ipynb
jupyter nbconvert --to script 03_evaluation_and_benchmarking.ipynb

# Run the scripts
python 01_data_collection_and_preprocessing.py
python 02_model_optimization_and_training.py
python 03_evaluation_and_benchmarking.py
```

### Option C: Use VS Code Remote SSH

1. Install VS Code with "Remote - SSH" extension
2. Connect to vast.ai instance via SSH
3. Open notebooks directly in VS Code

## Step 6: Run Notebooks in Order

1. `01_data_collection_and_preprocessing.ipynb` - Prepare datasets (~5 min)
2. `02_model_optimization_and_training.ipynb` - Train model (~30-120 min)
3. `03_evaluation_and_benchmarking.ipynb` - Evaluate performance (~15 min)
4. `04_geo_search_query.ipynb` - Optional RAG demo

## Configuration for Vast.ai

### Set Environment Variable (Optional)

```bash
export FINGEO_PROJECT_ROOT=/workspace/FinGEO-SLM
```

### 🚀 GPU-Optimized Training Configs

#### RTX 5090 (32GB) - Maximum Performance
```python
# In notebook 02:
runtime.model_key = "phi3-mini"
runtime.max_train_samples = None  # Use full dataset
runtime.per_device_train_batch_size = 8  # 4x default!
runtime.gradient_accumulation_steps = 4
runtime.num_train_epochs = 3
runtime.learning_rate = 2e-4

# Expected time: ~15-20 minutes for full training
# Cost: ~$0.45-0.60
```

#### RTX 4090 (24GB) - Great Balance
```python
# In notebook 02:
runtime.model_key = "phi3-mini"
runtime.max_train_samples = None  # Use full dataset
runtime.per_device_train_batch_size = 4  # 2x default
runtime.gradient_accumulation_steps = 4
runtime.num_train_epochs = 3
runtime.learning_rate = 2e-4

# Expected time: ~25-35 minutes
# Cost: ~$0.42-0.58
```

#### RTX 3090 (24GB) - Budget Friendly
```python
# In notebook 02:
runtime.model_key = "phi3-mini"
runtime.max_train_samples = None  # Use full dataset
runtime.per_device_train_batch_size = 2  # Standard
runtime.gradient_accumulation_steps = 4
runtime.num_train_epochs = 3
runtime.learning_rate = 2e-4

# Expected time: ~35-50 minutes
# Cost: ~$0.29-0.42
```

## Important Notes

### Data Persistence
- Save important outputs before stopping instance
- Use `/workspace` directory (persists across restarts)
- Copy trained models to cloud storage:
  ```bash
  # Example: sync to Google Drive or AWS S3
  # Install rclone for cloud sync
  apt-get install rclone
  ```

### Monitor GPU Usage
```bash
# Watch GPU usage in real-time
watch -n 1 nvidia-smi

# Or inside notebook:
import torch
print(f"GPU Memory: {torch.cuda.memory_allocated() / 1e9:.2f}GB")
```

### Cost Optimization

#### 💰 Save Money:
1. **Use interruptible instances**: 30-50% cheaper (for non-critical runs)
2. **Stop instance immediately after training**: Don't pay for idle time
3. **Prepare data locally first**: Upload pre-processed data to skip Step 1
4. **Use tmux/screen**: Prevents losing work on disconnect
5. **Batch multiple experiments**: Train 3-4 variants in one session

#### 📊 Track Costs:
```bash
# Before starting, note your credit balance
# After each run, check: vast.ai dashboard → Billing

# Estimate remaining credits needed:
echo "Remaining runs at $0.50/run: $((CREDITS / 50 * 100)) runs"
```

#### 🎯 Fastest Workflow (Minimize Billable Time):

**Step 1 - Local Prep (FREE):**
```bash
# On your local machine:
# 1. Fix all code issues
# 2. Test notebooks in small scale
# 3. Prepare upload script
```

**Step 2 - Rent & Upload (~2 min, $0.05):**
```bash
# Rent instance → immediately upload code
git clone https://github.com/your-repo/FinGEO-SLM.git
cd FinGEO-SLM
pip install -r requirements.txt  # ~1-2 min
```

**Step 3 - Train in tmux (~20 min, $0.60):**
```bash
# Use tmux so you can disconnect safely
tmux new -s training

# Run training
python 02_model_optimization_and_training.py

# Detach: Ctrl+B, then D
# Reattach later: tmux attach -t training
```

**Step 4 - Download & Stop (~1 min, $0.03):**
```bash
# Download trained model
tar -czf model.tar.gz fingeo_slm_outputs/

# From local machine:
scp -P <port> root@<ip>:/workspace/FinGEO-SLM/model.tar.gz .

# STOP INSTANCE IMMEDIATELY
```

**Total Time**: ~23 minutes | **Total Cost**: ~$0.68

vs.

**Inefficient Workflow** (leaving running, debugging on instance):
**Total Time**: 2-3 hours | **Total Cost**: $3-5 🚫

## Expected Performance

### RTX 5090 (32GB VRAM) ⚡
- **Data preprocessing**: 1-2 minutes
- **Training (full dataset, LoRA)**: 15-20 minutes
- **Evaluation (50 questions)**: 1-2 minutes
- **Total pipeline**: ~20-25 minutes
- **Estimated cost**: $0.60-0.75/run

### RTX 4090 (24GB VRAM) 🎯
- **Data preprocessing**: 2-3 minutes
- **Training (full dataset, LoRA)**: 25-35 minutes
- **Evaluation (50 questions)**: 2-3 minutes
- **Total pipeline**: ~30-40 minutes
- **Estimated cost**: $0.50-0.67/run

### RTX 3090 (24GB VRAM) 💰
- **Data preprocessing**: 3-5 minutes
- **Training (full dataset, LoRA)**: 35-50 minutes
- **Evaluation (50 questions)**: 3-5 minutes
- **Total pipeline**: ~45-60 minutes
- **Estimated cost**: $0.38-0.50/run

### A100 40GB (Alternative) 🏢
- **Data preprocessing**: 1-2 minutes
- **Training (full dataset, LoRA)**: 20-30 minutes
- **Evaluation (50 questions)**: 1-2 minutes
- **Total pipeline**: ~25-35 minutes
- **Estimated cost**: $0.83-1.17/run (more expensive)

## Troubleshooting

### Issue: CUDA Out of Memory
```python
# Reduce batch size in notebook 02:
runtime.per_device_train_batch_size = 2
runtime.gradient_accumulation_steps = 8
```

### Issue: Jupyter Connection Refused
```bash
# Check if port 8888 is exposed in vast.ai settings
# Or use SSH tunnel:
ssh -L 8888:localhost:8888 root@<instance-ip> -p <port>
# Then access http://localhost:8888
```

### Issue: Dependencies Not Found
```bash
# Clear pip cache and reinstall
pip cache purge
pip install -r requirements.txt --force-reinstall
```

### Issue: Notebook Kernel Dies
This usually means OOM (out of memory). Reduce batch size or use a larger GPU instance.

## Next Steps

After setup, proceed to the [main README](README.md) for detailed usage instructions.

## Saving Your Work

Before stopping the instance:

```bash
# Save trained models
tar -czf fingeo-slm-models.tar.gz fingeo-slm-adapter* processed_data/

# Download to local machine (from your local terminal)
scp -P <port> root@<instance-ip>:/workspace/FinGEO-SLM/fingeo-slm-models.tar.gz .
```
