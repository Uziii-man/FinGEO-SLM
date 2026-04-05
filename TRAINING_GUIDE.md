# FinGEO-SLM Training Guide

This guide walks you through training a financial QA model on Vast.ai GPU.

---

## Prerequisites

- **GPU Required**: CUDA-capable GPU (RTX 4090/5090 recommended)
- **Platform**: Vast.ai GPU instance
- **Data**: FinQA dataset (included in repository)
- **Time**: 15-45 minutes depending on GPU

---

## Quick Start

### Step 1: Setup Vast.ai Instance

```bash
# 1. Rent GPU instance on vast.ai (RTX 4090/5090 recommended)
# 2. SSH into instance
ssh root@<instance-ip> -p <port>

# 3. Clone and setup
cd /workspace
git clone <your-repo-url>
cd FinGEO-SLM
./setup.sh
```

### Step 2: Run Data Preprocessing

```bash
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root
```

1. Open `01_data_collection_and_preprocessing.ipynb`
2. Run all cells
3. Wait for completion (~10 minutes)

### Step 3: Train Model

1. Open `02_model_optimization_and_training.ipynb`
2. Configure model (optional):
```python
runtime.model_key = "phi3-mini"       # Model choice
runtime.max_train_samples = 6203      # Full dataset
runtime.num_train_epochs = 3          # Epochs
```
3. Run all cells
4. Training completes in 15-45 minutes

### Step 4: Evaluate

1. Open `03_evaluation_and_benchmarking.ipynb`
2. Run all cells
3. Review benchmarks and visualizations

---

## Training Configuration

### Model Options

| Model | Parameters | VRAM | Time | Best For |
|-------|-----------|------|------|----------|
| `phi3-mini` | 3.8B | 16GB | 20-45 min | Production ⭐ |
| `qwen2.5-1.5b` | 1.5B | 10GB | 15-30 min | Balanced |
| `mistral-7b` | 7B | 24GB | 45-90 min | Best accuracy |

### Training Parameters

```python
# Default configuration
runtime.model_key = "phi3-mini"
runtime.max_train_samples = 6203      # Full dataset
runtime.num_train_epochs = 3
runtime.per_device_train_batch_size = 4
runtime.gradient_accumulation_steps = 4
runtime.learning_rate = 2e-4
```

### GPU-Specific Settings

| GPU | VRAM | Batch Size | Expected Time |
|-----|------|------------|---------------|
| RTX 5090 | 32GB | 8 | 15-20 min |
| RTX 4090 | 24GB | 4 | 20-30 min |
| RTX 3090 | 24GB | 4 | 30-45 min |
| A100 | 40GB | 8 | 15-25 min |

---

## Troubleshooting

### Out of Memory (OOM)

```python
# Reduce batch size
runtime.per_device_train_batch_size = 2
runtime.gradient_accumulation_steps = 8
```

### Training Too Slow

- Check GPU utilization: `nvidia-smi`
- Ensure CUDA is detected
- Consider faster GPU (RTX 5090/A100)

### Model Not Saving

- Check disk space: `df -h`
- Verify output directory exists
- Check permissions

---

## Output Files

After training:

```
fingeo_slm_outputs/
├── finetuned_model/          # Main model (~7GB)
│   ├── config.json
│   ├── model.safetensors
│   ├── tokenizer.json
│   └── ...
└── fingeo-slm-adapter/       # LoRA adapter (~50MB)
```

---

## Cost Estimates

| GPU | Hourly Rate | Training Time | Total Cost |
|-----|-------------|---------------|------------|
| RTX 4090 | $0.35-0.50 | 30-45 min | $0.25-0.40 |
| RTX 5090 | $0.50-0.80 | 15-25 min | $0.20-0.35 |
| A100 | $1.00-1.50 | 15-25 min | $0.40-0.65 |

**Total Project Cost**: $1-3 for complete training + evaluation

---

## Next Steps

After training:
1. Run `03_evaluation_and_benchmarking.ipynb` for evaluation
2. Run `04_geo_search_query.ipynb` for RAG demo
3. Run `05_logical_reasoning_benchmark.ipynb` for reasoning tests
4. Download model to permanent storage

See [THESIS_GUIDE.md](THESIS_GUIDE.md) for academic workflow.
