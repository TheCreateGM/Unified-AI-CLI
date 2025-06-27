# Deep Thinking Brain - Unified AI CLI

A powerful command-line interface that combines the capabilities of multiple AI providers (Mistral AI, Google Gemini, and Anthropic Claude) into one intelligent system for deep thinking and problem-solving.

## Features

- **Multi-Provider Support**: Seamlessly switch between Mistral AI, Google Gemini, and Anthropic Claude
- **Deep Thinking Mode**: Runs Mistral, Gemini, and Claude in parallel, displays each response, and then synthesizes a final answer using Mistral. All steps are shown in the terminal.
- **Context Management**: Maintains conversation history across sessions
- **Code Generation**: Specialized code generation with Claude Code capabilities
- **Markdown Rendering**: Beautiful output formatting with syntax highlighting
- **Environment Configuration**: Secure API key management via .env files
- **Interactive Mode**: Chat-like interface similar to Ollama
- **Thread Management**: Organize conversations by topics/threads

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup
1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy the example environment file:
   ```bash
   cp env.example .env
   ```
4. Add your API keys to `.env`:
   ```bash
   MISTRAL_API_KEY=your_mistral_key_here
   GEMINI_API_KEY=your_gemini_key_here
   ANTHROPIC_API_KEY=your_anthropic_key_here
   ```

## Usage

### Basic Usage
```bash
# Simple question
python brain.py "What is the capital of France?"

# Deep thinking mode (uses multiple providers)
python brain.py --deep "Explain quantum computing"

# Code generation
python brain.py --code "Create a Python web scraper"

# Interactive mode
python brain.py --interactive
```

### Advanced Usage
```bash
# Use specific provider
python brain.py --provider mistral "Hello"

# Set model
python brain.py --model mistral-large-latest "Complex question"

# Save to file
python brain.py "Long analysis" --output analysis.md

# Continue conversation
python brain.py --thread coding "Continue from where we left off"
```

### Deep Thinking Mode (Synthesis)
To use the deep thinking mode, run:

```bash
brain --deep "Explain quantum computing in simple terms"
```

This will:
1. Get answers from Mistral, Gemini, and Claude in parallel
2. Display each provider's response in the terminal
3. Use Mistral to synthesize a comprehensive answer from all responses

All intermediate and final outputs will be displayed in the terminal for full transparency.

## Configuration

The tool uses a `config.yaml`