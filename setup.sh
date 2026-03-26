#!/bin/bash
# FinGEO-SLM Setup Script
# This script sets up the environment for running FinGEO-SLM on your local machine

set -e

echo "🚀 FinGEO-SLM Setup Script"
echo "=========================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Found Python $python_version"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip -q
echo "✓ pip upgraded"
echo ""

# Install PyTorch (platform-specific)
echo "Installing PyTorch..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "Detected macOS - installing PyTorch with MPS support"
    pip install torch torchvision torchaudio -q
else
    # Linux (assume CUDA available)
    echo "Detected Linux - installing PyTorch with CUDA support"
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 -q
fi
echo "✓ PyTorch installed"
echo ""

# Install other dependencies
echo "Installing project dependencies..."
pip install -r requirements.txt -q
echo "✓ Dependencies installed"
echo ""

# Install Jupyter kernel
echo "Setting up Jupyter kernel..."
pip install ipykernel -q
python -m ipykernel install --user --name=fingeo-slm --display-name "FinGEO-SLM" 2>/dev/null || true
echo "✓ Jupyter kernel installed"
echo ""

# Verify CUDA/MPS availability
echo "Checking compute backend..."
python -c "
import torch
if torch.cuda.is_available():
    print('✓ CUDA available:', torch.cuda.get_device_name(0))
    print('  -> QLoRA (4-bit) training enabled')
elif torch.backends.mps.is_available():
    print('✓ MPS (Apple Silicon) available')
    print('  -> Full-precision training only (QLoRA not supported)')
else:
    print('⚠ Only CPU available (training will be slow)')
"
echo ""

# Create necessary directories
echo "Creating output directories..."
mkdir -p processed_data
mkdir -p fingeo_slm_logs
mkdir -p fingeo_slm_outputs
echo "✓ Directories created"
echo ""

# Summary
echo "=========================="
echo "✅ Setup Complete!"
echo "=========================="
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Start Jupyter: jupyter notebook"
echo "3. Open and run notebooks in order:"
echo "   - 01_data_collection_and_preprocessing.ipynb"
echo "   - 02_model_optimization_and_training.ipynb"
echo "   - 03_evaluation_and_benchmarking.ipynb"
echo ""
echo "📚 Documentation:"
echo "   - Local setup: SETUP_LOCAL.md"
echo "   - Vast.ai setup: SETUP_VASTAI.md"
echo "   - Main README: README.md"
echo ""
