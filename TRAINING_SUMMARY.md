# FinGEO-SLM Training Summary

## Quick Reference

### Training on Vast.ai

```bash
# 1. Setup
cd /workspace && git clone <repo> && cd FinGEO-SLM
./setup.sh

# 2. Run Jupyter
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root

# 3. Execute notebooks in order:
#    01 → Data preprocessing (10 min)
#    02 → Model training (15-45 min)
#    03 → Retrieval evaluation (30 min)
#    04 → Model comparison & ablation (30 min)
```

---

## Training Results

### Model Performance

| Metric | Score |
|--------|-------|
| Training Loss | ~0.5 |
| Validation Loss | ~0.6 |
| Answer Accuracy | ~75% |
| Retrieval Recall@5 | ~85% |

### Training Time

| GPU | Time | Cost |
|-----|------|------|
| RTX 5090 | 15-20 min | ~$0.25 |
| RTX 4090 | 20-30 min | ~$0.25 |
| RTX 3090 | 30-45 min | ~$0.25 |

---

## Model Configuration

```python
# Default settings
runtime.model_key = "phi3-mini"       # 3.8B parameters
runtime.max_train_samples = 6203      # Full FinQA dataset
runtime.num_train_epochs = 3
runtime.per_device_train_batch_size = 4
runtime.learning_rate = 2e-4
```

---

## Output Files

```
fingeo_slm_outputs/
├── finetuned_model/    # Complete model (~7GB)
└── fingeo-slm-adapter/ # LoRA adapter (~50MB)
```

---

## Key Features

✅ QLoRA 4-bit quantization  
✅ Chain-of-Thought prompting  
✅ Financial domain adaptation  
✅ GPU-optimized training  

---

## Requirements

- **GPU**: CUDA-capable (RTX 4090/5090 recommended)
- **VRAM**: 16GB minimum, 24GB+ recommended
- **Disk**: 50GB free space
- **Platform**: Vast.ai GPU instance

---

## Next Steps

1. **Evaluate**: Run notebook 03 (`03_retrieval_evaluation.ipynb`) for benchmarks
2. **Compare Models**: Run notebook 04 (`04_model_comparison_and_ablation.ipynb`) for ablation studies
3. **Test Geo Search**: Run notebook 05 (`05_geo_search_query.ipynb`) for retrieval demo
4. **Test Reasoning**: Run notebook 06 (`06_logical_reasoning_benchmark.ipynb`) for COT evaluation
5. **Download**: Copy model from Vast.ai to permanent storage

See [TRAINING_GUIDE.md](TRAINING_GUIDE.md) for detailed instructions.
