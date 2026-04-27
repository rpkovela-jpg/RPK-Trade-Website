#!/bin/bash
# Quick setup script for RPK Trading System

echo "🚀 RPK Algorithmic Trading System - Setup Script"
echo "=================================================="

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Navigate to backend
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Return to root
cd ..

echo ""
echo "=================================================="
echo "✓ Setup complete!"
echo ""
echo "To start the application:"
echo ""
echo "1. Backend (Flask API):"
echo "   cd backend"
echo "   source venv/bin/activate  # On macOS/Linux"
echo "   python run.py"
echo ""
echo "2. Frontend (Web Interface):"
echo "   cd frontend"
echo "   Open index.html in your browser, or:"
echo "   python -m http.server 8000"
echo ""
echo "Then visit: http://localhost:8000"
echo ""
echo "API will be at: http://localhost:5000"
echo "=================================================="
