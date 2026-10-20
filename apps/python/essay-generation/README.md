# Essay Generation Agent with Reflection

A modular Python application that uses Large Language Models (LLMs) to generate, critique, and revise essays through an iterative reflection workflow.

Developed as part of the **Agentic AI course by Andrew Ng and DeepLearning.AI**, with additional software engineering enhancements focused on modular architecture, dependency injection, automated testing, error handling, and output persistence.

**Course reference:** https://www.deeplearning.ai/courses/agentic-ai/

## 1. Project Overview

The application implements a three-stage agentic workflow:

1. **Generate:** Produce an initial essay from a user-provided topic.
2. **Reflect:** Critically evaluate the generated essay.
3. **Revise:** Improve the original essay using the reflection feedback.

The workflow demonstrates how an LLM can iteratively improve its own output through a separate evaluation stage.

### Learning Objectives

- Understand the reflection design pattern in agentic AI.
- Orchestrate multiple sequential LLM calls.
- Separate LLM integration from application logic.
- Implement dependency injection using Python protocols.
- Build reproducible unit tests with fake and mocked clients.
- Handle provider errors and invalid responses.
- Persist intermediate and final artifacts.
- Design a maintainable Python project beyond a notebook.

## 2. High-Level Architecture

```text
                     User Topic
                         |
                         v
                    CLI / main.py
                         |
                         v
                 run_essay_workflow()
                         |
             +-----------+-----------+
             |                       |
             v                       |
       generate_draft()              |
             |                       |
             v                       |
        Initial Draft                |
             |                       |
             v                       |
       reflect_on_draft()            |
             |                       |
             v                       |
       Reflection Feedback           |
             |                       |
             v                       |
        revise_draft()               |
             |                       |
             v                       |
         Revised Essay               |
             |                       |
             v                       |
         EssayResult                 |
             |                       |
             v                       |
       Output Manager <--------------+
             |
             v
      Unique Run Directory
             |
     +-------+---------+
     |       |         |
     v       v         v
 draft.md reflection.md revised.md
```

### Architectural Principles

**Separation of concerns:** Each module has a focused responsibility.

**Dependency injection:** Workflow functions accept an LLM-compatible client rather than constructing their own.

**Protocol-based interfaces:** The `TextGenerator` protocol defines the contract required from a text-generation client.

**Testability:** Workflow logic can be tested without network requests.

**Fail-fast behavior:** Exceptions interrupt the workflow rather than allowing invalid intermediate results to propagate.

**Output preservation:** Each successful run receives a uniquely named output directory.

## 3. Project Structure

```text
essay-generation/
├── data/
├── docs/
├── output/
│   └── .gitkeep
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── llm_client.py
│   ├── draft_generator.py
│   ├── reflection.py
│   ├── revision.py
│   ├── workflow.py
│   ├── output_manager.py
│   └── exceptions.py
├── tests/
│   ├── __init__.py
│   ├── test_draft_generator.py
│   ├── test_reflection.py
│   ├── test_revision.py
│   ├── test_workflow.py
│   ├── test_main.py
│   ├── test_output_manager.py
│   ├── test_exceptions.py
│   └── test_llm_client.py
├── .env
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

The diagram documents the primary implementation files; optional local scripts and notebooks may also be present.

### Module Responsibilities

| Module               | Responsibility                                     |
| -------------------- | -------------------------------------------------- |
| `main.py`            | Application entry point and workflow execution     |
| `llm_client.py`      | LLM API integration and response validation        |
| `draft_generator.py` | Generate the initial essay                         |
| `reflection.py`      | Critique the draft                                 |
| `revision.py`        | Revise the essay using feedback                    |
| `workflow.py`        | Coordinate the three-stage workflow                |
| `output_manager.py`  | Create run directories and save Markdown artifacts |
| `exceptions.py`      | Application-level exception hierarchy              |

## 4. Reflection Workflow

### Stage 1: Essay Generation

**Function:** `generate_draft()`

**Input:** Essay topic

**Default model:** `openai:gpt-4o`

**Output:** Initial essay draft

The generation function creates a prompt instructing the LLM to produce an essay about the supplied topic.

### Stage 2: Reflection

**Function:** `reflect_on_draft()`

**Input:** Generated essay

**Default model:** `openai:o4-mini`

**Output:** Constructive feedback

The reflection stage evaluates dimensions such as:

- Structure and organization
- Clarity and coherence
- Strength of arguments
- Writing style
- Opportunities for improvement

### Stage 3: Revision

**Function:** `revise_draft()`

**Inputs:** Original essay and reflection feedback

**Default model:** `openai:gpt-4o`

**Output:** Revised essay

The revision stage uses the feedback to produce an improved version of the essay.

The revision prompt also discourages inventing unsupported statistics or citations. This is a prompt-level safeguard, not independent factual verification.

### Workflow Result

The workflow returns an `EssayResult` dataclass:

```python
@dataclass
class EssayResult:
    topic: str
    draft: str
    feedback: str
    revised_draft: str
