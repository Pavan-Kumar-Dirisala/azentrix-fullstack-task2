# 🔬 Multi-Agent Research Assistant

A LangGraph-powered Multi-Agent Research System that automatically performs deep research, validates sources, generates comprehensive reports, reviews report quality, and iteratively improves outputs through a feedback-driven rewrite loop.

Built as part of the Azentrix Digital Services Generative AI Internship Assessment (Task 2).

---

## 📌 Problem Statement

Single-prompt LLM calls often struggle with complex multi-step research tasks.

This project solves that problem by using a team of specialized AI agents that collaborate through an orchestrated workflow to:

* Plan research
* Search for information
* Validate sources
* Summarize findings
* Write reports
* Review report quality
* Rewrite reports based on reviewer feedback

---

## 🏗️ System Architecture

![Architecture Diagram](images/architecture.jpg)

---

## 🤖 Agents

### 1. Planner Agent

**Role**

Breaks the user's query into focused research subtopics.

**Input**

* User query

**Output**

* Research goal
* Search-friendly subtopics

---

### 2. Search Agent

**Role**

Collects information from the web using DuckDuckGo Search.

**Features**

* Domain filtering
* Source prioritization
* Multi-topic research

**Output**

* Search results

---

### 3. Validation Agent

**Role**

Filters low-quality or irrelevant search results.

**Features**

* Rule-based validation
* Keyword relevance checking
* Content quality filtering

**Output**

* Validated search results

---

### 4. Summariser Agent

**Role**

Creates concise summaries for each research topic.

**Features**

* Parallel execution
* Topic-level summarization
* Source preservation

**Output**

* Topic summaries

---

### 5. Writer Agent

**Role**

Generates a professional research report using validated summaries.

**Output**

* Title
* Executive Summary
* Full Report
* References

---

### 6. Reviewer Agent

**Role**

Evaluates report quality and provides feedback.

**Evaluation Criteria**

* Completeness
* Accuracy
* Depth of Analysis
* Structure
* Clarity
* References

**Output**

* Score
* Approval Status
* Feedback

---

## 🔄 Rewrite Loop

If the reviewer rejects the report:

1. Reviewer feedback is sent back to the Writer Agent.
2. The Writer Agent revises the report.
3. The Reviewer Agent evaluates the revised report.
4. The process repeats until approval or the maximum rewrite attempts are reached.

This avoids expensive re-search and re-summarization while improving report quality.

---

## 🧠 Tech Stack

### Frameworks

* LangGraph
* LangChain
* Streamlit

### LLMs

* GPT-5
* GPT-5 Mini

### Search

* DuckDuckGo Search

### Validation

* Rule-Based Validation Engine

### Output

* PDF Export
* JSON Export

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
├── images/
│   ├── architecture.jpg
│   ├── llm_report.png
│   ├── llm_review.png
│   ├── llm_timeline.png
│   ├── ai_software_report.png
│   ├── ai_software_review.png
│   ├── ai_software_timeline.png
│   ├── quantum_report.png
│   ├── quantum_review.png
│   └── quantum_timeline.png
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
git clone https://github.com/Pavan-Kumar-Dirisala/azentrix-fullstack-task2.git

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

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
```

---

## 🚀 Run Application

```bash
streamlit run main.py
```

---

## 📸 Example Runs

The system was tested across multiple research domains to validate the effectiveness of the multi-agent workflow.

---

### Example 1 — Recent Advancements in Large Language Models

**Input**

```text
Recent advancements in Large Language Models (LLMs)
```

#### Research Report

![LLM Report](images/llm_report.png)

#### Quality Review

![LLM Review](images/llm_review.png)

#### Execution Timeline

![LLM Timeline](images/llm_timeline.png)

---

### Example 2 — Impact of AI on Software Development and Engineering

**Input**

```text
What is the impact of AI on software development and software engineering?
```

#### Research Report

![AI Software Report](images/ai_software_report.png)

#### Quality Review

![AI Software Review](images/ai_software_review.png)

#### Execution Timeline

![AI Software Timeline](images/ai_software_timeline.png)

---

### Example 3 — Present and Future Applications of Quantum Computing

**Input**

```text
What are the current and future applications of quantum computing?
```

#### Research Report

![Quantum Report](images/quantum_report.png)

#### Quality Review

![Quantum Review](images/quantum_review.png)

#### Execution Timeline

![Quantum Timeline](images/quantum_timeline.png)

---

## 📄 Output Formats

The system supports:

* PDF Report Export
* JSON Export
* Interactive Streamlit Dashboard

---

## 🔮 Future Improvements

* Academic database integration
* Citation generation
* Multiple search providers
* Human-in-the-loop review
* Vector database memory
* Agent performance analytics
* Automated source credibility scoring
* Research gap detection and auto re-search

---

## 🎥 Demo Video

**Loom Demo:**
(Add Loom Video Link Here)

---

## 📝 DESIGN DOCUMENT

A detailed explanation of the system architecture, design decisions, challenges, trade-offs, and future improvements is available in:

```text
DESIGN.md
```

---

## 👨‍💻 Author

**Pavan Kumar Dirisala**

Generative AI Internship Assessment
Azentrix Digital Services
