from typing import Dict, List, Optional, Tuple

import torch
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

from .config import MODEL_PRESETS


def resolve_model_id(model_key_or_id: str) -> str:
    return MODEL_PRESETS.get(model_key_or_id, model_key_or_id)


def load_tokenizer(model_id: str):
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"
    return tokenizer


def _default_lora_targets(model) -> List[str]:
    candidates = ["q_proj", "k_proj", "v_proj", "o_proj"]
    names = set()
    for name, _ in model.named_modules():
        for c in candidates:
            if name.endswith(c):
                names.add(c)
    return sorted(names) if names else ["q_proj", "k_proj", "v_proj", "o_proj"]


def _quant_config_for_cuda() -> BitsAndBytesConfig:
    compute_dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    return BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=compute_dtype,
    )


def load_model_for_training(
    model_id: str,
    backend: str,
    use_qlora: bool,
    lora_r: int,
    lora_alpha: int,
    lora_dropout: float,
) -> Tuple[object, Dict[str, object]]:
    info: Dict[str, object] = {
        "backend": backend,
        "model_id": model_id,
        "qlora_enabled": False,
        "lora_enabled": False,
        "quantization": "none",
        "notes": [],
    }

    if backend == "cuda" and use_qlora:
        quant_config: Optional[BitsAndBytesConfig] = _quant_config_for_cuda()
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            quantization_config=quant_config,
            device_map="auto",
            trust_remote_code=False,
            attn_implementation="eager",
        )
        model = prepare_model_for_kbit_training(model)
        targets = _default_lora_targets(model)
        lora_config = LoraConfig(
            r=lora_r,
            lora_alpha=lora_alpha,
            target_modules=targets,
            lora_dropout=lora_dropout,
            bias="none",
            task_type="CAUSAL_LM",
        )
        model = get_peft_model(model, lora_config)
        info["qlora_enabled"] = True
        info["lora_enabled"] = True
        info["quantization"] = "4bit-nf4"
        info["lora_targets"] = targets
        return model, info

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="auto" if backend != "cpu" else None,
        trust_remote_code=False,
        attn_implementation="eager",
    )

    if backend == "mps":
        info["notes"].append("QLoRA/4-bit bitsandbytes is CUDA-only. Running full precision on Apple Silicon.")
    elif backend == "cpu":
        info["notes"].append("QLoRA/4-bit bitsandbytes is CUDA-only. Running full precision on CPU.")

    return model, info
