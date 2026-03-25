"""FinGEO-SLM core utilities for thesis-grade training and evaluation pipelines."""

from .config import MODEL_PRESETS, RuntimeConfig
from .platform import detect_backend
from .data import load_training_data
from .modeling import load_tokenizer, load_model_for_training, resolve_model_id
from .training import build_sft_config, choose_optimizer
from .evaluation import (
    lexical_overlap_score,
    char_ngram_jaccard,
    rerank_chunks,
    retrieval_metrics,
    extract_first_number,
    faithfulness_binary,
    timed_generation_metrics,
    peak_memory_mb,
    time_call,
)

__all__ = [
    "MODEL_PRESETS",
    "RuntimeConfig",
    "detect_backend",
    "load_training_data",
    "load_tokenizer",
    "load_model_for_training",
    "resolve_model_id",
    "build_sft_config",
    "choose_optimizer",
    "lexical_overlap_score",
    "char_ngram_jaccard",
    "rerank_chunks",
    "retrieval_metrics",
    "extract_first_number",
    "faithfulness_binary",
    "timed_generation_metrics",
    "peak_memory_mb",
    "time_call",
]