```

This provides a consistent data contract between orchestration, testing, and persistence.

## 5. LLM Integration Architecture

The application uses `aisuite` to communicate with an LLM provider.

The `LLMClient` encapsulates:

- Client initialization
- Environment variable loading
- Model selection
- Prompt submission
- Response extraction and validation
- Provider exception handling

### Dependency Injection

Instead of directly constructing `LLMClient` inside every workflow function, the application accepts an object that satisfies the `TextGenerator` protocol.

Conceptually:

```python
def generate_draft(
    topic: str,
    client: TextGenerator,
    model: str = "openai:gpt-4o",
) -> str: ...
```

This allows the same workflow code to run with either a real LLM client or a fake implementation.

### Benefits

- Lower coupling between application logic and LLM providers
- Easier unit testing
- Flexible model selection
- Improved maintainability
- Clearer module boundaries

## 6. Error Handling

The application defines custom exception types:

```text
RuntimeError
└── LLMError
    ├── LLMAuthenticationError
    ├── LLMRateLimitError
    ├── LLMServiceError
    └── LLMResponseError
```

### Error Categories

| Exception                | Description                             |
| ------------------------ | --------------------------------------- |
| `LLMAuthenticationError` | Authentication or permission failure    |
| `LLMRateLimitError`      | API rate limit exceeded                 |
| `LLMServiceError`        | Transient service or connection failure |
| `LLMResponseError`       | Empty or malformed response             |
| `LLMError`               | Other LLM-related errors                |

The LLM client inspects available exception chains to identify underlying OpenAI provider errors.

**Current limitations:** Automatic retries, backoff, and comprehensive tests of every provider-failure branch are not implemented.

## 7. Output Persistence

Successful workflow executions automatically save:

```text
output/
├── .gitkeep
└── 20261020_174703_0571847d/
    ├── draft.md
    ├── reflection.md
    └── revised.md
