# FinGEO-SLM

A financial AI project for fine-tuning Small Language Models (SLMs) on financial question-answering tasks with RAG (Retrieval-Augmented Generation) and benchmark evaluation.

## 🚀 Quick Start

### Local MacBook Setup
```bash
git clone <your-repo-url>
cd FinGEO-SLM
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
jupyter notebook
```

📖 **Detailed Guide**: See [SETUP_LOCAL.md](SETUP_LOCAL.md)

### Vast.ai Cloud GPU Setup
```bash
ssh root@<instance-ip> -p <port>
cd /workspace
git clone <your-repo-url>
cd FinGEO-SLM
pip install -r requirements.txt
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root
```

📖 **Detailed Guide**: See [SETUP_VASTAI.md](SETUP_VASTAI.md)

## 📁 Project Structure

```
FinGEO-SLM/
├── 01_data_collection_and_preprocessing.ipynb  # Data loading, EDA, and prompt formatting
├── 02_model_optimization_and_training.ipynb    # Model training with QLoRA/full-precision
├── 03_evaluation_and_benchmarking.ipynb        # Comprehensive performance evaluation
├── 04_geo_search_query.ipynb                   # RAG document retrieval demo
├── data/finQA/                                 # Training datasets (FinQA)
├── configs/                                    # Configuration templates
├── requirements.txt                            # Python dependencies
├── setup.sh / setup.bat                        # Automated setup scripts
└── QUICKSTART.md                               # Quick start guide
```

**Note:** All code is self-contained within the notebooks - no external Python modules required!

## 🎯 Usage

Run notebooks in order:

### 1. Data Preprocessing
```bash
jupyter notebook 01_data_collection_and_preprocessing.ipynb
```
- Loads FinQA dataset
- Formats data with Chain-of-Thought prompts
- Performs EDA with 10+ visualizations
- Token analysis and statistics
- Saves processed data to `processed_data/`

**New visualizations:** Dataset size comparison, question/answer length distributions, table size scatter plots, word frequency analysis, token distributions with percentiles

### 2. Model Training
```bash
jupyter notebook 02_model_optimization_and_training.ipynb
```
- Loads pre-trained SLM (Phi-3, Qwen, TinyLlama, Mistral)
- Auto-detects backend and applies QLoRA (4-bit) on CUDA or full-precision on MPS/CPU
- All code is self-contained in notebook cells
- Trains on financial Q&A data
- Comprehensive visualizations: token distributions, parameter breakdowns, training curves
- Saves adapter to `fingeo-slm-adapter/`

**New visualizations:** Dataset statistics, enhanced token length distributions, model parameter pie charts, training/validation split comparison, smoothed loss curves with moving averages

**Configuration**:
```python
runtime.model_key = "phi3-mini"  # or "qwen2.5-1.5b", "tinyllama-1.1b", "mistral-7b"
runtime.max_train_samples = 1000  # Reduce for faster iteration
runtime.num_train_epochs = 3
```

### 3. Evaluation
```bash
jupyter notebook 03_evaluation_and_benchmarking.ipynb
```
Runs comprehensive benchmarks with extensive visualizations:
- **Retrieval**: Recall@K, MRR, noise reduction
- **Generation**: Semantic accuracy, hallucination rate, exact match
- **Hardware**: TTFT, latency, throughput, memory usage
- **Ablations**: Dense vs sparse retrieval, with/without reranking

**New visualizations:** Enhanced TTFT/SSoV charts, reranker confidence plots, retrieval quality heatmaps, ablation comparison grids (2x2), efficiency metrics comparison, comprehensive results summary

### 4. RAG Demo (Optional)
```bash
jupyter notebook 04_geo_search_query.ipynb
```
- PDF document loading and chunking
- BM25 sparse retrieval
- Query-based document search
- 10+ visualizations for search analysis

**New visualizations:** Document/page statistics, chunk size distributions, keyword frequency, retrieval score distributions, similarity heatmaps, BM25 decay curves, chunk rank comparisons, length vs score scatter plots, query complexity analysis

## 🖥️ Platform Support

