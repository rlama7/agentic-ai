# Agentic AI — Module 3, Part 1: Functions as Tools

A local Python implementation of **“Turning functions into tools”** from [DeepLearning.AI's Agentic AI course](https://www.deeplearning.ai/courses/agentic-ai), taught by Andrew Ng.

The project demonstrates how a language model selects Python tools, supplies arguments, receives tool results, and coordinates several tools to complete a request. It includes both **AISuite-managed automatic tool calling** and **application-managed manual tool execution**.

> **Project status:** All four individual tools and the combined QR-code + weather-note workflow have been demonstrated locally. The initial attempt to inspect intermediate messages via `response.messages` showed that this attribute was unavailable; decorator-based execution tracing is an optional enhancement whose successful output has not yet been confirmed.

## What this demo does

| Tool | Purpose | Input | Output / effect |
| --- | --- | --- | --- |
| `get_current_time` | Read local system time | None | String such as `14:12:27` |
| `get_weather_from_ip` | Obtain approximate local weather | None | Current/high/low temperatures in °F |
| `write_txt_file` | Save a text note | `file_path`, `content` | UTF-8 file under `output/` |
| `generate_qr_code` | Generate a scannable QR code, optionally with a logo | `data`, `filename`, `image_path` | PNG under `output/` |

The combined agent can accept a request to generate a branded QR code **and** write a weather report with a retrieval time. Weather and time are retrieved before they are incorporated into the report.

## Repository layout

Located at `apps/python/tool-use/functions-as-tools/` in the larger `agentic-ai` repository.

```text
functions-as-tools/
├── .venv/                    # Local virtual environment (ignored)
├── .env                      # API key (ignored)
├── .env.example              # Credential placeholder
├── requirements.txt
├── README.md
├── assets/
│   └── lama-rock.png         # Local image used in the demonstrated QR workflow
├── output/                   # Generated TXT/PNG files
├── src/
│   ├── __init__.py
│   ├── main.py               # Automatic time tool demo
│   ├── tools.py              # Four Python tool functions
│   ├── manual_tool_call.py   # Manual schema + execution demo
│   ├── weather_agent.py      # Multiple available tools, weather request
│   ├── file_agent.py         # File-writing request
│   ├── qr_agent.py           # Branded QR-code request
│   ├── multi_tool_agent.py   # Combined multi-tool workflow
│   └── tracing.py            # Optional decorator-based execution trace
├── tests/
│   └── test_main.py          # Initial Hello World smoke test; see Testing note
└── docs/
    └── ARCHITECTURE.md
```

`src/tracing.py` describes the optional instrumentation from the final learning step. Verify that it exists locally before using it. The earlier `test_main.py` initially targeted the Hello World entry point and **must be updated or removed** if it still expects that output after `main.py` was changed to use AISuite.

## Getting started

Run these commands from the `functions-as-tools/` directory on macOS.

```bash
python3.11 -m venv .venv          # Create an isolated Python 3.11 environment
source .venv/bin/activate        # Activate the local environment
python -m pip install -r requirements.txt  # Install project dependencies
cp .env.example .env             # Create local credentials file, if not already present
```

Set your own `OPENAI_API_KEY` inside `.env`. **Do not commit credentials.** The existing repository-level `.gitignore` should exclude `.env`, `.venv/`, cache directories, and generated artifacts where appropriate.

The environment used for this demo is **Python 3.11.7**. Requirements include AISuite (with OpenAI and MCP extras), python-dotenv, requests, qrcode with Pillow support, and pytest:

```text
aisuite[openai,mcp]
python-dotenv
requests
qrcode[pil]
pytest
```

The version ranges above are illustrative dependency names, not a lockfile. For reproducible deployments, pin tested versions separately.

## Run the demonstrations

Run from `functions-as-tools/` with `.venv` active:

| Command | Demonstration |
| --- | --- |
| `python -m src.main` | Automatic time tool calling |
| `python -m src.manual_tool_call` | Manual tool schema, execution, and result return |
| `python -m src.weather_agent` | Select weather from several available tools |
| `python -m src.file_agent` | Infer filename and text content |
| `python -m src.qr_agent` | Infer URL, output name, and logo |
| `python -m src.multi_tool_agent` | Coordinate time, weather, QR creation, and note writing |

To inspect generated files:

```bash
cat output/weather_report.txt   # Display saved weather information
open output/lama_multi_qr.png    # Open QR image on macOS
```

Scan the QR with a phone to verify the encoded URL. **Pass plain URLs** such as `https://www.ratnalama.com` to the tool, not Markdown link syntax.

The combined demo writes or overwrites `output/weather_report.txt` and `output/lama_multi_qr.png`; keep any important previous versions elsewhere.

## Learning progression

1. **Plain Python function:** Implement and invoke `get_current_time()` without an LLM.
2. **Automatic tool calling:** Register a Python callable in AISuite with `tools=[get_current_time]` and `max_turns=5`.
3. **Manual tool calling:** Submit a JSON-compatible function schema, read `tool_calls`, parse `function.arguments`, execute an allowlisted function, and return the result with the corresponding `tool_call_id`.
4. **Additional tools:** Add an IP-based weather API lookup, text-file writing, and QR creation.
5. **Model-driven tool selection:** Provide multiple functions and let the model choose based on the user request.
6. **Multi-tool orchestration:** Use previously returned weather and time values to populate a saved weather report, alongside independent QR generation.
7. **Observability:** Inspect the tool sequence. Where AISuite does not surface an intermediate trace, wrap local functions to log actual execution.

## Enhancements beyond the course lab

- Organized the notebook content into independent, runnable Python modules within the larger portfolio repository.
- Created a dedicated virtual environment and `.env.example` for local setup.
- Limited text output to a project-specific `output/` directory and rejected obvious path-based filenames.
- Added HTTP timeouts and `raise_for_status()` to weather API calls.
- Made the QR logo optional; resolved logo assets from `assets/` and wrote PNGs into `output/`.
- Demonstrated QR generation with an independently selected Lama Rock logo and verified its scan behavior.
- Kept separate automatic and manual tool-calling demos to make their responsibilities easy to compare.
- Proposed lightweight decorator-based logging for tool execution and argument propagation (pending local confirmation).
- Resolved an AISuite optional-dependency failure involving `is_mcp_config` by installing the `mcp` extra.

## Testing and verification

This is a **learning/demo application**, not a production service. Validation was deliberately kept lightweight:

- Directly executed the time, weather, file-writing, and QR-code Python functions.
- Confirmed the time, weather, note-writing, QR, and combined AISuite agent responses in terminal output.
- Read the written text files and scanned generated QR images.
- Initially passed one pytest Hello World smoke test before changing the application entry point.

**Before running `pytest` again:** Update `tests/test_main.py` if it still asserts the previous Hello World output. No current automated test-suite pass is claimed for the later AISuite-based application. Prefer mocked API/tool tests if adding tests so test runs do not consume live API usage or overwrite files.

## Important boundaries

- IP-derived location is approximate; VPNs or network routing can change the weather location.
- API responses, model-selected tools, generated arguments, and execution ordering may vary across runs.
- AISuite may not expose full intermediate automatic tool history on the final response object. Function-level logs show actual local execution but are **not** a complete model conversation trace.
- File-writing and QR functions can overwrite names inside `output/`. This is acceptable for a controlled demo but requires stronger validation and approval controls in a deployed system.
- Exceptions and malformed responses should be handled more comprehensively in production.
- An OpenAI API key and paid API usage may be required; a ChatGPT subscription is not an API credential.

See [Architecture and execution flow](docs/ARCHITECTURE.md) for diagrams, message examples, trust boundaries, and design tradeoffs.

## Attribution

This is a **derivative learning project** based on the *Turning functions into tools* lab in Andrew Ng's [Agentic AI course on DeepLearning.AI](https://www.deeplearning.ai/courses/agentic-ai). The core exercise, tool names, and learning sequence come from the course. Local packaging, output restrictions, HTTP hardening, separate demo entry points, branding assets, troubleshooting notes, and instrumentation are project-specific refinements. This repository is not affiliated with or endorsed by DeepLearning.AI.
