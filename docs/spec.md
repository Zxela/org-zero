# 🧠 Org-Zero: AI Agent Network

Org-Zero replaces a traditional software development organization with a coordinated network of AI agents. Each agent is specialized and collaborates asynchronously via Redis Pub/Sub to accomplish tasks end-to-end—from user prompt to GitHub artifact.

## 🎯 Objective

Automate the full software delivery pipeline using AI agents:
- Accept multimodal input (text, voice, images)
- Orchestrate tasks using event-driven workflows
- Output source artifacts committed to GitHub

## 🧩 Architecture Overview

### Input Layer
- `FastAPI` web server receives user input at `/chat`
- Multi-modal support (text for now, extendable to voice/images)
- Director agent handles all human interaction

### Orchestration Layer
Agents communicate via Redis Pub/Sub:
- `director` publishes to `pm:task`
- `pm` delegates to `dev-implementor`, `designer`, `devops`, etc.
- `dev-implementor` pushes code
- `dev-reviewer` reviews
- `pm` aggregates results and reports back to `director`
- `director` responds to the user

### Output Layer
- Code and other artifacts committed to GitHub using GitHub API

## 🧠 Agent Roles

| Agent             | Purpose                                      |
|-------------------|----------------------------------------------|
| `director`        | Entry point, user-facing orchestrator        |
| `pm`              | Delegates tasks, tracks progress             |
| `designer`        | Creates wireframes and UX flows              |
| `dev-implementor` | Writes and commits application code          |
| `dev-reviewer`    | Reviews code from implementor                |
| `devops`          | Manages infra code (Terraform, CI/CD, etc.)  |
| `sales`           | Handles pricing strategy, positioning, growth|

## ⚙️ Tech Stack

- **Language**: Python 3.12+
- **Runtime**: Docker Compose
- **Infra**:
  - Redis for Pub/Sub (inter-agent messaging)
  - PostgreSQL (planned for structured task tracking)
- **Model Inference**: OpenRouter (configurable via `.env`)
- **Web Interface**: FastAPI

## 🗂️ Directory Structure

```bash
.
├── agents/
│   ├── director/
│   ├── pm/
│   ├── dev-implementor/
│   ├── dev-reviewer/
│   ├── designer/
│   ├── devops/
│   └── sales/
├── core/
│   ├── agents/
│   ├── events/
│   ├── models/
│   ├── logging.py
│   └── config.py
├── interfaces/
│   └── api/
│       └── main.py
├── scripts/
│   └── run_pm.py (and other runners)
├── docker-compose.yml
├── Makefile
├── .env
└── requirements.txt
```

## Current Features
- FastAPI endpoint (/chat) to send prompts
- Director agent creates task description
- ProjectManager agent subscribes to pm:task
- Dev agent subscribes to dev-implementor:task
- Tasks passed downstream and simulated "commits" printed
- Redis Pub/Sub wiring complete
- Configurable model backend via .env

