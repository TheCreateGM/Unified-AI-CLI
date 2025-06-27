#!/bin/bash

# Deep Thinking Brain CLI Installation Script

set -e

echo "🧠 Installing Deep Thinking Brain CLI..."

# Check if Python 3.8+ is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.8+ is required. Current version: $python_version"
    exit 1
fi

echo "✅ Python $python_version detected"

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Please edit .env file and add your API keys:"
    echo "   - MISTRAL_API_KEY"
    echo "   - GEMINI_API_KEY" 
    echo "   - ANTHROPIC_API_KEY"
else
    echo "✅ .env file already exists"
fi

# Make brain.py executable
chmod +x brain.py

# Create symlink to make it globally accessible
if [ ! -L /usr/local/bin/brain ]; then
    echo "🔗 Creating global symlink..."
    sudo ln -sf "$(pwd)/brain.py" /usr/local/bin/brain
    echo "✅ You can now use 'brain' command from anywhere"
else
    echo "✅ Global symlink already exists"
fi

# Create history directory
mkdir -p ~/.brain-cli

echo ""
echo "🎉 Installation complete!"
echo ""
echo "Usage examples:"
echo "  brain 'What is the capital of France?'"
echo "  brain --deep 'Explain quantum computing'"
echo "  brain --interactive"
echo "  brain --provider mistral 'Hello'"
echo ""
echo "For more information, see README.md"
echo "" 