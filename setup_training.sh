#!/bin/bash

# Quick Training Setup Script for Vast.ai/Google Colab
# Run this after uploading to cloud GPU instance

set -e  # Exit on error

echo "============================================"
echo "FinGEO-SLM Training Setup"
echo "============================================"

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Run this from the FinGEO-SLM directory"
    exit 1
fi

echo ""
echo "Step 1: Checking GPU..."
if command -v nvidia-smi &> /dev/null; then
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
    echo "✓ GPU detected"
else
    echo "⚠️  No GPU detected - training will be VERY slow"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "Step 2: Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

echo ""
echo "Step 3: Checking data..."
if [ -d "processed_data" ] && [ -d "data" ]; then
    echo "✓ Data directories found"
else
    echo "⚠️  Data directories missing - training may fail"
fi

echo ""
echo "Step 4: Creating output directories..."
mkdir -p fingeo_slm_outputs
mkdir -p fingeo_slm_logs
echo "✓ Output directories ready"

echo ""
echo "============================================"
echo "Setup Complete! Ready to train."
echo "============================================"
echo ""
echo "To start training:"
echo "  Option A: Open Jupyter and run notebook 2"
echo "    jupyter notebook --allow-root --no-browser"
echo ""
echo "  Option B: Execute notebook from command line"
echo "    jupyter nbconvert --to notebook --execute 02_model_optimization_and_training.ipynb"
echo ""
echo "Expected training time: 2-4 hours on GPU"
echo "============================================"
