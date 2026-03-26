# Local MacBook Setup Guide

This guide helps you run FinGEO-SLM on your local MacBook (Apple Silicon or Intel).

## Prerequisites

- macOS 12+ (Monterey or later)
- Python 3.9 or higher
- 16GB+ RAM recommended
- 20GB+ free disk space

## Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd FinGEO-SLM
```

## Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate
```

## Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install PyTorch for macOS (Apple Silicon MPS support)
pip install torch torchvision torchaudio

# Install other dependencies
pip install -r requirements.txt
```

**Note**: On MacBook, `bitsandbytes` (used for QLoRA) may not work as it's CUDA-only. The notebooks will automatically fall back to full-precision training on MPS/CPU.

## Step 4: Install Jupyter

```bash
# Jupyter is already in requirements.txt, but ensure it's available
pip install jupyter notebook

# Register the virtual environment as a Jupyter kernel
python -m ipykernel install --user --name=fingeo-slm --display-name "FinGEO-SLM"
```

## Step 5: Run the Notebooks

```bash
# Start Jupyter
jupyter notebook

# Or use Jupyter Lab
jupyter lab
```

Then open the notebooks in this order:
1. `01_data_collection_and_preprocessing.ipynb`
2. `02_model_optimization_and_training.ipynb`
3. `03_evaluation_and_benchmarking.ipynb`
4. `04_geo_search_query.ipynb` (optional)

## Important Notes for MacBook

### Memory Constraints
- Use smaller models on MacBook (TinyLlama, Qwen2.5-1.5B)
- Reduce `max_train_samples` in notebook 02 (try 100-500 samples)
- Close other applications during training

### No QLoRA on MacBook
The notebooks detect your platform automatically:
- **MacBook (MPS)**: Uses full-precision training (FP16/FP32)
- **CUDA GPU**: Uses 4-bit QLoRA for memory efficiency

### Model Selection
Edit the notebook configs to use smaller models:
```python
runtime.model_key = "tinyllama-1.1b"  # or "qwen2.5-1.5b"
runtime.max_train_samples = 200
```

### Expected Performance
- **Data preprocessing**: 2-5 minutes
- **Training (200 samples)**: 30-60 minutes on M1/M2
- **Evaluation**: 10-20 minutes

## Troubleshooting

### Issue: Out of Memory
```bash
# Reduce batch size in notebook
runtime.per_device_train_batch_size = 1
runtime.gradient_accumulation_steps = 8
```

### Issue: PyTorch not detecting MPS
```python
import torch
print(torch.backends.mps.is_available())  # Should be True on Apple Silicon
```

### Issue: Module not found
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Next Steps

After setup, proceed to the [main README](README.md) for usage instructions.
