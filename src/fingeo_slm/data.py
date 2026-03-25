from typing import Tuple

from datasets import Dataset, DatasetDict, load_from_disk


def load_training_data(
    dataset_path: str,
    text_field: str,
    max_samples: int = 5000,
    split_preference: str = "train",
) -> Tuple[Dataset, Dataset]:
    dataset = load_from_disk(dataset_path)

    if isinstance(dataset, DatasetDict):
        if split_preference in dataset:
            train_dataset = dataset[split_preference]
        else:
            first_split = list(dataset.keys())[0]
            train_dataset = dataset[first_split]
    else:
        train_dataset = dataset

    if text_field not in train_dataset.column_names:
        raise KeyError(f"Expected column '{text_field}' in dataset columns={train_dataset.column_names}")

    cleaned = train_dataset.filter(lambda ex: isinstance(ex[text_field], str) and len(ex[text_field].strip()) > 0)

    # Remove exact duplicate prompts to avoid leakage-like overfitting effects.
    seen = set()
    keep_indices = []
    for idx, text in enumerate(cleaned[text_field]):
        if text not in seen:
            seen.add(text)
            keep_indices.append(idx)
    unique = cleaned.select(keep_indices)

    if len(unique) == 0:
        raise ValueError("No valid training rows after filtering empty and duplicate prompts")

    subset = unique.select(range(min(max_samples, len(unique))))
    return unique, subset
