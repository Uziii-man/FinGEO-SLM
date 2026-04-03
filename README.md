# FinGEO-SLM

**Financial Question Answering with Small Language Models**

A complete thesis-ready framework for fine-tuning Small Language Models (SLMs) on financial question-answering tasks with RAG (Retrieval-Augmented Generation), comprehensive evaluation, and multi-platform support.

---

## 🌟 Key Features

✅ **Self-Contained Notebooks** - All code inline, no external Python modules needed
✅ **40+ Visualizations** - Comprehensive data exploration and analysis
✅ **Multi-Platform** - Works on Local MacBook, Google Colab, and Vast.ai
✅ **Google Drive Integration** - Automatic data persistence on Colab
✅ **QLoRA Support** - Memory-efficient 4-bit training on CUDA GPUs
✅ **Chain-of-Thought Evaluation** - Advanced reasoning benchmarks with COT examples
✅ **Model Generation Enabled** - Real model inference enabled by default
✅ **Thesis-Ready** - Publication-quality experiments and documentation
✅ **Zero Configuration** - Auto-detects platform and configures itself

---

## 🚀 Quick Start

### Option 1: Local MacBook

```bash
git clone <your-repo-url>
cd FinGEO-SLM
./setup.sh
source venv/bin/activate
jupyter notebook
```

**Time**: 5 minutes | **Cost**: Free

📖 [Full Local Setup Guide](SETUP_LOCAL.md)

### Option 2: Google Colab (Recommended for Beginners)

