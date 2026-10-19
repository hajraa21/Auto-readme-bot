# Auto‑Readme‑Bot 🤖  

[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/your-username/auto-readme-bot/generate_readme.yml?branch=main&label=CI)](https://github.com/your-username/auto-readme-bot/actions)  
[![License](https://img.shields.io/github/license/your-username/auto-readme-bot)](LICENSE)  
[![Version](https://img.shields.io/pypi/v/auto-readme-bot.svg)](https://pypi.org/project/auto-readme-bot/)  

> **Auto‑Readme‑Bot** is a tiny Python utility that scans a repository, sends the source files to a Groq LLM, and automatically generates a polished `README.md`. It can be run locally or as a GitHub Action to keep documentation in sync with code changes.

---

## Table of Contents  

- [Description](#description)  
- [Features](#features)  
- [Tech Stack / Built With](#tech-stack--built-with)  
- [Prerequisites & Installation](#prerequisites--installation)  
- [Usage](#usage)  
- [Environment Variables](#environment-variables)  
- [API Reference](#api-reference)  
- [Roadmap](#roadmap)  
- [Contributing](#contributing)  
- [License](#license)  
- [Authors & Acknowledgements](#authors--acknowledgements)  
- [Support / FAQ](#support--faq)  

---

## Description  

Maintaining up‑to‑date documentation is a repetitive task that often falls behind development. **Auto‑Readme‑Bot** automates this process:

1. Walks the repository tree while respecting ignore lists.  
2. Collects source files of supported extensions.  
3. Sends the aggregated code to Groq’s LLM with a detailed system prompt.  
4. Writes the LLM‑generated markdown to `README.md`.  

The bot can be triggered manually, via CI/CD, or as part of a pre‑commit workflow, ensuring that the README always reflects the current state of the codebase.

---

## Features  

- **Smart file selection** – skips common binary, build, and dependency directories/files.  
- **Broad language support** – works with Python, JavaScript/TypeScript, Go, Rust, Java, C/C++, Ruby, PHP, HTML/CSS, JSON/YAML, shell scripts, and more.  
- **Zero‑configuration CI** – a ready‑to‑use GitHub Actions workflow that generates and commits the README on every push.  
- **Customizable prompts** – edit the system prompt in `main.py` to tailor the output style or add extra sections.  
- **Environment‑agnostic** – runs on any platform with Python 3.13+ and an internet connection.  

---

## Tech Stack / Built With  

| Category | Tool / Library |
|----------|----------------|
| Language | Python 3.13 |
| LLM Provider | **Groq** (`groq` Python SDK) |
| Environment Management | `python-dotenv` |
| HTTP Requests | `requests` |
| CI / Automation | GitHub Actions |
| Packaging | `pyproject.toml` (PEP 621) |

---

## Prerequisites & Installation  

### Prerequisites  

- Python 3.13 or newer  
- A Groq API key (sign up at <https://groq.com/>)  

### Installation  

```bash
# Clone the repository
git clone https://github.com/your-username/auto-readme-bot.git
cd auto-readme-bot

# (Optional) Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt   # or: pip install groq python-dotenv requests
```

#### Install as a package (optional)

```bash
pip install .
```

---

## Usage  

### Run locally  

```bash
# Export your Groq API key (or place it in a .env file)
export GROQ_API_KEY=your_groq_api_key   # Windows: set GROQ_API_KEY=your_groq_api_key

# Execute the script
python main.py
```

The script will:

- Detect all relevant source files.  
- Call the Groq LLM with a system prompt that instructs it to generate a full README.  
- Write the output to `README.md`.  

### Run via GitHub Actions (recommended)  

A workflow file (`.github/workflows/generate_readme.yml`) is already included. After adding the secret `GROQ_API_KEY` to your repository settings, the README will be regenerated automatically on every push to `main`.

---

## Environment Variables  

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | API key for Groq’s LLM service. | Yes |
| `PYTHONPATH` *(optional)* | Allows adding extra directories to the module search path when scanning the repo. | No |

Create a `.env` file in the project root (ignored by Git) for convenience:

```dotenv
GROQ_API_KEY=your_groq_api_key
```

---

## API Reference  

The core functions can be imported and used programmatically:

```python
from auto_readme_bot import check_codebase, code_to_api

# 1️⃣ Gather source files
code_content = check_codebase(root_dir="path/to/your/project")

# 2️⃣ Generate README (writes to README.md)
code_to_api(code_content)
```

### Functions  

| Function | Signature | Description |
|----------|-----------|-------------|
| `check_codebase` | `check_codebase(root_dir: str = ".") -> dict[str, str]` | Recursively walks `root_dir`, filters out ignored directories/files, and returns a mapping `{file_path: file_content}`. |
| `code_to_api` | `code_to_api(code_content: dict[str, str]) -> None` | Formats the collected code, builds the user prompt, calls Groq’s chat completion endpoint, and writes the returned markdown to `README.md`. |

No public HTTP API is exposed; the library is intended for local or CI usage.

---

## Roadmap  

- [ ] Add support for custom ignore patterns via a `.readmeignore` file.  
- [ ] Provide a CLI flag to select the LLM model (e.g., `gpt-4o-mini`, `llama3.1‑70b`).  
- [ ] Implement a pre‑commit hook that runs the bot before each commit.  
- [ ] Add unit tests for the file‑collection logic.  
- [ ] Publish the package to PyPI under the name `auto-readme-bot`.  

---

## Contributing  

Contributions are welcome! Please follow these steps:

1. Fork the repository.  
2. Create a feature branch (`git checkout -b feat/awesome-feature`).  
3. Make your changes and ensure they pass linting (`flake8`) and any existing tests.  
4. Open a Pull Request with a clear description of the change.  
5. Ensure the CI workflow passes.  

### Development Setup  

```bash
# Install development dependencies (if you add a [dev] extra in pyproject.toml)
pip install -e .[dev]

# Linting
flake8 .

# Run tests (once tests are added)
pytest
```

Please adhere to the existing code style and include docstrings for new functions.

---

## License  

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## Authors & Acknowledgements  

- **Your Name** – Creator & Maintainer ([@your‑github‑handle](https://github.com/your-username))  
- **Groq** – Provided the LLM API used for content generation.  
- Inspired by various auto‑documentation tools and the philosophy of “documentation as code”.  

---

## Support / FAQ  

**Q: I get an authentication error from Groq.**  
A: Verify that `GROQ_API_KEY` is correctly set and has not expired. You can test it with a simple curl request or by printing the variable in the script (`print(os.getenv("GROQ_API_KEY"))`).  

**Q: The generated README is missing sections.**  
A: Edit the `SYSTEM_PROMPT` in `main.py` to include or reorder the desired sections, then re‑run the script.  

**Q: Can I run the bot on a private repository?**  
A: Yes. The script works on any local checkout; just ensure the Groq API key is available in the environment.  

**Q: How do I contribute a new language extension?**  
A: Add the file extension to the `VALID_EXTENSIONS` list in `main.py` and submit a PR.  

**Q: How can I use this for my personal projects?**  
A: Copy the `main.py` script and the GitHub Actions workflow into your repository, add the `GROQ_API_KEY` secret, and the bot will automatically generate a README for that project.  

For further assistance, open an issue or contact the maintainer via GitHub Discussions or email at `hajra.khan2108@gmail.com`.