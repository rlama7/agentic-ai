# SQL Generation with Reflection

A portfolio project demonstrating an **agentic SQL workflow** that converts natural-language questions into SQLite queries, executes them safely, evaluates real query results, and iteratively refines incorrect SQL using an LLM.

This project was inspired by the **Reflection Design Pattern** demonstrated in Andrew Ng's [Agentic AI course](https://www.deeplearning.ai/courses/agentic-ai/). The original course lab introduces a SQL generation workflow that improves a first-pass query using reflection and execution feedback.

This implementation extends that concept into a more modular, testable, and safety-conscious local Python application.

---

## Project Goals

The project explores how an LLM-powered workflow can move beyond:

```text
Prompt -> Answer
```

and instead use an agentic loop:

```text
Generate
   ↓
Execute
   ↓
Observe
   ↓
Reflect
   ↓
Refine
   ↓
Repeat if necessary
```

The main learning goals are:

- Generate SQL from natural-language questions.
- Ground SQL generation in the actual database schema.
- Provide business/domain semantics to the LLM.
- Execute generated SQL against a real SQLite database.
- Use execution output as external feedback.
- Reflect on incorrect or incomplete results.
- Iteratively refine SQL until the result is correct or a retry limit is reached.
- Prevent unsafe database mutations.
- Preserve workflow history for debugging and observability.
- Unit test deterministic workflow behavior without making live LLM calls.

---

# High-Level Architecture

```text
                            ┌─────────────────────┐
                            │    User Question    │
                            └──────────┬──────────┘
                                       │
                                       ▼
                            ┌─────────────────────┐
                            │     workflow.py     │
                            │   Orchestration     │
                            └──────────┬──────────┘
                                       │
                    ┌──────────────────┴──────────────────┐
                    │                                     │
                    ▼                                     ▼
          ┌───────────────────┐                 ┌───────────────────┐
          │       db.py       │                 │ sql_generator.py  │
          │                   │                 │                   │
          │ Schema discovery  │                 │ Natural language  │
          │ Domain semantics  │                 │       -> SQL      │
          │ SQL execution     │                 └─────────┬─────────┘
          └─────────┬─────────┘                           │
                    │                                     ▼
                    │                           ┌───────────────────┐
                    │                           │   llm_client.py   │
                    │                           │                   │
                    │                           │   OpenAI client   │
                    │                           └───────────────────┘
                    │
                    ▼
          ┌───────────────────┐
          │   validator.py    │
          │                   │
          │ Read-only SQL     │
          │ safety gate       │
          └─────────┬─────────┘
                    │
                    ▼
          ┌───────────────────┐
          │      SQLite       │
          │   products.db     │
          └─────────┬─────────┘
                    │
                    ▼
          ┌───────────────────┐
          │ Pandas DataFrame  │
          │ execution result  │
          └─────────┬─────────┘
                    │
                    ▼
          ┌───────────────────┐
          │   reflection.py   │
          │                   │
          │ Evaluate result   │
          │ + refine SQL      │
          └─────────┬─────────┘
                    │
             correct?
             ┌──────┴──────┐
             │             │
            Yes            No
             │             │
             ▼             ▼
           Finish      Retry with
                       refined SQL
```

---

# Project Structure

```text
sql-generation/
├── data/
│   └── products.db
│
├── src/
│   ├── __init__.py
│   ├── db.py
│   ├── llm_client.py
│   ├── reflection.py
│   ├── sql_generator.py
│   ├── validator.py
│   └── workflow.py
│
├── tests/
│   ├── test_db.py
│   ├── test_validator.py
│   └── test_workflow.py
│
├── .env
├── .env.example
├── main.py
├── requirements.txt
└── README.md
```

Repository-level Python tooling is configured from the root `agentic-ai/` project using:

```text
agentic-ai/
├── .vscode/
│   └── settings.json
└── pyproject.toml
```

---

# Module Responsibilities

## `main.py`

Application entry point.

Responsibilities:

- Define the user question.
- Invoke the SQL workflow.
- Print workflow attempts and final status.

`main.py` intentionally does **not** contain database, validation, LLM, or reflection logic.

---

## `src/db.py`

Database infrastructure layer.

Responsibilities:

