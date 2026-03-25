from dataclasses import dataclass
from typing import Dict


MODEL_PRESETS: Dict[str, str] = {
    "phi3-mini": "microsoft/Phi-3-mini-4k-instruct",
    "qwen2.5-1.5b": "Qwen/Qwen2.5-1.5B-Instruct",
    "tinyllama-1.1b": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    "mistral-7b": "mistralai/Mistral-7B-Instruct-v0.3",
}


@dataclass
class RuntimeConfig:
    model_key: str = "phi3-mini"
    dataset_path: str = "processed_data/finqa_cot"
    text_field: str = "formatted_prompt"
    output_dir: str = "fingeo_slm_outputs"
    log_dir: str = "fingeo_slm_logs"
    adapter_dir: str = "fingeo-slm-adapter"
    max_train_samples: int = 5000
    max_seq_length: int = 2048
    use_wandb: bool = False
    use_tensorboard: bool = True
    use_qlora: bool = True
    lora_r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05
