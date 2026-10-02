# Agentic AI Chart Generation

A local Python implementation and extension of the chart-generation refelection workflow from Andrew Ng's Agentic AI course by DeepLearing.AI.

The project explores how an LLM can generate visualization code, evaluate the resulting chart using multimodal reflection, and iterateveily produce an improved version.

## Workflow

1. Load and prepare coffee sales data.
2. Ask an LLM to generate matplotlib code.
3. Execute the generated code to create V1.
4. Send the rendered chart and original code back to a multimodal LLM.
5. Receive critique and improved plotting code.
6. Execute V2 and save the refined chart.

## Architecture

```text
coffee_sales.csv
      ↓
data_loader.py
      ↓
chart_generator.py
      ↓
LLM generates V1 code
      ↓
chart_v1.png
      ↓
reflection.py
      ↓
LLM critiques V1 + generates V2
      ↓
chart_v2.png
```

## Project Structure

```
chart-generation/
├── data/
│ └── coffee_sales.csv
├── output/
├── reference/
│ └── utils.py
├── src/
│ ├── **init**.py
│ ├── chart_generator.py
│ ├── data_loader.py
│ ├── llm_client.py
│ └── reflection.py
├── .env.example
├── main.py
├── README.md
└── requirements.txt
```

## Run

Activate the virtual environment:

```
source .venv/bin/activate
```

Install dependencies:

```
python -m pip install -r requirements.txt
```

Create `.env` folder then add your `OPENAI_API_KEY`

```
OPENAI_API_KEY=
```

Run:

```
python main.py
```

## Key Concepts

- Agentic reflection
- Multimodal LLM evaluation
- Dynamic code generation
- Structured prompting
- Python orchestration
- pandas
- matplotlib
- OpenAI Responses API

## Safey Note

This demo project executes LLM-generated Python code using `exec()`.

This is intentionally kept for educational parity with the lab workflow. A production system should sandbox or validate generated code before execution.

## Acknowledgment and Enhancements

This project is based on the chart-generation reflection workflow taught in Andrew Ng’s **Agentic AI** course by DeepLearning.AI.

The original course workflow demonstrates an agentic reflection pattern:

1. Generate an initial visualization (V1) with an LLM.
2. Execute the generated plotting code.
3. Send the resulting chart back to a multimodal LLM for critique.
4. Generate improved plotting code.
5. Execute the refined version (V2).

Course: [Agentic AI — DeepLearning.AI](https://www.deeplearning.ai/courses/agentic-ai)

This repository does **not** simply reproduce the notebook implementation. I reworked the lab into a standalone, modular Python application and added several engineering refinements to make the workflow easier to understand, maintain, extend, and integrate into a broader AI/frontend portfolio.

### Enhancements added in this implementation

- **Modular application architecture**  
  Replaced the notebook-style, cell-based workflow with dedicated modules for data loading, LLM access, chart generation, reflection, and orchestration.

- **Local project structure**  
  Converted the hosted Jupyter lab into a reproducible local Python project with isolated virtual environments, dependency management, environment variables, and generated output folders.

- **Dedicated LLM client abstraction**  
  Moved model access into `llm_client.py` so chart-generation logic is decoupled from API configuration and can be swapped or extended later.

- **Custom data-loading layer**  
  Reimplemented the dataset preparation logic locally instead of relying on the course-provided `utils.py` helper.

- **Explicit code extraction pipeline**  
  Added reusable parsing logic for extracting generated Python from `<execute_python>` blocks.

- **Separated V1 execution and reflection responsibilities**  
  Split chart generation, execution, and multimodal reflection into independently understandable components.

- **Environment variable and API-key management**  
  Added `.env` / `.env.example` handling so credentials remain outside source control.

- **Error handling and validation**  
  Added validation for missing generated-code blocks, missing files, and other runtime failures.

- **Security awareness around generated code execution**  
  Documented the risk of executing LLM-generated Python with `exec()` and called out the need for sandboxing or validation in production environments.

- **Portfolio-oriented architecture**  
  Structured the project so it can later be extended with a React/TypeScript frontend, API layer, streaming responses, model selection, workflow visualization, or safer remote execution.

The course provided the underlying reflection pattern and learning exercise; the surrounding application architecture, local implementation, modularization, error handling, configuration strategy, and extensibility work were added as part of this project.

## Acknowledgment and Enhancements

This project is based on the chart-generation reflection workflow taught in Andrew Ng’s **Agentic AI** course by DeepLearning.AI.

The original course workflow demonstrates an agentic reflection pattern:

1. Generate an initial visualization (V1) with an LLM.
2. Execute the generated plotting code.
3. Send the resulting chart back to a multimodal LLM for critique.
4. Generate improved plotting code.
5. Execute the refined version (V2).

Course: [Agentic AI — DeepLearning.AI](https://www.deeplearning.ai/courses/agentic-ai)

This repository does **not** simply reproduce the notebook implementation. I reworked the lab into a standalone, modular Python application and added several engineering refinements to make the workflow easier to understand, maintain, extend, and integrate into a broader AI/frontend portfolio.

### Enhancements added in this implementation

- **Modular application architecture**  
  Replaced the notebook-style, cell-based workflow with dedicated modules for data loading, LLM access, chart generation, reflection, and orchestration.

- **Local project structure**  
  Converted the hosted Jupyter lab into a reproducible local Python project with isolated virtual environments, dependency management, environment variables, and generated output folders.

- **Dedicated LLM client abstraction**  
  Moved model access into `llm_client.py` so chart-generation logic is decoupled from API configuration and can be swapped or extended later.

- **Custom data-loading layer**  
  Reimplemented the dataset preparation logic locally instead of relying on the course-provided `utils.py` helper.

- **Explicit code extraction pipeline**  
  Added reusable parsing logic for extracting generated Python from `<execute_python>` blocks.

- **Separated V1 execution and reflection responsibilities**  
  Split chart generation, execution, and multimodal reflection into independently understandable components.

- **Environment variable and API-key management**  
  Added `.env` / `.env.example` handling so credentials remain outside source control.

- **Error handling and validation**  
  Added validation for missing generated-code blocks, missing files, and other runtime failures.

- **Security awareness around generated code execution**  
  Documented the risk of executing LLM-generated Python with `exec()` and called out the need for sandboxing or validation in production environments.

- **Portfolio-oriented architecture**  
  Structured the project so it can later be extended with a React/TypeScript frontend, API layer, streaming responses, model selection, workflow visualization, or safer remote execution.

The course provided the underlying reflection pattern and learning exercise; the surrounding application architecture, local implementation, modularization, error handling, configuration strategy, and extensibility work were added as part of this project.

## What I Changed from the Original Lab

| Course Lab                  | This Project                                                                        |
| --------------------------- | ----------------------------------------------------------------------------------- |
| Jupyter notebook cells      | Modular Python application                                                          |
| Course-provided `utils.py`  | Custom `data_loader.py`, `llm_client.py`, `chart_generator.py`, and `reflection.py` |
| Hosted notebook environment | Local VS Code + `.venv` setup                                                       |
| Hidden helper behavior      | Explicit implementation of data loading, LLM calls, parsing, and reflection         |
| Inline execution flow       | Reusable functions with clear responsibilities                                      |
| Course-managed credentials  | Local `.env` configuration                                                          |
| Minimal runtime handling    | Added validation and error handling                                                 |
| Learning-only structure     | Portfolio-ready structure designed for future React/TypeScript integration          |

This keeps the educational source clear while also demonstrating independent engineering work rather than a direct copy of the lab.