- Connect to SQLite.
- Return the `transactions` table schema.
- Extract useful database semantics.
- Execute validated SQL.
- Return SQL results as Pandas DataFrames.

Example schema exposed to the agent:

```text
table name: transactions
id (INTEGER)
product_id (INTEGER)
product_name (TEXT)
brand (TEXT)
category (TEXT)
color (TEXT)
action (TEXT)
qty_delta (INTEGER)
unit_price (REAL)
notes (TEXT)
ts (DATETIME)
```

The application also provides semantic context such as:

```text
Valid action values:
insert
price_update
restock
sale

sale:
qty_delta < 0

insert / restock:
qty_delta > 0

price_update:
qty_delta = 0
```

This semantic grounding became important because schema types alone do not explain the business meaning of the data.

---

## `src/llm_client.py`

Centralized LLM communication.

Responsibilities:

- Load environment variables.
- Read `OPENAI_API_KEY`.
- Initialize the OpenAI client.
- Provide a reusable `get_response()` abstraction.
- Handle LLM API errors.

This keeps OpenAI-specific implementation details out of the SQL generator and reflection modules.

---

## `src/sql_generator.py`

Initial SQL generation.

Inputs:

```text
User question
+
Database schema
+
Database semantics
```

Output:

```text
SQL V1
```

The generator is instructed to:

- Use SQLite syntax.
- Query only the `transactions` table.
- Generate a read-only `SELECT`.
- Return SQL only.
- Avoid markdown code fences and explanations.

Example:

```text
User:
Which color of product has the highest total sales?
```

Possible generated SQL:

```sql
SELECT
    color,
    SUM(-qty_delta * unit_price) AS total_sales
FROM transactions
WHERE action = 'sale'
GROUP BY color
ORDER BY total_sales DESC
LIMIT 1;
```

---

## `src/validator.py`

Safety boundary between the LLM and SQLite.

The current implementation only permits read-only `SELECT` queries.

Examples:

```sql
SELECT * FROM transactions;
```

Allowed.

```sql
DELETE FROM transactions;
```

Rejected.

```sql
DROP TABLE transactions;
```

Rejected.

```sql
UPDATE transactions SET ...;
```

Rejected.

Unsafe SQL returns an error DataFrame instead of mutating the database.

---

## `src/reflection.py`

Reflection and evaluation layer.

Inputs:

```text
Original user question
+
Database schema
+
Database semantics
+
Current SQL query
+
Actual SQL execution result
```

Structured output:

```json
{
  "is_correct": false,
  "feedback": "Explanation of the issue",
  "refined_sql": "Improved SELECT query"
}
```

This allows the application to distinguish between:

```text
Human-readable feedback
```

and:

```text
Machine-executable refined SQL
```

---

## `src/workflow.py`

Agentic orchestration layer.

Responsibilities:

- Discover schema.
- Load database semantics.
- Generate SQL V1.
- Execute SQL.
- Pass execution output to reflection.
- Store attempt history.
- Retry with refined SQL.
- Stop when correct.
- Stop safely after a maximum number of attempts.

Default maximum:

```text
3 reflection attempts
```

This prevents uncontrolled agent loops.

---

# Workflow Design

The core execution loop is:

```text
1. Extract database schema
2. Extract database semantics
3. Generate initial SQL
4. Validate SQL
5. Execute SQL
6. Observe result
7. Reflect on result
8. Determine correctness
9. Refine if necessary
10. Repeat until success or max attempts
```

Pseudocode:

```text
schema = get_schema()
context = get_database_context()

sql = generate_sql(question, schema, context)

for attempt in max_attempts:
    result = execute_sql(sql)

    correct, feedback, refined_sql =
        reflect(question, sql, result, schema, context)

    save_attempt(sql, result, feedback, correct)

    if correct:
        return success

    sql = refined_sql

return failure
```

---

# Structured Workflow History

Each workflow attempt is preserved using a dataclass.

Conceptually:

```text
WorkflowResult
├── question
├── succeeded
└── attempts
    ├── Attempt 1
    │   ├── SQL
    │   ├── result
    │   ├── feedback
    │   └── is_correct
    │
    ├── Attempt 2
    └── Attempt 3
```

