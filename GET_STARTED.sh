#!/bin/bash
# Quick start script for the MathTutor Harness Evaluation project

echo "=========================================="
echo "MathTutor Harness Evaluation Setup"
echo "=========================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9+"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "⬇️  Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo ""
echo "✅ Installation complete!"
echo ""

# Check for .env
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.example .env
    echo ""
    echo "📝 Please edit .env and add your ANTHROPIC_API_KEY"
    echo ""
    echo "Get your API key from: https://console.anthropic.com/"
    echo ""
else
    echo "✅ .env file exists"
    echo ""
fi

# Run tests
echo "🧪 Running tests..."
python -m pytest tests/test_harnesses.py -v

echo ""
echo "=========================================="
echo "Setup Complete! Next Steps:"
echo "=========================================="
echo ""
echo "1. Add your API key to .env:"
echo "   nano .env"
echo ""
echo "2. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "3. Run a quick experiment (3 problems):"
echo "   python run_experiment.py"
echo ""
echo "4. Launch the dashboard:"
echo "   python src/dashboard.py"
echo ""
echo "5. Read the documentation:"
echo "   - README.md - Project overview"
echo "   - QUICKSTART.md - Getting started guide"
echo "   - ANALYSIS_GUIDE.md - How to interpret results"
echo "   - PROJECT_OVERVIEW.md - Technical details"
echo ""
echo "=========================================="

