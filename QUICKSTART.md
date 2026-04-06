# FinGEO-SLM Quick Start

**Get up and running in 15 minutes on Vast.ai**

---

## Prerequisites

- **GPU Required**: CUDA-capable GPU (RTX 4090/5090 recommended)
- **Platform**: Vast.ai GPU instance
- **Budget**: ~$0.35-0.60/hour

---

## Step 1: Rent Vast.ai GPU (5 minutes)

1. Go to [vast.ai](https://vast.ai)
2. Search for instances:
   - **GPU**: RTX 4090 or 5090
   - **VRAM**: ≥24GB
   - **Disk**: ≥50GB
   - **Sort by**: Price (lowest first)

3. Rent instance and SSH in:
```bash
ssh root@<instance-ip> -p <port>
```

---

## Step 2: Setup (5 minutes)

```bash
# Navigate to workspace
cd /workspace

# Clone repository
git clone <your-repo-url>
cd FinGEO-SLM

# Run setup script
./setup.sh
```

The setup script will:
- ✅ Validate GPU availability
- ✅ Install dependencies
- ✅ Create output directories
- ✅ Show estimated training time

---

## Step 3: Start Jupyter (1 minute)

```bash
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root
```

Then:
1. Copy the URL with token from terminal
2. Replace `127.0.0.1` with your Vast.ai instance IP
3. Open in browser

---

## Step 4: Run Notebooks (1-2 hours)

Execute in order:

### 1. Data Preprocessing (10 min)
```
01_data_collection_and_preprocessing.ipynb
```
- Loads and formats FinQA dataset
- 10+ visualizations

### 2. Model Training (15-45 min)
```
02_model_optimization_and_training.ipynb
```
- QLoRA 4-bit training
- GPU-optimized
- Auto-saves model

**Training time by GPU**:
- RTX 5090: ~15-20 min
- RTX 4090: ~20-30 min  
- RTX 3090: ~30-45 min

### 3. Retrieval Evaluation (30 min)
```
03_retrieval_evaluation.ipynb
```
- Retrieval pipeline setup
- TTFT/SSoV benchmarks
- Basic visualizations

### 4. Model Comparison & Ablation (30 min)
```
04_model_comparison_and_ablation.ipynb
```
- Comparative model evaluation
- Ablation studies
- Comprehensive dashboard

### 5. Optional: Geo Search Query (15 min)
```
05_geo_search_query.ipynb
```

### 6. Optional: Reasoning Benchmark (20 min)
```
06_logical_reasoning_benchmark.ipynb
```

---

## Expected Costs

| GPU | Time | Cost |
|-----|------|------|
| RTX 4090 | 1.5 hrs | $0.50-0.75 |
| RTX 5090 | 1 hr | $0.50-0.80 |

**Total Project Cost**: $1-2 for complete run

---

## Troubleshooting

### GPU Not Detected
```bash
nvidia-smi  # Check GPU availability
python3 -c "from gpu_utils import validate_gpu_environment; validate_gpu_environment()"
```

### Out of Memory
Edit notebook cell:
```python
runtime.per_device_train_batch_size = 2
runtime.gradient_accumulation_steps = 8
```

### Dependencies Missing
```bash
pip install -r requirements.txt --force-reinstall
```

---

## Next Steps

- **Detailed Setup**: See [SETUP_VASTAI.md](SETUP_VASTAI.md)
- **Training Guide**: See [TRAINING_GUIDE.md](TRAINING_GUIDE.md)
- **Thesis Work**: See [THESIS_GUIDE.md](THESIS_GUIDE.md)

---

**Questions?** Check [SETUP_VASTAI.md](SETUP_VASTAI.md) for detailed troubleshooting.
