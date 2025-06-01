# 🧠 Org-Zero: AI Agent Network

Org-Zero is an experimental framework that replaces a traditional software development organization with a coordinated network of AI agents. Each agent is specialized and collaborates asynchronously via Redis Pub/Sub to accomplish tasks end-to-end—from user prompt to GitHub artifact.

---

## 🚀 Objective

Automate the full software delivery pipeline using AI agents:
- Accept multimodal input (text, voice, images)
- Orchestrate tasks using event-driven workflows
- Output source artifacts committed to GitHub

---

## 🏗️ Architecture Overview

- **Input Layer:**  
  FastAPI web server receives user input at `/chat` (text for now, extendable to voice/images). The Director agent handles all human interaction.

- **Orchestration Layer:**  
  Agents communicate via Redis Pub/Sub:
  - `director` publishes to `pm:task`
  - `pm` delegates to `implementor`, `designer`, `devops`, etc.
  - `implementor` pushes code
  - `reviewer` reviews
  - `pm` aggregates results and reports back to `director`
  - `director` responds to the user

- **Output Layer:**  
  Code and other artifacts are committed to GitHub using the GitHub API.

---

## 📈 Project Progress (as of May 31, 2025)

- Core agent framework established: agents for Director, PM, Designer, Implementor, Reviewer, DevOps, and Sales are scaffolded and configured.
- Redis Pub/Sub event-driven communication implemented for agent orchestration.
- FastAPI input layer operational for text-based user prompts.
- Initial Docker and infrastructure setup complete (Dockerfile, docker-compose, Terraform scaffolding).
- Modular agent configuration and prompt templates in place for each role.
- Early tests for Director and PM agents implemented.
- Project structure and documentation improved for onboarding and contribution.

---

## 🧠 Agent Roles

| Agent             | Purpose                                      |
|-------------------|----------------------------------------------|
| `director`        | Entry point, user-facing orchestrator        |
| `pm`              | Delegates tasks, tracks progress             |
| `designer`        | Creates wireframes and UX flows              |
| `implementor`     | Writes and commits application code          |
| `reviewer`        | Reviews code from implementor                |
| `devops`          | Manages infra code (Terraform, CI/CD, etc.)  |
| `sales`           | Handles pricing strategy, positioning, growth|

---

## ⚙️ Tech Stack

- **Language:** Python 3.12+
- **Runtime:** Docker Compose
- **Infra:**  
  - Redis for Pub/Sub (inter-agent messaging)  
  - PostgreSQL (planned for structured task tracking)
- **Model Inference:** OpenRouter (configurable via `.env`)
- **Web Interface:** FastAPI

---

## 🗂️ Directory Structure

```
.
├── agents/
│   ├── director/
│   ├── pm/
│   ├── implementor/
│   ├── reviewer/
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

---

## ✨ Current Features

- FastAPI endpoint (`/chat`) to send prompts
- Director agent creates task description
- ProjectManager agent subscribes to `pm:task`
- Dev agent subscribes to `implementor:task`
- Tasks passed downstream and simulated "commits" printed
- Redis Pub/Sub wiring complete
- Configurable model backend via `.env`

---

## 📡 API Endpoints

### `POST /chat`
- **Description:** Accepts user prompts (text, extendable to multimodal).
- **Request Body:**  
  ```json
  {
    "prompt": "string"
  }
  ```
- **Response:**  
  Returns the Director agent's response and initiates the agent workflow.

---

## 🛣️ Roadmap / Work To Come

- [ ] Add support for voice and image input (multimodal)
- [ ] Integrate PostgreSQL for structured task tracking and persistence
- [ ] Implement full GitHub artifact commit pipeline
- [ ] Expand agent capabilities (e.g., more advanced code review, sales/marketing automation)
- [ ] Add web UI for monitoring and interacting with agent workflows
- [ ] Improve error handling, logging, and observability
- [ ] Add authentication and user management

---

## 🏁 Getting Started

1. Clone the repo
2. Copy `.env.example` to `.env` and configure
3. Run `docker-compose up`
4. Access the API at `http://localhost:8000/chat`

---

## 🛠️ Development

### Makefile Commands

- `make setup` — Create a Python virtual environment
- `make install` — Install dependencies into the venv
- `make run-pm` — Start the Project Manager agent
- `make run-api` — Start the FastAPI server
- `make run-dev` — Start both PM agent and API server
- `make run-designer` — Start the Designer agent
- `make run-reviewer` — Start the Reviewer agent
- `make run-devops` — Start the DevOps agent
- `make run-sales` — Start the Sales agent
- `make start-redis` — Launch Redis in Docker
- `make clean` — Remove venv and `__pycache__` folders
- `make test` — Run all unit tests in the project (recursively from root)
- `make test-designer` — Run DesignerAgent unit tests
- `make test-reviewer` — Run ReviewerAgent unit tests
- `make test-devops` — Run DevOpsAgent unit tests
- `make test-sales` — Run SalesAgent unit tests
- `make test-file FILE=path/to/test_file.py` — Run a specific test file (e.g., `make test-file FILE=agents/pm/test_agent.py`)

### Running Individual Agents

To run a specific agent (e.g., DevOps or Sales):

```powershell
# Start DevOps agent
make run-devops

# Start Sales agent
make run-sales
```

### Running Agent Unit Tests

```powershell
# Test DevOps agent
make test-devops

# Test Sales agent
make test-sales
```

---

## 🐳 Docker Compose Services

- `api` — FastAPI server
- `pm` — Project Manager agent
- `implementor` — Implementation agent
- `designer` — Designer agent
- `reviewer` — Reviewer agent
- `redis` — Redis server

---

## 🤝 Contributing

Contributions, ideas, and feedback are welcome! Please open an issue or submit a pull request.
