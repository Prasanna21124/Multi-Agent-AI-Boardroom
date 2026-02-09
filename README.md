# Multi-Agent AI Startup Strategy Engine

AI Boardroom Agent is an AI-powered full-stack web application that simulates a virtual boardroom of specialized AI agents to analyze startup ideas and generate structured business execution strategies.

Built using:

- FastAPI
- LangChain + LangGraph
- OpenAI API
- SQLite
- HTML, CSS, JavaScript

---

# Problem Statement

Entrepreneurs and students often struggle to:

- Transform vague startup ideas into structured plans
- Identify technical and business risks early
- Choose the correct technology stack
- Understand market positioning
- Break down execution into actionable steps

Most AI tools generate generic responses without structured role-based thinking.

---

# Solution Overview

AI Boardroom Agent simulates a structured boardroom environment consisting of multiple AI agents, each responsible for a specific role:

| Agent | Responsibility |
|--------|----------------|
| Clarifier Agent | Refines and structures the raw idea |
| Planning Agent | Creates a detailed execution roadmap |
| Risk Analyst | Identifies potential risks and challenges |
| Technical Strategist | Recommends tools and architecture |
| Market Analyst | Evaluates market positioning |

Each agent executes sequentially using **LangGraph workflow orchestration**, passing structured state between steps.

---

# System Architecture

## Frontend
- Custom HTML, CSS, JavaScript
- Chat-style user interface
- Structured AI output rendering
- Conversation history rendering

## Backend
- FastAPI
- Modular router-based architecture
- LangChain for prompt management
- LangGraph for multi-step agent workflow
- OpenAI LLM integration
- SQLite database for persistence

## Database
- SQLAlchemy ORM
- Stores conversation history
- Persistent session storage

---

# Vector Store

To enhance contextual intelligence, the system integrates a vector-based memory layer.

## Purpose

The vector store enables:

- Retrieval of semantically similar past ideas
- Context-aware AI responses
- Persistent memory across sessions
- Improved strategy consistency

Instead of treating each request independently, the system injects relevant historical context into the AI workflow.

## Technologies Used

- OpenAI Embeddings
- LangChain VectorStore abstraction
- Local vector storage (FAISS / In-memory store)
- Memory injection into LangGraph state

---

## Memory Injection Flow

```
User Input
    ↓
Generate Embedding
    ↓
Search Similar Documents
    ↓
Inject memory_context into LangGraph state
    ↓
Multi-agent execution
```

---

# AI Workflow (LangGraph Execution Flow)

```
User Input
        ↓
Clarifier Agent
        ↓
Planning Agent
        ↓
Risk Analyst
        ↓
Technical Strategist
        ↓
Market Analyst
        ↓
Structured Response
        ↓
Stored in SQLite Database
```

LangGraph manages:
- State propagation
- Sequential agent execution
- Structured output aggregation

---

# Project Structure

```
Full-Stack-AI-Agent/
│
├── backend/
│   ├── main.py
│   ├── graph.py
│   ├── prompt.py
│   ├── routers/
│   │   ├── plan.py
│   │   ├── health.py
│   ├── db/
│   │   ├── database.py
│   │   ├── models.py
│   ├── conversations.db
│   ├── vector/
│       ├── vector_store.py
├── frontend/
│   ├── index.html
│
│
├── README.md
├── requirements.txt
├── .gitignore
```


# Database Design

SQLite database stores:

- User Input
- Clarified Idea
- Execution Plan
- Risk Analysis
- Tools Recommendation
- Market Analysis
- Timestamp

This ensures conversation persistence even after refreshing the page.

---

# Technical Highlights

- Multi-agent orchestration using LangGraph
- Structured prompt engineering
- State management across agents
- Modular FastAPI router architecture
- Persistent database storage
- Text input

---