```

Each run directory combines a UTC timestamp and a short UUID-derived identifier.

### Persistence Design

`create_run_directory()` creates a new directory using exclusive creation to prevent silently reusing an existing run directory.

`save_essay_result()` writes the three Markdown files using UTF-8 encoding.

The persistence layer is separate from the essay-generation workflow.

**Current limitation:** A filesystem failure partway through saving may leave a partially populated run directory. Atomic multi-file persistence is not yet implemented.

## 8. Setup and Execution

### Prerequisites

- Python 3.11 or a compatible version
- Access to an OpenAI API key
- Project dependencies installed in the active Python environment

### Environment Configuration

Configure the environment variable:

```dotenv
OPENAI_API_KEY=your_api_key_here
```

Store the real key in `.env`, which must remain excluded from version control.

Do not commit API credentials.

### Install Dependencies

From the project directory, activate your existing virtual environment and install the dependencies declared by the project:

```bash
python -m pip install -r requirements.txt
```

Use the actual requirements file maintained by this project, or the installation configuration in `pyproject.toml` if dependencies are managed there.

### Run the Application

```bash
python -m src.main
```

The CLI executes the three-stage workflow using its default topic:

> The impact of artificial intelligence on education

It prints the draft, reflection feedback, and revised essay, then saves all three results in a new output directory.

Live execution makes external API requests and may incur usage charges.

## 9. Testing Strategy

The project uses `pytest` with deterministic tests.

### Unit Testing

Tests validate each workflow component independently:

- Topic validation
- Draft generation
- Reflection
- Revision
- Model selection
- Output content

### Workflow Testing

Fake LLM clients simulate a sequence of generated outputs.

Tests verify that the workflow executes the required stages in order and stops when a stage fails.

### LLM Client Testing

Mocked API clients validate:

- Successful response extraction
- Correct forwarding of request arguments
- Rejection of empty strings
- Rejection of whitespace-only responses
- Rejection of missing content
- Rejection of malformed response choices

### Persistence Testing

Tests use pytest's `tmp_path` fixture to validate:

- File creation
- File overwriting behavior
- Unicode preservation
- Invalid destination paths
- Unique run directory creation
- Automatic persistence through the application entry point

### Execute Tests

```bash
python -m pytest -v
```

**Latest confirmed baseline:** 29 passing tests.

### Code Quality

```bash
python -m ruff check .
python -m ruff format --check .
```

These commands verify linting and formatting.

## 10. Enhancements Beyond the Course Exercise

The original course exercise establishes the reflection workflow through draft generation, critique, and revision.

This repository extends that learning exercise into a maintainable application.

| Area                  | Enhancement                             |
| --------------------- | --------------------------------------- |
| Architecture          | Modular Python source files             |
| Orchestration         | Dedicated workflow coordinator          |
| Interface design      | `TextGenerator` protocol                |
| Dependency management | Injectable LLM client                   |
| Data modeling         | Typed `EssayResult` dataclass           |
| Persistence           | Automatic Markdown artifact saving      |
| Version preservation  | Unique run directories                  |
| Reliability           | Fail-fast workflow behavior             |
| Error handling        | Custom exception hierarchy              |
| Response validation   | Empty and malformed response rejection  |
| Testing               | Pytest unit and integration-style tests |
| Mocking               | Fake LLM clients and `unittest.mock`    |
| Code quality          | Ruff linting and formatting             |

These enhancements are intended to demonstrate the transition from completing an educational notebook to engineering a reusable LLM-powered application.

## 11. Limitations and Future Enhancements

The following improvements are intentionally outside the current learning scope.

### Reliability

- Exponential backoff for retryable errors
- Request timeout configuration and retry limits
- Atomic persistence and cleanup of partial runs
- Structured logging and execution tracing

### Agentic Capabilities

- Multiple reflection and revision iterations
- Quality scoring and stopping criteria
- Source retrieval and citation verification
- Multi-agent evaluation
- Human-in-the-loop approvals

### Application Features

- Command-line topic arguments
- Model configuration through environment variables
- FastAPI integration
- React-based UI
- Asynchronous execution
- Token usage and cost tracking

### Evaluation

- Automated output-quality evaluation
- Reproducible benchmark datasets
- Comparison of original and revised essay quality
- Regression tests for prompt changes

These are potential future enhancements, not claims about existing functionality.

## 12. Key Engineering Takeaways

This module demonstrated that an agentic AI workflow involves more than prompting an LLM.

It requires coordination of multiple model calls, management of intermediate outputs, reliable error propagation, clear software interfaces, and testable application behavior.

The most important lessons were:

1. **Orchestration:** Multiple LLM calls can be composed into a coherent workflow.
2. **Reflection:** A critique stage can provide feedback for improving generated output.
3. **Separation of concerns:** Prompting, workflow control, API communication, and persistence should remain independent.
4. **Dependency injection:** Abstract interfaces allow realistic testing without external API calls.
5. **Reliability:** Errors must propagate predictably, and invalid responses must be rejected.
6. **Testing:** Agentic applications require deterministic software tests in addition to qualitative evaluation of model output.

## 13. Acknowledgment

This project is an educational derivative inspired by the reflection workflow presented in Andrew Ng and DeepLearning.AI's **Agentic AI** course.

Course: https://www.deeplearning.ai/courses/agentic-ai/

The underlying workflow concepts originate from the course. The modular architecture, workflow integration, persistence implementation, exception handling, and automated tests represent additional engineering work completed while studying the material.

This repository is an independent learning implementation and is not an official DeepLearning.AI project.
