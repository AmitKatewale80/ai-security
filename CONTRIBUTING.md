# Contributing to Airline AI Security Labs

Thank you for your interest in contributing! Here's how you can help.

## How to Contribute

### Reporting Issues
- Open a GitHub Issue describing the bug or suggestion
- Include which lab is affected and steps to reproduce

### Adding New Labs
1. Fork the repository
2. Create a new folder: `airline-labs/lab-XX-descriptive-name/`
3. Include at minimum:
   - `README.md` — Lab description, objectives, and instructions
   - Numbered Python scripts (`1_first_step.py`, `2_second_step.py`, etc.)
   - `requirements.txt` — Python dependencies
   - `.gitignore` — Exclude venvs, models, sensitive data
   - `reset.py` — Cleanup script
4. Submit a Pull Request

### Code Style
- Use Python 3.9+ compatible syntax
- Include docstrings and comments explaining security concepts
- Use `rich` library for colored terminal output where possible
- Keep scripts self-contained and runnable independently

### Security
- Never commit real API keys, credentials, or sensitive data
- Use `.env.example` files to show required environment variables
- All attack simulations must be local-only (no external targets)

## Code of Conduct

Be respectful, constructive, and focused on education. This is a learning resource.
