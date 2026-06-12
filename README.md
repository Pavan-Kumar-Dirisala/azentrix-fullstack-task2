# 🔬 Multi-Agent Research Assistant

A LangGraph-powered Multi-Agent Research System that automatically performs deep research, validates sources, generates comprehensive reports, reviews report quality, and iteratively improves outputs through a feedback-driven rewrite loop.

Built as part of the Azentrix Digital Services Generative AI Internship Assessment (Task 2).

---

## 📌 Problem Statement

Single-prompt LLM calls often struggle with complex multi-step research tasks.

This project solves that problem by using a team of specialized AI agents that collaborate through an orchestrated workflow to:

- Plan research
- Search for information
- Validate sources
- Summarize findings
- Write reports
- Review report quality
- Rewrite reports based on reviewer feedback

---

## 🏗️ System Architecture

![Architecture Diagram](architecture.png)

### Workflow

User Query
↓
Planner Agent
↓
Search Agent
↓
Validation Agent
↓
Parallel Summariser Agent
↓
Writer Agent
↓
Reviewer Agent
↓
Approved?

YES → Final Report

NO → Rewrite Loop → Writer Agent → Reviewer Agent

---

## 🤖 Agents

### 1. Planner Agent

**Role**

Breaks the user's query into focused research subtopics.

**Input**

- User query

**Output**

- Research goal
- Search-friendly subtopics

---

### 2. Search Agent

**Role**

Collects information from the web using DuckDuckGo.

**Features**

- Domain filtering
- Source prioritization
- Multi-topic research

**Output**

- Search results

---

### 3. Validation Agent

**Role**

Filters low-quality or irrelevant search results.

**Features**

- Rule-based validation
- Keyword relevance checking
- Content quality filtering

**Output**

- Validated search results

---

### 4. Summariser Agent

**Role**

Creates concise summaries for each research topic.

**Features**

- Parallel execution
- Topic-level summarization
- Source preservation

**Output**

- Topic summaries

---

### 5. Writer Agent

**Role**

Generates a professional research report using validated summaries.

**Output**

- Title
- Executive Summary
- Full Report
- References

---

### 6. Reviewer Agent

**Role**

Evaluates report quality.

**Evaluation Criteria**

- Completeness
- Accuracy
- Depth
- Structure
- Clarity
- References

**Output**

- Score
- Approval Status
- Feedback

---

## 🔄 Rewrite Loop

If the reviewer rejects the report:

1. Reviewer feedback is sent back to the Writer Agent.
2. The Writer Agent revises the report.
3. The Reviewer Agent evaluates the revised report.
4. Process repeats until approval or maximum rewrite attempts are reached.

This avoids expensive re-search and re-summarization while improving report quality.

---

## 🧠 Tech Stack

### Frameworks

- LangGraph
- LangChain
- Streamlit

### LLMs

- GPT-5
- GPT-5 Mini

### Search

- DuckDuckGo Search

### Validation

- Rule-Based Validation Engine

### Output

- PDF Export
- JSON Export

---

## 📂 Project Structure

```text
Task-2/
│
├── agents/
│   ├── planning_agent.py
│   ├── searching_agent.py
│   ├── validation_agent.py
│   ├── summariser_agent.py
│   ├── writer_agent.py
│   └── reviewer_agent.py
│
├── graph/
│   ├── state.py
│   ├── nodes.py
│   └── workflow.py
│
├── prompts/
│   ├── planning_prompt.py
│   ├── summarizer_prompt.py
│   ├── writer_prompt.py
│   └── reviewer_prompt.py
│
├── tools/
│   └── search_tool.py
│
├── main.py
├── schemas.py
├── DESIGN.md
├── README.md
└── requirements.txt
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/your-username/azentrix-fullstack-task2.git

cd azentrix-fullstack-task2
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

#### Windows

```bash
.venv\Scripts\activate
```

#### Mac/Linux

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file.

```env
OPENAI_API_KEY=your_api_key_here
```

---

## 🚀 Run Application

```bash
streamlit run main.py
```

---

## 📊 Example Queries

### Example 1

```text
Impact of Trump on F1 Visa Policies
```

### Example 2

```text
Will AI Replace Software Engineers by 2035?
```

### Example 3

```text
Future of Renewable Energy Technologies
```

---

## 📸 Screenshots

### Dashboard

(Add screenshot)

### Workflow Execution

(Add screenshot)

### Generated Report

(Add screenshot)

### Review Results

(Add screenshot)

---

## 📄 Output Formats

The system can export:

- PDF Research Report
- JSON Research Data

---

## 🔮 Future Improvements

- Academic database integration
- Citation generation
- Multi-source search engines
- Human-in-the-loop review
- Vector database memory
- Agent performance analytics

---

## 🎥 Demo Video

Loom Demo:

(Add Loom Link)

---

## 👨‍💻 Author

Pavan Kumar Dirisala

Generative AI Internship Assessment
Azentrix Digital Services