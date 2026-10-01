## Apply reflection to improve the LLM output

## Strategy

Load data
↓
Generate V1 plotting code with LLM
↓
Execute V1 → chart_v1.png
↓
Send chart + original code to reflection LLM
↓
Receive feedback + V2 code
↓
Execute V2 → chart_v2.png

## Table of Contents

Our new 8-step local project plan

1. Scaffold the local project structure
2. Add configuration and environment variables
3. Implement dataset loading
4. Implement the LLM client
5. Implement V1 chart-code generation
6. Implement safe extraction/execution of generated code
7. Implement image reflection and V2 generation
8. Wire everything together in main.py, run it, document it, and commit
