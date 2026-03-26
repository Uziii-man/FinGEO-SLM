# Quick Start Guide

Get FinGEO-SLM running in 5 minutes.

## Prerequisites
- Python 3.9+
- 8GB+ RAM (16GB+ recommended)
- 10GB+ free disk space

## One-Line Setup

### macOS/Linux
```bash
./setup.sh
```

### Windows
```cmd
setup.bat
```

## Manual Setup (3 Steps)

### 1. Create Environment
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate.bat  # Windows
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Start Jupyter
```bash
jupyter notebook
```

## Run Your First Experiment

Open notebooks in order:

### 1️⃣ Data Preprocessing (5 min)
```bash
01_data_collection_and_preprocessing.ipynb
```
Loads and formats FinQA dataset.

### 2️⃣ Model Training (30-60 min)
```bash
02_model_optimization_and_training.ipynb
```
Trains a financial AI model.

**MacBook users**: Change these settings in the notebook:
```python
runtime.model_key = "tinyllama-1.1b"  # Use smaller model
runtime.max_train_samples = 200        # Train on fewer samples
```

### 3️⃣ Evaluation (10 min)
```bash
03_evaluation_and_benchmarking.ipynb
```
Tests model performance.

## Platform-Specific Tips

### 💻 Running on MacBook
- Use smaller models: `tinyllama-1.1b` or `qwen2.5-1.5b`
- Reduce samples: `max_train_samples = 200`
- Full-precision only (no QLoRA)

### ☁️ Running on Vast.ai
- Use any GPU with 16GB+ VRAM
- Full QLoRA (4-bit) support
- Can train on full dataset (6,251 samples)

### 🆓 Running on Google Colab
- Free T4 GPU available
- Notebooks work out-of-the-box
- QLoRA supported

## Common Issues

### Out of Memory?
```python
# Reduce these in notebook 02:
runtime.per_device_train_batch_size = 1
runtime.max_train_samples = 100
```

### CUDA Not Available?
If you have an NVIDIA GPU but CUDA isn't working:
```bash
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

### Module Not Found?
```bash
pip install -r requirements.txt --force-reinstall
```

## Need More Help?

- 📖 [Detailed MacBook Setup](SETUP_LOCAL.md)
- ☁️ [Detailed Vast.ai Setup](SETUP_VASTAI.md)
- 📘 [Full Documentation](README.md)

## What You'll Get

After running all 3 notebooks:
- ✅ Trained financial AI model
- ✅ Performance benchmarks
- ✅ Model saved to `fingeo-slm-adapter/`
- ✅ Processed data in `processed_data/`

Ready? Run `./setup.sh` (or `setup.bat`) and start Jupyter!