| Platform | QLoRA (4-bit) | Full Precision | Notes |
|----------|---------------|----------------|-------|
| **MacBook (MPS)** | ❌ | ✅ | Use smaller models (1.5B-3B params) |
| **CUDA GPU** | ✅ | ✅ | Full QLoRA support (recommended) |
| **CPU** | ❌ | ✅ | Very slow, not recommended |
| **Google Colab** | ✅ | ✅ | Free T4 GPU (limited runtime) |
| **Vast.ai** | ✅ | ✅ | Affordable GPU rental |

### Why No QLoRA on MacBook?
- `bitsandbytes` (4-bit quantization) is CUDA-only
- Apple Silicon (MPS) doesn't support it
- Notebooks automatically fall back to full-precision FP16/FP32

## 🎛️ Model Selection

Built-in model presets:

| Model | Size | Best For | VRAM |
|-------|------|----------|------|
| `tinyllama-1.1b` | 1.1B | MacBook, quick testing | 4-8GB |
| `qwen2.5-1.5b` | 1.5B | MacBook, balanced performance | 6-10GB |
| `phi3-mini` | 3.8B | General use, good accuracy | 12-16GB |
| `mistral-7b` | 7B | Best accuracy, baseline | 20-24GB |

## 📊 Expected Performance

### MacBook M1/M2 (16GB RAM)
- Model: TinyLlama or Qwen2.5-1.5B
- Batch size: 1-2
- Training time: 30-60 min (200 samples)
- Inference: 10-20 tokens/sec

### CUDA GPU (RTX 3090, 24GB)
- Model: Phi-3 or Mistral-7B
- Batch size: 4-8 with QLoRA
- Training time: 1-2 hours (full dataset)
- Inference: 30-60 tokens/sec

## 🔧 Key Features

✅ **Self-Contained Notebooks**: All code is inline - no external Python modules needed
✅ **Rich Visualizations**: 30+ charts and graphs across all notebooks
✅ **Automatic Platform Detection**: Detects Colab/Vast/Local and configures accordingly
✅ **Smart Backend Selection**: QLoRA on CUDA, full-precision on MPS/CPU
✅ **Data Quality Checks**: Removes empty/duplicate prompts
✅ **Comprehensive Benchmarks**: Retrieval, generation, hardware, ablations
✅ **Cloud-Ready**: Works on Colab, vast.ai, and local machines
✅ **Easy to Share**: Single notebook files can be shared and run independently

## 📦 Dependencies

Main libraries:
- `torch` - PyTorch deep learning framework
- `transformers` - Hugging Face model library
- `peft` - Parameter-Efficient Fine-Tuning (LoRA)
- `datasets` - Dataset loading and processing
- `langchain` - RAG document retrieval
- `bitsandbytes` - 4-bit quantization (optional, CUDA only)

See [requirements.txt](requirements.txt) for complete list.

## 🐛 Troubleshooting

### Out of Memory
```python
# In notebook 02:
runtime.per_device_train_batch_size = 1
runtime.gradient_accumulation_steps = 8
runtime.max_train_samples = 200
```

### Module Not Found
```bash
pip install -r requirements.txt --force-reinstall
```

### CUDA Not Available
```bash
# Verify PyTorch installation
python -c "import torch; print(torch.cuda.is_available())"

# Reinstall PyTorch with CUDA
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

### Notebook Kernel Crashes
- Reduce model size (use TinyLlama)
- Reduce batch size and max_train_samples
- Close other applications

## 📚 Dataset Information

### FinQA
- **Source**: [FinQA Dataset](https://github.com/czyssrs/FinQA)
- **Size**: 6,251 training examples
- **Format**: Financial tables + question + reasoning steps + answer
- **Use**: Fine-tuning SLMs

### FinanceBench
- **Source**: [PatronusAI/financebench](https://huggingface.co/datasets/PatronusAI/financebench)
- **Size**: 150 examples
- **Use**: Evaluation benchmark

## 🎓 Academic Context

This project follows thesis-standard practices:
- Modular, reusable code architecture
- Rigorous data validation and cleaning
- Comprehensive evaluation metrics
- Hardware-agnostic design
- Reproducible experiments

## 📄 License

[Add your license here]

## 🤝 Contributing

[Add contribution guidelines here]

## 📧 Contact

[Add your contact information here]

---

**Ready to start?** Choose your platform and follow the setup guide:
- 💻 [Local MacBook Setup](SETUP_LOCAL.md)
- ☁️ [Vast.ai Cloud Setup](SETUP_VASTAI.md)
