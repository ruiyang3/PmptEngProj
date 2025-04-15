# PmptEngProj

Hybrid Data Conversational AI

## Directory Structure

```
PmptEngProj/
├── policy_rag_assets/
├── policy_rag_utils/
├── sql_rag_assets/
├── .gitignore
├── PromptModel.py
├── compiler_agent.py
├── interface.py
├── pipeline.py
├── policy_rag_api.py
├── sql_rag_api.py
├── sub_task_formulator.py
```


## Main Components

| File/Folder | Description |
| :-- | :-- |
| `PromptModel.py` | Core prompt modeling logic |
| `compiler_agent.py` | Compiler agent for prompt processing |
| `interface.py` | Interface definitions for the project |
| `pipeline.py` | Pipeline orchestration for prompt workflows |
| `policy_rag_api.py` | API for policy RAG tasks |
| `sql_rag_api.py` | API for SQL RAG tasks |
| `sub_task_formulator.py` | Utilities for breaking down tasks into sub-tasks |
| `policy_rag_assets/` | Assets for policy RAG |
| `policy_rag_utils/` | Utilities for policy RAG |
| `sql_rag_assets/` | Assets for SQL RAG |

## Installation

1. Clone the repository:

```bash
git clone https://github.com/ruiyang3/PmptEngProj.git
cd PmptEngProj
```

2. (Optional) Create and activate a virtual environment.
3. Install dependencies (if any are specified in a requirements file).

## Usage

```bash
python interface.py
```

