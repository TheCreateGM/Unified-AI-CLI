# Deep Thinking Brain - Unified AI CLI

A powerful command-line interface that combines the capabilities of multiple AI providers (Mistral AI, Google Gemini, and Anthropic Claude) into one intelligent system for deep thinking and problem-solving.

## Features

- **Multi-Provider Support**: Seamlessly switch between Mistral AI, Google Gemini, and Anthropic Claude
- **Deep Thinking Mode**: Combines insights from multiple AI models for comprehensive analysis
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

## Configuration

The tool uses a `config.yaml` file for default settings:

```yaml
default_provider: mistral
default_model: mistral-large-latest
max_tokens: 4096
temperature: 0.7
history_enabled: true
output_format: markdown
```

## Providers

### Mistral AI
- Models: mistral-large-latest, mistral-medium-latest, mistral-small-latest, open-mistral-7b, open-mixtral-8x7b, open-mixtral-8x22b, open-mistral-nemo
- Best for: General conversation, creative writing, analysis, code generation

### Google Gemini
- Models: gemini-pro, gemini-pro-vision
- Best for: Multimodal tasks, coding, reasoning

### Anthropic Claude
- Models: claude-3-opus, claude-3-sonnet, claude-3-haiku
- Best for: Code generation, technical writing, safety-focused tasks

## Deep Thinking Mode

When using `--deep` flag, the tool:
1. Analyzes the question with multiple AI providers
2. Combines insights for comprehensive understanding
3. Provides a unified, well-reasoned response
4. Shows individual provider perspectives

## Examples

```bash
# Code review
python brain.py --code "Review this Python code for best practices"

# Research synthesis
python brain.py --deep "Compare machine learning frameworks"

# Creative writing
python brain.py --provider mistral "Write a short story about AI"

# Technical analysis
python brain.py --provider claude "Explain Docker containers"
```

## Environment Variables

Create a `.env` file with your API keys:

```env
MISTRAL_API_KEY=your-mistral-api-key
GEMINI_API_KEY=your-gemini-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-api-key
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### Open Source

This project is **open source** and welcomes contributions from the community. Feel free to:

- 🐛 Report bugs and issues
- 💡 Suggest new features
- 🔧 Submit pull requests
- 📖 Improve documentation
- 🌟 Star the repository if you find it useful

The MIT License ensures that you can:
- Use this software for any purpose
- Modify and distribute it
- Use it commercially
- Distribute modified versions

All we ask is that you include the original license and copyright notice. 