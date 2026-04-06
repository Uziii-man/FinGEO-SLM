# FinGEO-SLM Thesis Experimental Guide

## Complete Guide for Academic Research and Thesis Work

This guide provides a systematic approach to training, testing, and documenting FinGEO-SLM experiments for thesis/research purposes.

---

## 📋 Table of Contents

1. [Experimental Setup](#experimental-setup)
2. [Phase 1: Data Preparation](#phase-1-data-preparation)
3. [Phase 2: Model Training](#phase-2-model-training)
4. [Phase 3: Evaluation](#phase-3-evaluation)
5. [Phase 4: Ablation Studies](#phase-4-ablation-studies)
6. [Phase 5: Results Documentation](#phase-5-results-documentation)
7. [Thesis Writing Tips](#thesis-writing-tips)

---

## Experimental Setup

### Environment Options

#### Option A: Vast.ai GPU Instance
**Best for:** Initial testing, code development, small experiments

```bash
# Setup
cd FinGEO-SLM
./setup.sh
source venv/bin/activate

# Verify setup
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
```

**Recommended configuration:**
- Model: TinyLlama-1.1B or Qwen2.5-1.5B
- Training samples: 200-500 (for quick iteration)
- Use for: Code debugging, visualization testing, initial experiments

#### Option B: Vast.ai (Production Experiments)
**Best for:** Full-scale training, final experiments, thesis results

```bash
# On vast.ai instance
cd /workspace
git clone <your-repo-url>
cd FinGEO-SLM
pip install -r requirements.txt

# Verify CUDA
nvidia-smi
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
```

**Recommended configuration:**
- GPU: RTX 3090/4090 (24GB) or A100 (40GB)
- Model: Phi-3-Mini or Mistral-7B
- Training samples: Full dataset (6,203 samples)
- Use for: Final experiments, benchmark results, thesis data

---

## Phase 1: Data Preparation

### Notebook 01: Data Collection and Preprocessing

**Objective:** Prepare and analyze the FinQA dataset with proper documentation.

#### Steps:

1. **Open Notebook 01**
   ```bash
   jupyter notebook 01_data_collection_and_preprocessing.ipynb
   ```

2. **Run All Cells** (Shift + Enter on each cell)
   - Environment setup
   - Load FinQA and FinanceBench datasets
   - Data exploration and visualization
   - Prompt formatting
   - Save processed data

3. **Document for Thesis:**

   **Take screenshots of:**
   - Dataset size comparison chart
   - Question/answer length distributions
   - Token length distribution with percentiles
   - Sample formatted prompt

   **Note down statistics:**
   - Total samples: 6,251 (FinQA)
   - Average token length: [from output]
   - Max token length: [from output]
   - Reasoning steps distribution: [from output]

4. **Save Outputs:**
   ```bash
   # Processed data will be saved to:
   ls processed_data/financebench/
   ```

#### Expected Time:
- Vast.ai: 5-10 minutes
- Vast.ai: 3-5 minutes

#### Thesis Section:
Use for **Chapter 3: Methodology → Data Preparation**

---

## Phase 2: Model Training

### Notebook 02: Model Optimization and Training

**Objective:** Fine-tune SLMs with proper experimental controls.

#### Experimental Design

For a complete thesis, run **3 model configurations:**

##### Experiment 1: Baseline (Small Model)
```python
# In notebook cell:
runtime.model_key = "tinyllama-1.1b"
runtime.max_train_samples = 1000  # Quick baseline
runtime.num_train_epochs = 1
runtime.per_device_train_batch_size = 4
runtime.gradient_accumulation_steps = 4
```

##### Experiment 2: Medium Model
```python
runtime.model_key = "qwen2.5-1.5b"
runtime.max_train_samples = 3000  # More data
runtime.num_train_epochs = 2
runtime.per_device_train_batch_size = 4
runtime.gradient_accumulation_steps = 4
```

##### Experiment 3: Production Model (Best Results)
```python
runtime.model_key = "phi3-mini"  # or "mistral-7b" on GPU
runtime.max_train_samples = 6203  # Full dataset
runtime.num_train_epochs = 3
runtime.per_device_train_batch_size = 4
runtime.gradient_accumulation_steps = 4
```

#### Training Checklist:

**Before Training:**
- [ ] Set random seed (already set to 42 in notebook)
- [ ] Document hardware (GPU type, VRAM, backend)
- [ ] Note training start time

**During Training:**
- [ ] Monitor GPU memory usage
- [ ] Watch training loss curve
- [ ] Check for OOM errors (reduce batch size if needed)

**After Training:**
- [ ] Save training loss plot
- [ ] Document final loss value
- [ ] Note training duration
- [ ] Verify model saved to `fingeo-slm-adapter/` or `fingeo-slm-adapter-full/`

#### Training Configurations Table (for thesis):

| Experiment | Model | Params | Samples | Epochs | Batch | Backend | Time | Final Loss |
|------------|-------|--------|---------|--------|-------|---------|------|------------|
| Baseline   | TinyLlama | 1.1B | 1000 | 1 | 4 | CUDA | [fill] | [fill] |
| Medium     | Qwen2.5 | 1.5B | 3000 | 2 | 4 | CUDA | [fill] | [fill] |
| Production | Phi-3 | 3.8B | 6203 | 3 | 4 | CUDA | [fill] | [fill] |

**Fill this table with actual results from your experiments!**

#### Expected Time:
- **TinyLlama (1000 samples, 1 epoch):**
  - Vast.ai M2: ~30-45 minutes
  - RTX 3090: ~10-15 minutes

- **Phi-3 (6203 samples, 3 epochs):**
  - RTX 3090: ~2-3 hours
  - A100: ~1-1.5 hours

#### Save for Thesis:
```bash
# Screenshot/export:
# - Training loss curve
# - Token length distribution
# - Model parameter breakdown
# - Final training logs

# Save model checkpoint info:
ls -lh fingeo-slm-adapter*/
```

#### Thesis Section:
Use for **Chapter 3: Methodology → Model Training** and **Chapter 4: Results → Training Performance**

---

## Phase 3: Evaluation

### Notebook 03: Retrieval Evaluation & Benchmarking

**Objective:** Set up the evaluation pipeline with retrieval, model loading, and initial benchmarks.

#### Evaluation Metrics

Your thesis should report these metrics (all automated in the notebook):

**1. Retrieval Metrics:**
- Recall@K (K=1,3,5)
- Mean Reciprocal Rank (MRR)
- Query-context overlap

**2. Generation Metrics:**
- Semantic accuracy (lexical overlap)
- Faithfulness (binary correctness)
- Exact match rate
- Hallucination rate

**3. Efficiency Metrics:**
- Time to First Token (TTFT)
- Tokens per Second (TPS)
- Peak memory usage
- Latency per query

**4. Ablation Studies:**
- Dense vs. Sparse retrieval
- With/without reranking
- Different chunk sizes
- Different retrieval K values

#### Running Evaluation:

1. **Configure test set size:**
   ```python
   # In notebook 03:
   test_sample_size = 50  # For quick test
   # or
   test_sample_size = 150  # Full FinanceBench (recommended for thesis)
   ```

2. **Run all evaluation cells:**
   - Basic metrics (TTFT, SSoV)
   - Retrieval quality
   - Generation quality
   - Ablation studies

3. **Collect results tables:**
   The notebook generates comparison tables automatically. Copy these for your thesis!

#### Expected Results Template:

**Table: Retrieval Performance**
| Method | Recall@1 | Recall@3 | Recall@5 | MRR |
|--------|----------|----------|----------|-----|
| BM25 (Sparse) | [fill] | [fill] | [fill] | [fill] |
| Dense | [fill] | [fill] | [fill] | [fill] |
| Hybrid | [fill] | [fill] | [fill] | [fill] |

**Table: Generation Performance**
| Model | Accuracy | Exact Match | Hallucination Rate | TTFT (s) | TPS |
|-------|----------|-------------|-------------------|----------|-----|
| TinyLlama | [fill] | [fill] | [fill] | [fill] | [fill] |
| Qwen2.5 | [fill] | [fill] | [fill] | [fill] | [fill] |
| Phi-3 | [fill] | [fill] | [fill] | [fill] | [fill] |

**Table: Ablation Study**
| Configuration | Faithfulness | Recall@5 | Notes |
|---------------|--------------|----------|-------|
| No Reranker | [fill] | [fill] | Baseline |
| With Reranker | [fill] | [fill] | +X% improvement |
| Dense only | [fill] | [fill] | [fill] |
| Sparse only | [fill] | [fill] | [fill] |
| Hybrid | [fill] | [fill] | Best overall |

#### Expected Time:
- 50 samples: 15-20 minutes
- 150 samples: 30-45 minutes

#### Save for Thesis:
- All comparison charts (10+ visualizations)
- Ablation study 2x2 grid
- Efficiency comparison charts
- Results summary table

#### Thesis Section:
Use for **Chapter 4: Results and Analysis**

---

## Phase 4: Ablation Studies

### Additional Experiments (Optional but Recommended)

For a strong thesis, conduct ablation studies by systematically varying:

#### A. Training Data Size
Test how performance scales with data:

```python
# Run notebook 02 with different max_train_samples:
training_sizes = [500, 1000, 2000, 4000, 6203]

for size in training_sizes:
    runtime.max_train_samples = size
    # Train model
    # Evaluate on same test set
    # Record results
```

**Plot:** Performance vs. Training Size curve

#### B. Model Size Comparison
Compare different model architectures:

```python
models = ["tinyllama-1.1b", "qwen2.5-1.5b", "phi3-mini"]

for model_key in models:
    runtime.model_key = model_key
    # Train on same data
    # Evaluate on same test set
    # Compare performance vs. parameter count
```

**Plot:** Accuracy vs. Model Parameters scatter plot

#### C. RAG Configuration
Test different retrieval configurations in notebook 03:

```python
# Test different K values
k_values = [1, 3, 5, 10]

# Test with/without reranking
use_reranker = [True, False]

# Test different retrieval methods
methods = ["sparse", "dense", "hybrid"]
```

**Plot:** Recall@K for different configurations

#### D. Prompt Engineering
Test different prompt formats in notebook 01:

- Chain-of-Thought (current)
- Direct answer only
- Few-shot with examples
- Step-by-step reasoning

Modify the `format_cot_prompt()` function to test variations.

---

## Phase 5: Results Documentation

### Organize Your Results

Create a results directory:

```bash
mkdir -p thesis_results/
mkdir -p thesis_results/figures/
mkdir -p thesis_results/tables/
mkdir -p thesis_results/model_checkpoints/
```

### Save Everything:

#### 1. Figures (from notebooks)
```bash
# Save all plots as high-res PNGs
# Right-click on plots in Jupyter → Save Image
# Or export programmatically in notebooks

# Organize:
thesis_results/figures/
├── 01_data_statistics.png
├── 02_token_distribution.png
├── 03_training_loss_curve.png
├── 04_parameter_breakdown.png
├── 05_retrieval_comparison.png
├── 06_ablation_grid.png
└── 07_efficiency_metrics.png
```

#### 2. Tables (export as CSV)
```python
# In notebooks, add cells to export results:
import pandas as pd

results_df = pd.DataFrame({
    'Model': ['TinyLlama', 'Qwen2.5', 'Phi-3'],
    'Accuracy': [0.65, 0.72, 0.78],
    'TTFT': [1.2, 1.5, 2.1],
    # ... add all metrics
})

results_df.to_csv('thesis_results/tables/model_comparison.csv', index=False)
```

#### 3. Model Checkpoints
```bash
# Copy trained models
cp -r fingeo-slm-adapter-tinyllama thesis_results/model_checkpoints/
cp -r fingeo-slm-adapter-phi3 thesis_results/model_checkpoints/
```

#### 4. Training Logs
```bash
# Copy logs
cp -r fingeo_slm_logs/ thesis_results/training_logs/
```

#### 5. Experimental Configuration
Document your exact setup:

```python
# Save in thesis_results/experiment_config.json
import json

config = {
    "hardware": {
        "platform": "vast.ai",
        "gpu": "RTX 3090",
        "vram": "24GB",
        "cuda_version": "11.8"
    },
    "models": {
        "tinyllama": {
            "id": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            "params": "1.1B",
            "training_samples": 1000,
            "epochs": 1,
            "final_loss": 0.45
        },
        # ... add all models
    },
    "datasets": {
        "train": "FinQA (6203 samples)",
        "eval": "FinanceBench (150 samples)"
    },
    "random_seed": 42,
    "date": "2026-03-26"
}

with open('thesis_results/experiment_config.json', 'w') as f:
    json.dump(config, f, indent=2)
```

---

## 📊 Thesis Writing Tips

### Chapter 3: Methodology

**What to include:**

1. **Dataset Description**
   - FinQA statistics (from notebook 01)
   - Data preprocessing pipeline
   - Train/val/test splits
   - Prompt format examples

2. **Model Architecture**
   - Base models used (TinyLlama, Qwen, Phi-3)
   - Why these models were chosen
   - Parameter counts
   - LoRA/QLoRA configuration (if applicable)

3. **Training Procedure**
   - Optimization algorithm (AdamW)
   - Learning rate (2e-4)
   - Batch size and gradient accumulation
   - Training epochs
   - Hardware setup

4. **Evaluation Metrics**
   - Define each metric (Recall@K, MRR, etc.)
   - Why these metrics are appropriate
   - Test set description

### Chapter 4: Results and Analysis

**What to include:**

1. **Training Results**
   - Loss curves for each model
   - Training time comparison
   - Convergence analysis

2. **Performance Comparison**
   - All evaluation metrics in tables
   - Model comparison across all dimensions
   - Statistical significance tests (if applicable)

3. **Ablation Studies**
   - Impact of training data size
   - Impact of model size
   - Impact of RAG configuration
   - Impact of prompt format

4. **Error Analysis**
   - Examples of successful predictions
   - Examples of failures
   - Common error patterns
   - Qualitative analysis

### Chapter 5: Discussion

**What to discuss:**

1. **Key Findings**
   - Which model performed best and why
   - Trade-offs (accuracy vs. speed vs. memory)
   - Surprising results

2. **Limitations**
   - Hardware constraints (if using Vast.ai for some experiments)
   - Dataset limitations
   - Model limitations

3. **Future Work**
   - Larger models (13B, 70B)
   - More training data
   - Advanced RAG techniques
   - Multi-modal inputs

---

## 🔬 Reproducibility Checklist

For strong academic work, ensure:

- [ ] Random seed is fixed (seed=42 in notebooks)
- [ ] All hyperparameters are documented
- [ ] Dataset versions are specified
- [ ] Hardware specifications are recorded
- [ ] Training time is measured
- [ ] Code is version-controlled (git commit hash)
- [ ] Results can be reproduced by others

### Create Reproducibility Documentation:

```bash
# Create reproducibility.md
cat > thesis_results/REPRODUCIBILITY.md << 'EOF'
# Reproducibility Information

## Environment
- Python: 3.9+
- PyTorch: 2.0+
- Transformers: 4.40+
- Hardware: [specify]

## Exact Steps to Reproduce

1. Clone repository: `git clone <url>`
2. Checkout commit: `git checkout <commit-hash>`
3. Install dependencies: `pip install -r requirements.txt`
4. Run notebook 01: `jupyter notebook 01_data_collection_and_preprocessing.ipynb`
5. Run notebook 02 with config: [specify exact cell configurations]
6. Run notebook 03 (`03_retrieval_evaluation.ipynb`): [specify test set size]
7. Run notebook 04 (`04_model_comparison_and_ablation.ipynb`): [specify ablation configurations]

## Random Seeds
- Global seed: 42
- Train/val split: seed=42

## Data Versions
- FinQA: [specify version/commit]
- FinanceBench: [specify version/commit]

## Expected Results
- Model X accuracy: 0.78 ± 0.02
- Training time: ~2 hours ± 15 min on RTX 3090

EOF
```

---

## 📅 Recommended Timeline

### Week 1: Setup and Exploration
- [ ] Day 1-2: Environment setup
- [ ] Day 3-4: Run notebook 01, understand data
- [ ] Day 5-7: Initial training experiments on small model

### Week 2: Full-Scale Training
- [ ] Day 1-3: Train baseline model (TinyLlama)
- [ ] Day 4-5: Train medium model (Qwen2.5)
- [ ] Day 6-7: Train production model (Phi-3/Mistral)

### Week 3: Evaluation and Ablations
- [ ] Day 1-2: Run retrieval evaluation (notebook 03) and model comparison/ablations (notebook 04)
- [ ] Day 3-5: Additional ablation studies (data size, model size)
- [ ] Day 6-7: RAG configuration experiments

### Week 4: Analysis and Documentation
- [ ] Day 1-2: Organize all results
- [ ] Day 3-4: Create figures and tables
- [ ] Day 5-7: Write methodology and results chapters

---

## 🎯 Quick Start Checklist

Ready to start? Follow this checklist:

**Step 1: Setup (30 min)**
- [ ] Clone repository
- [ ] Run `./setup.sh`
- [ ] Verify environment
- [ ] Open Jupyter

**Step 2: Data Preparation (1 hour)**
- [ ] Run notebook 01 completely
- [ ] Save all visualization screenshots
- [ ] Note down statistics
- [ ] Verify processed_data/ created

**Step 3: First Training Run (2-3 hours)**
- [ ] Open notebook 02
- [ ] Configure for TinyLlama baseline
- [ ] Run training
- [ ] Save loss curve
- [ ] Document results

**Step 4: First Evaluation (1 hour)**
- [ ] Open notebook 03 (`03_retrieval_evaluation.ipynb`)
- [ ] Run on 50 test samples
- [ ] Review all metrics
- [ ] Save comparison charts

**Step 4b: Model Comparison & Ablation (1 hour)**
- [ ] Open notebook 04 (`04_model_comparison_and_ablation.ipynb`)
- [ ] Run comparative evaluation
- [ ] Review ablation study results
- [ ] Save dashboard visualizations

**Step 5: Plan Full Experiments (planning)**
- [ ] Decide on model configurations
- [ ] Plan ablation studies
- [ ] Create experiment tracking spreadsheet
- [ ] Set up thesis_results/ directory

---

## 💡 Pro Tips for Thesis Success

1. **Start Small, Scale Up**
   - Test on Vast.ai with small samples first
   - Move to cloud GPU for final experiments
   - This saves money and debugging time

2. **Document Everything**
   - Keep a lab notebook (markdown file)
   - Screenshot every important result
   - Save all intermediate results

3. **Version Control Your Experiments**
   ```bash
   git commit -m "Baseline experiment: TinyLlama 1000 samples"
   git tag exp-baseline-v1
   ```

4. **Compare Against Baselines**
   - Include a "no fine-tuning" baseline (0-shot)
   - Compare against published FinQA results
   - Show incremental improvements

5. **Error Analysis is Key**
   - Don't just report numbers
   - Show examples of what works/fails
   - Explain why certain approaches work better

6. **Prepare for Questions**
   - Document why you made each choice
   - Be ready to explain hyperparameters
   - Keep detailed notes on experiment decisions

---

## 📚 Additional Resources

### Related Papers to Cite
- FinQA paper: Chen et al. (2021)
- LoRA: Hu et al. (2021)
- QLoRA: Dettmers et al. (2023)
- RAG: Lewis et al. (2020)
- GEO: Chen et al. (2025)
- Sentence-BERT: Reimers and Gurevych (2019)

### Useful Tools
- TensorBoard: Monitor training in real-time
- WandB: Experiment tracking (optional)
- Jupyter nbconvert: Export notebooks to PDF/HTML

---

## 🔄 Thesis Alignment

**IMPORTANT**: Before submitting your thesis, review `THESIS_CHANGES.md` for:
- Required text updates to match actual implementation
- Clarifications on algorithm descriptions
- Results tables that need to be filled in

### Key Implementation Details for Thesis

| Thesis Claim | Actual Implementation |
|--------------|----------------------|
| FAISS+BM25 ensemble | ✅ Implemented in Notebook 03 |
| Cross-encoder reranking | ⚠️ Uses lexical overlap (not neural cross-encoder) |
| OCR/2D layout parsing | ⚠️ Uses JSON-to-Markdown (not spatial parsing) |
| GEO visibility metrics | ✅ SSoV, mention frequency implemented |
| Numerical hallucination | ✅ Implemented in Notebook 03 |
| Memory profiling | ✅ MemoryProfiler class added |

---

## ❓ FAQ

**Q: How many experiments do I need for a thesis?**
A: Minimum 3 model configurations + 2-3 ablation studies. More is better!

**Q: What if training fails on Vast.ai?**
A: Reduce batch size to 1, reduce samples to 100-200, or use cloud GPU.

**Q: How do I know if results are significant?**
A: Run multiple seeds (42, 43, 44) and report mean ± std deviation.

**Q: Can I use these results in my thesis?**
A: Yes! This is a proper ML pipeline. Just document everything properly.

**Q: How long for a complete thesis experiment suite?**
A: 2-4 weeks for full training + evaluation + ablations + documentation.

---

## 📞 Getting Help

If you run into issues:

1. Check CHANGELOG.md for recent changes
2. Review inline notebook documentation
3. Check error messages in training logs
4. Verify hardware compatibility (GPU)
5. Test with smaller configurations first

---

**Good luck with your thesis! 🎓**

Remember: Systematic experiments + clear documentation = strong thesis results!
