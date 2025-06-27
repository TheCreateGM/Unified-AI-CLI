# Changelog

## [2.1.0] - 2025-06-27

### Added
- Deep Thinking Mode (Chained): The CLI now chains Mistral → Gemini → Claude for deep synthesis. Mistral answers the prompt, Gemini reviews and improves it, and Claude deeply synthesizes and further improves the answer. All intermediate and final outputs are displayed in the terminal for transparency and insight.

## [2.0.0] - 2025-06-27

### Changed
- **BREAKING**: Replaced OpenAI ChatGPT with Mistral AI as the primary provider
- Updated default provider from `openai` to `mistral`
- Updated default model from `gpt-4` to `mistral-large-latest`
- Replaced `openai` dependency with `requests` for direct API calls
- Updated all configuration files to use Mistral AI models

### Added
- Support for Mistral AI models:
  - `mistral-large-latest`
  - `mistral-medium-latest`
  - `mistral-small-latest`
  - `open-mistral-7b`
  - `open-mixtral-8x7b`
  - `open-mixtral-8x22b`
  - `open-mistral-nemo`

### Updated
- Environment variable from `OPENAI_API_KEY` to `MISTRAL_API_KEY`
- All documentation and examples to reference Mistral AI
- Test suite to use Mistral AI provider
- Demo scripts to showcase Mistral AI capabilities
- Installation scripts to mention Mistral AI API key

### Removed
- OpenAI SDK dependency (`openai>=1.0.0`)
- `tiktoken` dependency (no longer needed)
- All OpenAI-specific code and configurations

## [1.0.0] - 2025-06-25

### Added
- Initial release with OpenAI ChatGPT, Google Gemini, and Anthropic Claude support
- Deep thinking mode that combines multiple AI providers
- Interactive chat mode
- Thread management for conversations
- Beautiful terminal output with Rich library
- Configuration management with YAML
- History management across sessions
- Installation and setup scripts 