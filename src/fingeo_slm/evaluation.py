import re
import time
from typing import Dict, List, Tuple

import numpy as np


def lexical_overlap_score(query: str, text: str) -> float:
    q = set(re.findall(r"[A-Za-z0-9$.]+", query.lower()))
    t = set(re.findall(r"[A-Za-z0-9$.]+", text.lower()))
    if not q:
        return 0.0
    return len(q & t) / len(q)


def char_ngram_jaccard(query: str, text: str, n: int = 3) -> float:
    def grams(s: str) -> set:
        s = re.sub(r"\s+", " ", s.lower()).strip()
        if len(s) < n:
            return {s}
        return {s[i : i + n] for i in range(len(s) - n + 1)}

    qg, tg = grams(query), grams(text)
    denom = max(1, len(qg | tg))
    return len(qg & tg) / denom


def rerank_chunks(query: str, chunks: List[str]) -> Tuple[List[str], List[Tuple[str, float]]]:
    scored = [(chunk, lexical_overlap_score(query, chunk)) for chunk in chunks]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [chunk for chunk, _ in scored], scored


def retrieval_metrics(cases: List[Dict], retrieval_fn, rerank: bool = True, top_n: int = 6) -> Dict[str, float]:
    k_values = [1, 3, 5]
    recall_hits = {k: 0 for k in k_values}
    reciprocal_ranks = []
    noise_reduction = []

    for case in cases:
        raw = retrieval_fn(case["query"], top_n=top_n)
        ranked = raw
        if rerank:
            ranked, _ = rerank_chunks(case["query"], raw)

        for k in k_values:
            if case["gold_chunk"] in ranked[:k]:
                recall_hits[k] += 1

        rr = 0.0
        for i, chunk in enumerate(ranked, start=1):
            if chunk == case["gold_chunk"]:
                rr = 1.0 / i
                break
        reciprocal_ranks.append(rr)

        raw_irrelevant = sum(1 for chunk in raw if chunk != case["gold_chunk"])
        ranked_irrelevant = sum(1 for chunk in ranked if chunk != case["gold_chunk"])
        if raw_irrelevant > 0:
            noise_reduction.append((raw_irrelevant - ranked_irrelevant) / raw_irrelevant)
        else:
            noise_reduction.append(0.0)

    n = max(1, len(cases))
    return {
        "Recall@1": recall_hits[1] / n,
        "Recall@3": recall_hits[3] / n,
        "Recall@5": recall_hits[5] / n,
        "MRR": float(np.mean(reciprocal_ranks)) if reciprocal_ranks else 0.0,
        "NoiseReduction": float(np.mean(noise_reduction)) if noise_reduction else 0.0,
    }


_number_pattern = re.compile(r"\$\d+(?:\.\d+)?\s*Billion", flags=re.IGNORECASE)


def extract_first_number(text: str):
    m = _number_pattern.search(text)
    return m.group(0).strip().lower() if m else None


def faithfulness_binary(answer: str, context: str) -> int:
    ans_num = extract_first_number(answer)
    if not ans_num:
        return 0
    return int(ans_num in context.lower())


def timed_generation_metrics(answer: str, call_duration_ms: float) -> Dict[str, float]:
    token_count = max(1, len(answer.split()))
    throughput_tps = token_count / max(1e-6, call_duration_ms / 1000.0)
    return {
        "latency_ms": call_duration_ms,
        "throughput_tps": throughput_tps,
    }


def peak_memory_mb() -> float:
    try:
        import torch

        if torch.cuda.is_available():
            return torch.cuda.max_memory_allocated() / (1024 ** 2)
        if hasattr(torch.backends, "mps") and torch.backends.mps.is_available() and hasattr(torch.mps, "current_allocated_memory"):
            return torch.mps.current_allocated_memory() / (1024 ** 2)
    except Exception:
        pass
    return np.nan


def time_call(fn, *args, **kwargs):
    t0 = time.perf_counter()
    result = fn(*args, **kwargs)
    ms = (time.perf_counter() - t0) * 1000.0
    return result, ms
