# ArubaClawV2 - Nanobot-inspired agent for Aruba CX switches

**Status**: In development

**Goal**: Create an ultra-lightweight Python 3.12+ agent inspired by Nanobot, specifically designed for Aruba CX 6100 switches.

## Key Differences from arubaclawV1:

1. **Python 3.12+** - Use modern Python features (f-strings, dataclasses, async)
2. **Nanobot philosophy** - Ultra-lightweight, ~4000 lines of core code
3. **Aruba CX optimized** - Built-in NAE Python environment
4. **Stdlib only** - No external dependencies (urllib, ssl, json, os, datetime, hashlib)
5. **Multi-provider LLM** - OpenAI, Anthropic, Ollama, Groq, Perplexity, OpenRouter

## Structure:

```
arubaclawV2/
├── arubaclaw.py        # Core agent (~4000 lines)
├── skills/             # Skills modules
│   ├── __init__.py
│   └── network.py      # Network automation skills
├── tasks/              # Scheduled tasks
│   ├── __init__.py
│   └── health_check.py
├── examples/
│   ├── simple-chat.py
│   └── scheduled-task.py
└── tests/
    ├── test_agent.py
    └── test_skills.py
```

## Core Features:

- `ArubaClawAgent` class
- Chat with LLM
- Web search (Brave API)
- Scheduled tasks (cron-style)
- Skills system
- Console/SSH access

## Next Steps

1. ✅ Create repo: `jsmeyers/arubaclawV2`
2. Implement core agent (`arubaclaw.py`)
3. Add Aruba CX-specific skills
4. Test on virtual switch
5. Deploy to production hardware

---

**Repo**: https://github.com/jsmeyers/arubaclawV2
