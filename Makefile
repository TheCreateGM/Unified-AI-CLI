# Deep Thinking Brain CLI Makefile

.PHONY: install uninstall test clean help setup

# Default target
all: setup

# Setup the environment
setup:
	@echo "🧠 Setting up Deep Thinking Brain CLI..."
	@chmod +x install.sh
	@./install.sh

# Install dependencies only
install-deps:
	@echo "📦 Installing dependencies..."
	@pip3 install -r requirements.txt

# Create .env file
setup-env:
	@echo "📝 Setting up environment file..."
	@cp env.example .env
	@echo "⚠️  Please edit .env file and add your API keys"

# Make executable and create symlink
install-cli:
	@echo "🔗 Installing CLI..."
	@chmod +x brain.py
	@sudo ln -sf $(PWD)/brain.py /usr/local/bin/brain
	@mkdir -p ~/.brain-cli
	@echo "✅ CLI installed successfully"

# Run tests
test:
	@echo "🧪 Running tests..."
	@python3 -m pytest tests/ -v

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@rm -rf .pytest_cache
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info/

# Uninstall
uninstall:
	@echo "🗑️  Uninstalling Deep Thinking Brain CLI..."
	@sudo rm -f /usr/local/bin/brain
	@echo "✅ CLI uninstalled"

# Show help
help:
	@echo "Deep Thinking Brain CLI - Available commands:"
	@echo ""
	@echo "  setup        - Complete setup (install deps, setup env, install CLI)"
	@echo "  install-deps - Install Python dependencies only"
	@echo "  setup-env    - Create .env file from template"
	@echo "  install-cli  - Make executable and create global symlink"
	@echo "  test         - Run tests"
	@echo "  clean        - Clean up Python cache and build files"
	@echo "  uninstall    - Remove global symlink"
	@echo "  help         - Show this help message"
	@echo ""
	@echo "Usage examples:"
	@echo "  make setup        # Complete installation"
	@echo "  make install-deps # Install dependencies only"
	@echo "  make test         # Run tests"

# Development helpers
dev-setup: install-deps setup-env
	@echo "🔧 Development environment ready"

# Quick test run
quick-test:
	@echo "⚡ Quick test..."
	@python3 brain.py --help

# Format code
format:
	@echo "🎨 Formatting code..."
	@black brain.py
	@isort brain.py

# Lint code
lint:
	@echo "🔍 Linting code..."
	@flake8 brain.py
	@pylint brain.py 