# arubaclawV2 Tests

Test suite for the ArubaClawV2 agent.

## Running Tests

```bash
cd tests
python3 test_agent.py
python3 test_skills.py
python3 test_llm.py
```

## Test Coverage

- `test_agent.py` - Core agent initialization and configuration
- `test_skills.py` - Network and system skills
- `test_llm.py` - LLM provider API formatting

## Mock Testing

Tests use `unittest.mock` to simulate API responses.
