import torch
from trl import SFTConfig


def choose_optimizer(backend: str, qlora_enabled: bool) -> str:
    if backend == "cuda" and qlora_enabled:
        return "paged_adamw_32bit"
    return "adamw_torch"


def build_sft_config(
    output_dir: str,
    log_dir: str,
    report_to: str,
    backend: str,
    qlora_enabled: bool,
    max_seq_length: int,
) -> SFTConfig:
    bf16 = backend == "cuda" and torch.cuda.is_bf16_supported()
    fp16 = backend == "cuda" and not bf16

    return SFTConfig(
        output_dir=output_dir,
        per_device_train_batch_size=1 if backend != "cuda" else 2,
        gradient_accumulation_steps=8 if backend != "cuda" else 4,
        optim=choose_optimizer(backend, qlora_enabled),
        learning_rate=2e-4,
        logging_steps=10,
        num_train_epochs=1,
        bf16=bf16,
        fp16=fp16,
        report_to=report_to,
        logging_dir=log_dir,
        save_strategy="no",
        dataset_text_field="formatted_prompt",
        max_length=max_seq_length,
        packing=False,
    )