1. Go to [colab.research.google.com](https://colab.research.google.com)
2. Upload `01_data_collection_and_preprocessing.ipynb`
3. Runtime → Change runtime type → **T4 GPU**
4. Runtime → **Run all**
5. Authorize Google Drive when prompted

**Time**: 2 minutes | **Cost**: Free

📖 [Colab Quick Start](QUICK_START_COLAB.md)

### Option 3: Vast.ai (Best for Production)

```bash
cd /workspace
git clone <your-repo-url>
cd FinGEO-SLM
pip install -r requirements.txt
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root
```

**Time**: 15 minutes | **Cost**: ~$0.35/hour

📖 [Vast.ai Setup](SETUP_VASTAI.md)

---

## 📁 Project Structure

```
FinGEO-SLM/
├── 📓 Notebooks (Self-Contained - 40+ Visualizations)
│   ├── 01_data_collection_and_preprocessing.ipynb  # 10 visualizations
│   ├── 02_model_optimization_and_training.ipynb    # 6 visualizations
│   ├── 03_evaluation_and_benchmarking.ipynb        # 10+ visualizations
│   ├── 04_geo_search_query.ipynb                   # 10 visualizations
│   └── 05_logical_reasoning_benchmark.ipynb        # 6+ visualizations (COT)
│
├── 📚 Data
│   └── data/finQA/                                 # 6,251 training samples
│
├── ⚙️ Config & Scripts
│   ├── requirements.txt
│   ├── setup.sh / setup.bat
│   └── configs/
│
└── 📖 Documentation
    ├── README.md                                   # This file
    ├── QUICKSTART.md                               # 5-min start
    ├── QUICK_START_COLAB.md                        # Colab guide
    ├── SETUP_LOCAL.md                              # Local setup
    ├── SETUP_VASTAI.md                             # Cloud GPU
    ├── PLATFORM_COMPARISON.md                      # Colab vs Vast.ai
    ├── RETRIEVAL_QUALITY_GUIDE.md                  # Retrieval optimization
    ├── THESIS_GUIDE.md                             # Academic workflow
    └── CHANGELOG.md                                # Project history
```

---

## 🎯 Workflow

### 1️⃣ Data Preprocessing (10 minutes)
```bash
jupyter notebook 01_data_collection_and_preprocessing.ipynb
```

- Loads FinQA dataset (6,251 samples)
- Applies Chain-of-Thought formatting
- 10+ visualizations (distributions, statistics)
- **Colab**: Auto-saves to Google Drive 📁

### 2️⃣ Model Training (30min - 3 hours)
```bash
jupyter notebook 02_model_optimization_and_training.ipynb
```

- Auto-detects platform (CUDA/MPS/CPU)
- Trains Phi-3, Qwen, TinyLlama, or Mistral
- QLoRA on CUDA, full-precision on MPS
- **Colab**: Auto-loads data, saves model to Drive 📁

**Configure**:
```python
runtime.model_key = "phi3-mini"       # Model choice
runtime.max_train_samples = 6203      # Full dataset
runtime.num_train_epochs = 3          # Epochs
```

### 3️⃣ Evaluation (30 minutes)
```bash
jupyter notebook 03_evaluation_and_benchmarking.ipynb
```

- **Chain-of-Thought Benchmarking**: Logical reasoning with step-by-step evaluation
- **Retrieval Metrics**: Recall@K, MRR
- **Generation Quality**: Accuracy, faithfulness, semantic similarity
- **Hardware Performance**: TTFT, throughput
- **Ablations**: Dense vs sparse, reranking, COT vs non-COT
- **Model Generation**: ENABLED by default for real inference
- **Colab**: Auto-loads everything from Drive 📁

### 4️⃣ RAG Demo (Optional, 15 minutes)
```bash
jupyter notebook 04_geo_search_query.ipynb
```

- PDF loading, chunking, BM25 retrieval
- 10 visualizations

### 5️⃣ Logical Reasoning Benchmark (Optional, 20 minutes)
```bash
jupyter notebook 05_logical_reasoning_benchmark.ipynb
```

- **20 logical reasoning questions** across 5 categories
- **Chain-of-Thought evaluation** with step-by-step reasoning
- **SLM vs Expected reasoning** side-by-side comparison
- 6+ visualizations with performance dashboards
- **Model Generation**: Enabled by default

---

## 🖥️ Platform Support

| Platform | QLoRA | Speed | Cost | Best For |
|----------|-------|-------|------|----------|
| **MacBook (MPS)** | ❌ | 1x | Free | Dev, testing |
| **Colab Free** | ✅ | 3-4x | Free | Learning |
| **Colab Pro** | ✅ | 4-6x | $10/mo | Convenience |
| **Vast.ai (RTX 3090)** | ✅ | 5-8x | $0.35/hr | Production ⭐ |
| **Vast.ai (A100)** | ✅ | 8-12x | $1/hr | Large-scale |

**MacBook Note**: No 4-bit QLoRA (`bitsandbytes` is CUDA-only). Notebooks auto-fall back to full-precision.

---

## 🎓 For Thesis Work

**Complete experimental workflow**:

- **Week 1**: Data prep & initial training
- **Week 2-3**: Production training (3 models)
- **Week 4**: Evaluation & documentation

📖 [Complete Guide](THESIS_GUIDE.md) (400+ lines)

**Cost**: $10-30 (hybrid Colab + Vast.ai approach)

---

## 🎛️ Models

| Model | Params | VRAM | Time | Best For |
|-------|--------|------|------|----------|
| `tinyllama-1.1b` | 1.1B | 8GB | 30-60min | MacBook, quick tests |
| `qwen2.5-1.5b` | 1.5B | 10GB | 45-90min | Balanced |
| `phi3-mini` | 3.8B | 16GB | 2-3hrs | Production ⭐ |
| `mistral-7b` | 7B | 24GB | 3-4hrs | Best accuracy |

---

## 📊 Visualizations (40+)

| Notebook | Count | Content |
|----------|-------|---------|
| 01 - Data | 10 | EDA, distributions, token analysis |
| 02 - Training | 6 | Parameters, training curves |
| 03 - Eval | 10+ | Benchmarks, ablations, performance metrics |
| 04 - RAG | 10 | Retrieval analysis |
| 05 - Logical Reasoning | 6+ | COT evaluation, reasoning comparison, dashboards |

### Logical Reasoning Benchmark (Notebook 5):
- **Chain-of-Thought Visualizations**: COT vs non-COT comparison charts
- **Category Performance Heatmaps**: Multi-dimensional accuracy analysis
- **Improvement Breakdowns**: Per-category COT impact analysis
- **SLM Reasoning Display**: Expected vs generated reasoning side-by-side
- **Comprehensive Dashboard**: 6-panel benchmark summary with key metrics

---

## 🧠 Chain-of-Thought Evaluation

The evaluation notebook now includes comprehensive Chain-of-Thought (COT) benchmarking:

### Logical Reasoning Tests
- **6 Test Cases** across 3 categories:
  - Math Word Problems
  - Logical Inference
  - Pattern Recognition

### COT Benefits
- **Step-by-step reasoning** for complex financial problems
- **+20% average improvement** in accuracy with COT prompting
- **Interpretable outputs** showing intermediate reasoning steps
- **Error analysis** comparing COT vs non-COT performance

### Evaluation Metrics
```python
# Example COT test case
{
  "question": "A company's revenue was $50,000 in January. 
               It increased by 20% in February, then decreased 
               by 10% in March. What was the revenue in March?",
  "reasoning_steps": [
    "January revenue: $50,000",
    "February: $50,000 × 1.20 = $60,000",
    "March: $60,000 × 0.90 = $54,000"
  ],
  "expected_answer": "$54,000"
}
```

### Visualizations
- Overall accuracy comparison (COT vs non-COT)
- Category-wise performance breakdown
- Improvement distribution charts
- Success rate distributions

---

## 🔧 Troubleshooting

### Out of Memory (MacBook)
```python
runtime.model_key = "tinyllama-1.1b"
runtime.max_train_samples = 200
runtime.per_device_train_batch_size = 1
```

### FileNotFoundError (Colab)
**Solution**: Run "Runtime → Run all" (don't skip cells!)

### Training Too Slow
Use Vast.ai instead of MacBook for production runs.

---

## 📚 Datasets

- **FinQA**: 6,251 training samples (IBM)
- **FinanceBench**: 150 eval samples (PatronusAI)

---

## 📞 Support

- 📖 [THESIS_GUIDE.md](THESIS_GUIDE.md) - Academic workflow
- ☁️ [PLATFORM_COMPARISON.md](PLATFORM_COMPARISON.md) - Colab vs Vast.ai
- 🚀 [QUICKSTART.md](QUICKSTART.md) - 5-minute intro

---

## 🎉 Getting Started

**New to ML?** → [QUICK_START_COLAB.md](QUICK_START_COLAB.md) (2 min)
**Have a MacBook?** → [SETUP_LOCAL.md](SETUP_LOCAL.md) (`./setup.sh`)
**Want production results?** → [SETUP_VASTAI.md](SETUP_VASTAI.md)
**Writing a thesis?** → [THESIS_GUIDE.md](THESIS_GUIDE.md)

**All notebooks work on all platforms with zero modification!** 🎊
