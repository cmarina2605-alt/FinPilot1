#!/bin/bash
echo "FINPILOT AI - AUTOMATIC INSTALLATION"
echo "=========================================="

# 1. Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# 2. Activate environment
echo "Activating environment..."
source venv/bin/activate

# 3. Update pip
echo "Updating pip..."
pip install --upgrade pip

# 4. Install dependencies
echo "Installing dependencies..."
pip install --force-reinstall -r requirements.txt
pip install --force-reinstall numpy==1.26.4

# 5. Finished
echo ""
echo "INSTALLATION COMPLETE!"
echo "=========================================="
echo "NOW RUN:"
echo "   ./start.sh"
echo ""
echo "Available models:"
echo "   ollama pull gemma2:9b   # 5.4 GB"
echo "   ollama pull gemma2:2b   # 1.3 GB"
echo ""