This enables:

- debugging,
- testing,
- execution tracing,
- future UI rendering,
- side-by-side V1/V2/V3 comparisons,
- portfolio demonstrations.

---

# Reflection Example

An early version of the workflow generated:

```sql
SELECT color, SUM(qty_delta * unit_price) AS total_sales
FROM transactions
WHERE action = 'sale'
GROUP BY color
ORDER BY total_sales DESC
LIMIT 1;
```

Result:

```text
color    total_sales
blue     -190571.46
```

The SQL was:

```text
syntactically valid
```

and:

```text
successfully executed
```

but:

```text
semantically incorrect
```

because sale events use negative `qty_delta`.

This illustrates an important concept:

```text
SQL syntax correctness
        !=
Business logic correctness
        !=
User-intent correctness
```

After database semantics were provided to the model, it generated a correct revenue calculation such as:

```sql
SELECT
    color,
    SUM(-qty_delta * unit_price) AS total_sales
FROM transactions
WHERE action = 'sale'
GROUP BY color
ORDER BY total_sales DESC
LIMIT 1;
```

Result:

```text
color    total_sales
white    358315.09
```

Reflection then confirmed the result as correct.

---

# Why External Feedback Matters

Reviewing SQL text alone may not reveal semantic problems.

Static review:

```text
Question
+
SQL
+
Schema
```

can still miss domain-specific behavior.

External-feedback reflection adds:

```text
Actual query execution result
```

which changes the evaluation to:

```text
Question
+
SQL
+
Schema
+
Database semantics
+
Real execution output
```

This allows the model to reason about what **actually happened**, not only what the query appears likely to do.

---

# Enhancements Beyond the Course Lab

The original Agentic AI lab demonstrates:

```text
Generate V1
→ Execute V1
→ Reflect
→ Generate V2
→ Execute V2
```

This portfolio implementation extends that workflow.

## 1. Bounded Iterative Reflection

Course-style flow:

```text
V1
→ V2
→ stop
```

Enhanced flow:

```text
V1
→ evaluate
→ V2
→ evaluate
→ V3
→ ...
→ stop at success or max attempts
```

This allows the workflow to recover when the first refinement is also incorrect.

---

## 2. Explicit Correctness Decision

Reflection returns:

```json
{
  "is_correct": true,
  "feedback": "...",
  "refined_sql": "..."
}
```

The workflow does not need to infer correctness from free-form feedback.

---

## 3. Database Semantic Grounding

The workflow provides not only schema structure but also business meaning.

Example:

```text
action = sale
qty_delta is negative for sale events
sales revenue uses positive quantity magnitude
```

This prevents the LLM from guessing domain-specific values such as:

```text
sell
```

instead of the actual database value:

```text
sale
```

---

## 4. Read-Only SQL Guardrail

Generated SQL passes through a validation layer before execution.

Unsafe mutation queries are rejected.

Example:

```sql
DELETE FROM transactions;
```

becomes:

```text
Only SELECT queries are allowed.
```

instead of reaching SQLite.

---

## 5. Structured Attempt History

Every attempt records:

```text
attempt number
SQL query
execution result
reflection result
feedback
```

This improves observability and testability.

---

## 6. Modular Architecture

The notebook workflow was separated into reusable modules:

```text
DB
LLM client
SQL generator
validator
reflection
workflow
presentation
```

This makes responsibilities easier to understand and test independently.

---

## 7. Deterministic Unit Testing

Live LLM calls are intentionally avoided in unit tests.

`unittest.mock.patch` replaces:

```text
generate_sql()
reflect_on_sql()
```

with predictable fake responses.

This allows the retry logic to be tested deterministically.

---

## 8. Failure-Path Testing

The test suite validates:

- successful refinement,
- bounded retries,
- unsuccessful workflows,
- unsafe generated SQL,
- database schema/context,
- read-only validation.

---

## 9. Python Tooling

The portfolio repository uses:

```text
Pylance
→ type analysis / IntelliSense

Ruff
→ linting / formatting / import management

pytest
→ behavioral testing
```

Python source uses conventional:

```text
4-space indentation
```

and shared Ruff configuration is maintained at the repository root.

---

# Tests

Current test suite:

