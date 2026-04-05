# FinGEO-SLM

**Financial Question Answering with Small Language Models**

A production-ready framework for fine-tuning Small Language Models (SLMs) on financial question-answering tasks with RAG (Retrieval-Augmented Generation) and comprehensive evaluation.

> **⚠️ GPU REQUIRED**: This project requires a CUDA-capable GPU. Recommended: Vast.ai GPU instance (RTX 4090/5090).

---

## 🌟 Key Features

✅ **GPU-Optimized** - CUDA-only for maximum performance  
✅ **40+ Visualizations** - Comprehensive data exploration and analysis  
✅ **QLoRA Training** - Memory-efficient 4-bit training on GPUs  
✅ **Chain-of-Thought Evaluation** - Advanced reasoning benchmarks  
✅ **RAG Pipeline** - Dense + sparse retrieval with reranking  
✅ **Production-Ready** - Clean, focused codebase  
✅ **Thesis-Ready** - Publication-quality experiments and documentation  

---

## 🚀 Quick Start (Vast.ai)

### 1. Rent a GPU Instance

**Recommended**: RTX 4090 or 5090 (24-32GB VRAM)

```bash
# Vast.ai search filters:
# - GPU: RTX 4090 or 5090
# - VRAM: ≥24GB
# - Disk: ≥50GB
# - Cost: ~$0.35-0.60/hour
```

### 2. Setup Environment

```bash
# Clone repository
cd /workspace
git clone <your-repo-url>
cd FinGEO-SLM

# Run setup script (installs dependencies, validates GPU)
./setup.sh

# Verify GPU
python3 -c "from gpu_utils import print_gpu_quick_check; print_gpu_quick_check()"
```

### 3. Run Notebooks

```bash
# Start Jupyter
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root

# Then access via Vast.ai's provided URL
```

**Execution Order**:
1. `01_data_collection_and_preprocessing.ipynb` (10 min)
2. `02_model_optimization_and_training.ipynb` (15-45 min)
3. `03_evaluation_and_benchmarking.ipynb` (30 min)
4. `04_geo_search_query.ipynb` (optional, 15 min)
5. `05_logical_reasoning_benchmark.ipynb` (optional, 20 min)

**Total Time**: ~1-2 hours | **Cost**: $0.60-1.20

📖 **Full Setup Guide**: [SETUP_VASTAI.md](SETUP_VASTAI.md)

---

## 📁 Project Structure

```
FinGEO-SLM/
├── 📓 Notebooks
│   ├── 01_data_collection_and_preprocessing.ipynb
│   ├── 02_model_optimization_and_training.ipynb
│   ├── 03_evaluation_and_benchmarking.ipynb
│   ├── 04_geo_search_query.ipynb
│   └── 05_logical_reasoning_benchmark.ipynb
│
├── 📚 Data
│   └── data/finQA/
│
├── ⚙️ Configuration
│   ├── requirements.txt
│   ├── setup.sh
│   └── gpu_utils.py
│
└── 📖 Documentation
    ├── README.md
    ├── SETUP_VASTAI.md
    ├── QUICKSTART.md
    ├── TRAINING_GUIDE.md
    ├── BENCHMARK_GUIDE.md
    └── THESIS_GUIDE.md
```

---

## 🖥️ GPU Requirements

| GPU | VRAM | Training Time | Cost/Hour | Status |
|-----|------|---------------|-----------|--------|
| RTX 5090 | 32GB | 15-20 min | $0.50-0.80 | ✅ Best |
| RTX 4090 | 24GB | 20-30 min | $0.35-0.50 | ✅ Great |
| RTX 3090 | 24GB | 30-45 min | $0.25-0.40 | ✅ Good |
| A100 (40GB) | 40GB | 15-25 min | $1.00-1.50 | ⚡ Fastest |

**Minimum**: 16GB VRAM  
**Recommended**: 24GB+ VRAM

---

## 🎛️ Supported Models

| Model | Parameters | VRAM | Training Time |
|-------|-----------|------|---------------|
| `phi3-mini` | 3.8B | 16GB | 20-45min ⭐ |
| `qwen2.5-1.5b` | 1.5B | 10GB | 20-35min |
| `mistral-7b` | 7B | 24GB | 45-90min |

---

## 📖 Documentation

- **[SETUP_VASTAI.md](SETUP_VASTAI.md)** - Vast.ai setup guide
- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute overview  
- **[TRAINING_GUIDE.md](TRAINING_GUIDE.md)** - Training procedures
- **[THESIS_GUIDE.md](THESIS_GUIDE.md)** - Academic workflow

---

## 🎉 Getting Started

```bash
# 1. Rent Vast.ai GPU (RTX 4090/5090)
# 2. Clone and setup
./setup.sh

# 3. Start Jupyter
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root

# 4. Run notebooks in order
```

**Questions?** See [SETUP_VASTAI.md](SETUP_VASTAI.md)

---

**🚀 Ready for production GPU training!**
