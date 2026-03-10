# ArubaClawV2 - Core Agent

A lightweight AI agent framework for Aruba CX 6100 switches inspired by nanobot.

## Features

- Ultra-lightweight (~4000 lines of core code)
- Python 3.12+ with modern features
- Stdlib only (no external dependencies)
- Multi-provider LLM support
- Network automation skills
- Scheduled tasks

## Architecture

```
ArubaClawAgent
├──_llm_provider (OpenAI, Anthropic, Ollama, Groq, Perplexity, OpenRouter)
├── skills (network, system, utilities)
├── tasks (scheduled operations)
└── state (memory, history, workspace)
```

## Installation

```bash
# Copy arubaclaw.py to switch
curl -o /tmp/arubaclaw.py https://raw.githubusercontent.com/jsmeyers/arubaclawV2/main/arubaclaw.py

# Run
python3 /tmp/arubaclaw.py --test
python3 /tmp/arubaclaw.py --cli
```

## Configuration

```python
# Edit config at ~/.arubaclaw/config.json
{
    "llm_provider": "openai",
    "llm_model": "gpt-4o-mini",
    "api_key": "sk-...",
    "api_timeout": 30
}
```

Or use environment variables:
- `ARUBACLAW_API_KEY`
- `ARUBACLAW_PROVIDER`
- `ARUBACLAW_MODEL`
- `ARUBACLAW_TIMEOUT`

## Usage

```python
from arubaclaw import ArubaClawAgent

agent = ArubaClawAgent()

# Chat with LLM
response = agent.chat("Show me BGP neighbors")
print(response)

# Web search
results = agent.web_search("Aruba CX documentation")
```

## LLM Providers

| Provider | Endpoint | Auth |
|----------|----------|------|
| OpenAI | api.openai.com | API key |
| Anthropic | api.anthropic.com | API key |
| Ollama | localhost:11434 | None (local) |
| Groq | api.groq.com | API key |
| Perplexity | api.perplexity.ai | API key |
| OpenRouter | openrouter.ai | API key |

## License

MIT

## Acknowledgments

- Inspired by [nanobot](https://github.com/HKUDS/nanobot) by HKUDS
