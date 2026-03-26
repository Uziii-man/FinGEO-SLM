@echo off
REM FinGEO-SLM Setup Script for Windows
REM This script sets up the environment for running FinGEO-SLM on Windows

echo ================================
echo FinGEO-SLM Setup Script (Windows)
echo ================================
echo.

REM Check Python version
echo Checking Python version...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python 3.9 or higher.
    pause
    exit /b 1
)
echo.

REM Create virtual environment
echo Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip -q
echo pip upgraded
echo.

REM Install PyTorch for Windows
echo Installing PyTorch...
echo Detected Windows - installing PyTorch with CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 -q
echo PyTorch installed
echo.

REM Install other dependencies
echo Installing project dependencies...
pip install -r requirements.txt -q
echo Dependencies installed
echo.

REM Install Jupyter kernel
echo Setting up Jupyter kernel...
pip install ipykernel -q
python -m ipykernel install --user --name=fingeo-slm --display-name "FinGEO-SLM"
echo Jupyter kernel installed
echo.

REM Verify CUDA availability
echo Checking compute backend...
python -c "import torch; print('CUDA available:', torch.cuda.is_available()); print('Device:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
echo.

REM Create necessary directories
echo Creating output directories...
if not exist "processed_data" mkdir processed_data
if not exist "fingeo_slm_logs" mkdir fingeo_slm_logs
if not exist "fingeo_slm_outputs" mkdir fingeo_slm_outputs
echo Directories created
echo.

REM Summary
echo ================================
echo Setup Complete!
echo ================================
echo.
echo Next steps:
echo 1. Activate the virtual environment: venv\Scripts\activate.bat
echo 2. Start Jupyter: jupyter notebook
echo 3. Open and run notebooks in order:
echo    - 01_data_collection_and_preprocessing.ipynb
echo    - 02_model_optimization_and_training.ipynb
echo    - 03_evaluation_and_benchmarking.ipynb
echo.
echo Documentation:
echo    - Main README: README.md
echo.
pause