```text
tests/test_db.py
tests/test_validator.py
tests/test_workflow.py
```

At the completion of this module:

```text
10 tests passing
```

Run:

```bash
python -m pytest
```

Expected:

```text
10 passed
```

Run linting:

```bash
python -m ruff check . --fix
```

Expected:

```text
All checks passed!
```

---

# Setup

From:

```text
agentic-ai/apps/python/sql-generation
```

create a virtual environment:

```bash
python3.11 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

---

# Environment Variables

Create:

```text
.env
```

with:

```text
OPENAI_API_KEY=<your-key>
```

Do not commit `.env`.

The repository-level `.gitignore` excludes:

```text
.env
.env.*
```

while allowing:

```text
.env.example
```

to remain in source control.

---

# Run the Demo

From:

```text
apps/python/sql-generation
```

run:

```bash
python main.py
```

Example question:

```text
Which color of product has the highest total sales?
```

Example successful workflow:

```text
Attempt 1

SQL:
SELECT color,
       SUM(-qty_delta * unit_price) AS total_sales
FROM transactions
WHERE action = 'sale'
GROUP BY color
ORDER BY total_sales DESC
LIMIT 1;

Result:
color    total_sales
white    358315.09

Reflection Correct?:
True

Workflow Success:
True
```

---

# Key Lessons

## Valid code does not guarantee a correct answer

A SQL statement can be:

```text
syntactically valid
```

and:

```text
successfully executed
```

while still producing a result that violates business semantics.

---

## Execution is a source of feedback

Agentic workflows become more reliable when the model can observe the results of its actions.

```text
Generate
→ Execute
→ Observe
→ Reflect
→ Improve
```

is more powerful than:

```text
Prompt
→ Answer
```

---

## Reflection requires good context

The reflection loop initially failed because the database schema only described:

```text
action (TEXT)
qty_delta (INTEGER)
```

It did not explain:

```text
sale is the valid action value
sale quantities are negative
```

Adding domain semantics dramatically improved model performance.

---

## Agent loops require boundaries

Reflection should not run forever.

The workflow therefore uses:

```text
MAX_ATTEMPTS = 3
```

to guarantee bounded execution.

---

## LLMs should not directly control mutable systems

The model proposes SQL.

The application decides whether that SQL is safe enough to execute.

```text
LLM
↓
SQL proposal
↓
Validator
↓
Database
```

This separation is an important agentic-system design principle.

---

# Limitations

This is an educational portfolio implementation rather than a production SQL agent.

Current limitations include:

- SQL safety validation is intentionally lightweight.
- Reflection correctness is still ultimately judged by an LLM.
- SQLite is the only supported database.
- No schema relationships or joins are currently required.
- No authentication or multi-user model exists.
- No UI/API layer has been added.
- LLM generation is non-deterministic during live runs.
- Database semantic descriptions are tailored to the current dataset.

Possible future enhancements:

- SQL AST/parser-based safety validation.
- SQLite enforced read-only connections.
- deterministic domain validators,
- richer observability / traces,
- token and latency metrics,
- CLI arguments,
- FastAPI API layer,
- frontend visualization,
- multi-database adapters,
- confidence scoring,
- evaluation datasets,
- integration tests,
- model comparison experiments.

---

# Attribution

This project is inspired by and builds upon concepts taught in:

**Andrew Ng — Agentic AI**

DeepLearning.AI  
https://www.deeplearning.ai/courses/agentic-ai/

The course lab demonstrates the **Reflection Design Pattern** by generating SQL, executing it, evaluating the result, and refining the query using feedback.

This portfolio implementation was independently reorganized and extended with:

- modular local Python architecture,
- database semantic grounding,
- bounded iterative reflection,
- explicit correctness decisions,
- SQL safety validation,
- structured workflow history,
- deterministic mocked LLM tests,
- failure-path testing,
- Ruff linting/formatting,
- and portfolio-oriented documentation.

---

# Status

```text
SQL generation            ✅
SQLite execution          ✅
Database semantic context ✅
Reflection                ✅
Iterative refinement      ✅
Read-only SQL validation  ✅
Structured attempt history ✅
Unit tests                ✅
Ruff linting              ✅
Portfolio documentation   ✅
```
