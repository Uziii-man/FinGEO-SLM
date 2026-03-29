# Quick Start Guide - Google Colab

## Overview
All 4 notebooks now have automatic Google Drive integration. Just open and run - everything is automatic!

## First Time Setup (5 minutes)

### Step 1: Upload Notebooks to Colab
1. Go to https://colab.research.google.com
2. Click File → Upload notebook
3. Upload all 4 notebooks:
   - `01_data_collection_and_preprocessing.ipynb`
   - `02_model_optimization_and_training.ipynb`
   - `03_evaluation_and_benchmarking.ipynb`
   - `04_geo_search_query.ipynb`

### Step 2: Run Notebook 01 (Data Preprocessing)
1. Open `01_data_collection_and_preprocessing.ipynb`
2. Click Runtime → Run all
3. When prompted, authorize Google Drive access
4. Wait for preprocessing to complete
5. Data will automatically save to your Google Drive

**Expected time**: 5-10 minutes

### Step 3: Run Notebook 02 (Training)
1. Open `02_model_optimization_and_training.ipynb`
2. Click Runtime → Run all
3. Drive will auto-mount (no authorization needed)
4. processed_data will auto-load from Drive
5. Model will auto-save to Drive after training

**Expected time**: 20-60 minutes (depending on GPU)

### Step 4: Run Notebook 03 (Evaluation)
1. Open `03_evaluation_and_benchmarking.ipynb`
2. Click Runtime → Run all
3. Data and models will auto-load from Drive
4. Results will auto-save to Drive

**Expected time**: 10-20 minutes

### Step 5: Run Notebook 04 (RAG Demo)
1. Open `04_geo_search_query.ipynb`
2. Click Runtime → Run all
3. PDFs will auto-load from Drive if available

**Expected time**: 2-5 minutes

## What Happens Automatically

### Notebook 01
- ✓ Mounts Google Drive
- ✓ Processes FinQA data
- ✓ Saves to local workspace
- ✓ **Copies to Drive** → `/MyDrive/FinGEO-SLM/processed_data/`

### Notebook 02
- ✓ Mounts Google Drive
- ✓ **Loads data from Drive** if not found locally
- ✓ Trains model
- ✓ **Saves model to Drive** → `/MyDrive/FinGEO-SLM/models/`
- ✓ **Saves logs to Drive** → `/MyDrive/FinGEO-SLM/logs/`

### Notebook 03
- ✓ Mounts Google Drive
- ✓ **Loads data from Drive** if needed
- ✓ **Loads models from Drive** if available
- ✓ Runs evaluation
- ✓ **Saves results to Drive** → `/MyDrive/FinGEO-SLM/results/`

### Notebook 04
- ✓ Mounts Google Drive
- ✓ **Loads PDFs from Drive** if available
- ✓ Runs search queries

## Your Google Drive Structure

After running all notebooks, your Drive will look like this:

```
Google Drive/
└── MyDrive/
    └── FinGEO-SLM/
        ├── processed_data/
        │   └── finqa_cot/         (from Notebook 01)
        ├── models/
        │   ├── phi3-mini/         (from Notebook 02)
        │   ├── qwen2_5-1_5b/
        │   └── tinyllama-1_1b/
        ├── results/
        │   ├── evaluation_results_latest.json  (from Notebook 03)
        │   └── generation_details_*.json
        └── logs/
            └── phi3-mini/         (training logs)
```

## Benefits

1. **Session Persistence**: Your data survives Colab disconnects
2. **Resume Training**: Start where you left off
3. **Share Models**: Trained models available across notebooks
4. **No Manual Steps**: Everything is automatic
5. **Zero Configuration**: Just run cells in order

## Troubleshooting

### "Drive mounting failed"
**Solution**: Click the link when prompted to authorize Drive access

### "processed_data not found"
**Solution**: Run Notebook 01 first to create the data

### "Disk space full"
**Solution**: Check your Google Drive storage (free tier = 15GB)

### "Runtime disconnected"
**Solution**: Just reconnect and re-run - your data is safe in Drive!

## Pro Tips

### 💡 Use GPU Runtime
1. Click Runtime → Change runtime type
2. Select "T4 GPU" or "A100 GPU"
3. This speeds up training significantly

### 💡 Keep Drive Mounted
Don't disconnect from Colab unnecessarily - keeping the session alive maintains the Drive mount

### 💡 Monitor Progress
Watch the output - emoji indicators show what's happening:
- 📁 = Mounting Drive
- 📥 = Loading from Drive
- 📤 = Saving to Drive
- ✓ = Success
- ⚠ = Warning (not critical)
- ❌ = Error (needs attention)

### 💡 Resume After Disconnect
If Colab disconnects during training:
1. Reconnect to runtime
2. Re-run the notebook
3. Partial progress may be available in Drive

### 💡 Compare Runs
Evaluation results are timestamped in Drive:
- `evaluation_results_20260330_123456.json`
- Compare different model configurations
- Track improvements over time

## Advanced: Accessing Results

### From Python (in Colab)
```python
import json
from pathlib import Path

# Load latest evaluation results
results_file = Path('/content/drive/MyDrive/FinGEO-SLM/results/evaluation_results_latest.json')
with open(results_file) as f:
    results = json.load(f)

print(f"Best retrieval: {results['retrieval_ablation']}")
print(f"Average SSoV: {results['generation_metrics']['with_reranker']['SSoV']}")
```

### Download to Your Computer
1. Open Google Drive in your browser
2. Navigate to MyDrive/FinGEO-SLM
3. Right-click any folder → Download
4. Use for thesis analysis, presentations, etc.

## Need Help?

Check these files in your local repository:
- `DRIVE_INTEGRATION_SUMMARY.md` - Complete technical details
- `CELL_ADDITIONS_DETAIL.md` - Exact cells added to each notebook

## Running Locally?

No problem! The notebooks automatically detect when NOT on Colab:
- Drive operations are skipped
- Everything uses local files
- No changes to your workflow
- Same results, different storage location

Happy training! 🚀
