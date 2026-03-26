# Vast.ai Setup Guide

This guide helps you run FinGEO-SLM on vast.ai cloud GPU instances.

## Prerequisites

- Vast.ai account with credits
- SSH client (terminal or PuTTY)
- Basic Linux command knowledge

## Step 1: Rent a GPU Instance

1. Go to [vast.ai](https://vast.ai/)
2. Select a GPU instance:
   - **Recommended**: RTX 3090/4090, A4000, or better
   - **Minimum**: 24GB VRAM for full QLoRA training
   - **Budget**: 16GB VRAM (reduce batch size)
3. Select a Docker image:
   - **Recommended**: `pytorch/pytorch:2.0.1-cuda11.8-cudnn8-devel`
   - Or any PyTorch 2.0+ with CUDA 11.7+
4. Click "Rent" and wait for instance to start

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

### Recommended Training Config

For optimal performance on vast.ai with 24GB VRAM:

```python
# In notebook 02:
runtime.model_key = "phi3-mini"  # or "mistral-7b" for larger GPU
runtime.max_train_samples = 1000  # or full dataset (6251)
runtime.per_device_train_batch_size = 4
runtime.gradient_accumulation_steps = 4
runtime.num_train_epochs = 3
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
- Use `interruptible` instances for non-critical work
- Stop instance when not in use
- Use smaller models for testing, full models for final runs

## Expected Performance

On RTX 3090 (24GB):
- **Data preprocessing**: 3-5 minutes
- **Training (full dataset, QLoRA)**: 1-2 hours
- **Evaluation**: 10-15 minutes

On A100 (40GB):
- **Data preprocessing**: 2-3 minutes
- **Training (full dataset, QLoRA)**: 30-60 minutes
- **Evaluation**: 5-10 minutes

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
