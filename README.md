# FinGEO-SLM

FinGEO-SLM is a thesis-oriented financial RAG and fine-tuning project with a modular training stack, dataset validation, and benchmark-ready evaluation pipeline.

## Project Layout

- 01_data_collection_and_preprocessing.ipynb: raw data ingestion and prompt construction.
- 02_model_optimization_and_training.ipynb: model loading, backend-aware QLoRA/full-precision training, and diagnostics.
- 03_evaluation_and_benchmarking.ipynb: retrieval, generation, hardware, and ablation benchmarks.
- 04_geo_search_query.ipynb: document-level search and retrieval demonstrations.
- src/fingeo_slm/: reusable production-style modules for config, data, modeling, training, and evaluation.
- configs/experiment.example.json: runtime configuration template.

## Thesis-Standard Refactor

The codebase now follows an industry-style modular split:

- src/fingeo_slm/config.py:
	- RuntimeConfig dataclass
	- model preset registry (small SLMs and 7B baseline)
- src/fingeo_slm/data.py:
	- robust dataset loading from disk
	- empty-prompt filtering
	- duplicate-prompt removal to reduce leakage-like repetition
- src/fingeo_slm/modeling.py:
	- backend detection-aware model loading
	- conditional 4-bit QLoRA activation on CUDA
	- LoRA target discovery and adapter injection
- src/fingeo_slm/training.py:
	- backend-safe optimizer and precision configuration
- src/fingeo_slm/evaluation.py:
	- retrieval metrics (Recall@K, MRR, Noise Reduction)
	- faithfulness and exact-match helpers
	- timing and memory helpers

## Extended Benchmarking and Evaluation

03_evaluation_and_benchmarking.ipynb includes four benchmark phases backed by FinQA test data:

### 1. Retrieval Performance Metrics

- Recall@1, Recall@3, Recall@5: checks whether the ground-truth chunk appears in the top K retrieved chunks.
- Mean Reciprocal Rank (MRR): measures how high the first relevant chunk is ranked.
- Information Noise Reduction: estimates how much irrelevant context is removed by reranking.

### 2. Generative Accuracy and Fidelity

- Semantic Share-of-Voice (SSoV): detects whether target entities are surfaced in generated answers.
- Hallucination Rate / Faithfulness proxy: binary check that generated numeric claims are present in retrieved context.
- Numerical Exact Match (EM): verifies extracted financial values against ground truth.

### 3. Hardware and Edge Efficiency

- Time-to-First-Token (TTFT) in milliseconds.
- Total inference latency per query.
- Generation throughput in tokens per second.
- Peak memory utilization (CUDA or MPS if available).

### 4. Ablation Studies

- Dense vs Sparse vs Hybrid retrieval comparison.
- No-reranker vs Cross-Encoder reranking effect.
- Base SLM proxy vs CoT fine-tuned proxy comparison.
- SLM vs 7B baseline comparison hook (activate model generation mode for real inference).

## Model Selection and Switching

You can switch models by setting runtime.model_key in 02_model_optimization_and_training.ipynb and ACTIVE_SLM_KEY in 03_evaluation_and_benchmarking.ipynb.

Built-in presets:

- phi3-mini -> microsoft/Phi-3-mini-4k-instruct
- qwen2.5-1.5b -> Qwen/Qwen2.5-1.5B-Instruct
- tinyllama-1.1b -> TinyLlama/TinyLlama-1.1B-Chat-v1.0
- mistral-7b -> mistralai/Mistral-7B-Instruct-v0.3

You can also pass a direct Hugging Face model ID instead of a preset.

## Why QLoRA/4-bit Did Not Work on MacBook

Root cause:

- bitsandbytes 4-bit kernels are CUDA-only.
- Apple Silicon (MPS) does not support bitsandbytes QLoRA path.
- The old notebook used a CUDA-only optimizer (paged_adamw_32bit) even on non-CUDA devices.

Fixes applied:

- Automatic backend detection (cuda/mps/cpu).
- QLoRA enabled only on CUDA.
- On MPS/CPU: automatic full-precision fallback and AdamW torch optimizer.
- Explicit runtime logs show whether QLoRA is active.

Practical guidance:

- For real QLoRA thesis experiments: run on NVIDIA CUDA hardware.
- For MacBook development/debug: use smaller SLM presets (tinyllama-1.1b or qwen2.5-1.5b) and reduced sample size.

## Dataset Quality and Training Data Issue

The training path now validates and cleans dataset rows before training:

- confirms required text column exists
- removes empty prompts
- removes exact duplicate prompts
- creates explicit train/eval split for better scientific reporting

This addresses common data quality issues that degrade training stability and overstate metrics.

## Running the benchmark notebook

1. Open 03_evaluation_and_benchmarking.ipynb.
2. Run cells top to bottom.
3. Set ACTIVE_SLM_KEY and optionally BASELINE_7B_KEY.
4. Set ENABLE_MODEL_GENERATION = True to run real model-based ablations.
5. For strict hardware profiling, wrap memory tracking around your full inference call.

## Running training notebook

1. Open 02_model_optimization_and_training.ipynb.
2. Select runtime.model_key and runtime.max_train_samples.
3. Run all cells.
4. Check runtime logs for backend mode:
	- CUDA: 4-bit QLoRA + LoRA adapters
	- MPS/CPU: full precision fallback
5. Saved artifacts:
	- LoRA path: fingeo-slm-adapter
	- Full precision fallback path: fingeo-slm-adapter-full