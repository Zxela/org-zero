# Makefile

# Variables
VENV ?= .venv
PYTHON := python3
PIP := $(VENV)/bin/pip
REDIS_URL := localhost
REDIS_PORT := 6379
POSTGRES_URL := localhost
POSTGRES_PORT := 5432

.PHONY: all setup install check run-pm run-api run-dev start-redis start-postgres clean test test-file run-designer run-reviewer run-sales run-devops

all: install

# =====================
# 🛠️  Setup & Install
# =====================
setup:
	@echo "🔧 Checking virtual environment..."
	@test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	@echo "✅ Virtual environment created at $(VENV)"
	@test -f $(PIP) || ( \
		echo "⚠️ pip not found. Attempting to install..."; \
		$(PYTHON) -m ensurepip --upgrade; \
		$(PYTHON) -m venv --upgrade-deps $(VENV); \
	)
	@echo "📦 Using Python: $$($(VENV)/bin/python --version)"

install: setup
	@echo "📦 Installing dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "✅ Dependencies installed"

check:
	@echo "🔎 Checking Redis availability..."
	@timeout 1 bash -c "</dev/tcp/$(REDIS_URL)/$(REDIS_PORT)" || (echo "❌ Redis not reachable at $(REDIS_URL):$(REDIS_PORT). Run `make start-redis` or install Redis locally."; exit 1)
	@echo "✅ Redis is online."
	@echo "🔎 Checking PostgreSQL availability..."
	@timeout 1 bash -c "</dev/tcp/$(POSTGRES_URL)/$(POSTGRES_PORT)" || (echo "❌ PostgreSQL not reachable at $(POSTGRES_URL):$(POSTGRES_PORT). Run `make start-postgres` or install PostgreSQL locally."; exit 1)
	@echo "✅ PostgreSQL is online."

# =====================
# 🚀 Run Agents & API
# =====================
run-pm: install check
	@echo "👷 Starting PM Agent..."
	PYTHONPATH=. $(VENV)/bin/python scripts/run_pm.py

run-implementor: install check
	@echo "👷 Starting Implementor Agent..."
	PYTHONPATH=. $(VENV)/bin/python scripts/run_implementor.py

run-api: install check
	@echo "🚀 Starting FastAPI server..."
	PYTHONPATH=. $(VENV)/bin/uvicorn interfaces.api.main:app --reload

run-designer: install check
	@echo "🎨 Starting Designer Agent..."
	PYTHONPATH=. $(VENV)/bin/python agents/designer/agent.py

run-reviewer: install check
	@echo "🔍 Starting Reviewer Agent..."
	PYTHONPATH=. $(VENV)/bin/python agents/reviewer/agent.py

run-devops: install check
	@echo "🔧 Starting DevOps Agent..."
	PYTHONPATH=. $(VENV)/bin/python agents/devops/agent.py

run-sales: install check
	@echo "💼 Starting Sales Agent..."
	PYTHONPATH=. $(VENV)/bin/python agents/sales/agent.py

# Run all main agents for local dev (backgrounded)
run-dev: install check
	@echo "🚀 Starting dev environment: PM, API, Designer, Reviewer (backgrounded)"
	@echo "Tip: Use 'ps' or 'jobs' to see running processes. Use 'make clean' to stop all if needed."
	@echo "👉 Starting PM Agent..."
	@PYTHONPATH=. $(VENV)/bin/python scripts/run_pm.py & \
	sleep 1 && \
	echo "👉 Starting API server..." && \
	PYTHONPATH=. $(VENV)/bin/uvicorn interfaces.api.main:app --reload & \
	echo "👉 Starting Designer Agent..." && \
	PYTHONPATH=. $(VENV)/bin/python agents/designer/agent.py & \
	echo "👉 Starting Reviewer Agent..." && \
	PYTHONPATH=. $(VENV)/bin/python agents/reviewer/agent.py & \
	wait

# =====================
# 🧪 Testing
# =====================
test: install
	@echo "🧪 Running all unit tests..."
	$(VENV)/bin/python -m unittest discover -s . -p '*_test.py'

test-designer: install
	@echo "🧪 Running DesignerAgent unit tests..."
	$(VENV)/bin/python -m unittest tests/agents/designer/designer_agent_test.py

test-reviewer: install
	@echo "🧪 Running ReviewerAgent unit tests..."
	$(VENV)/bin/python -m unittest tests/agents/reviewer/reviewer_agent_test.py

test-devops: install
	@echo "🧪 Running DevOpsAgent unit tests..."
	$(VENV)/bin/python -m unittest tests/agents/devops/devops_agent_test.py

test-sales: install
	@echo "🧪 Running SalesAgent unit tests..."
	$(VENV)/bin/python -m unittest tests/agents/sales/sales_agent_test.py

# Usage: make test-file FILE=path/to/your_test_file.py
# Example: make test-file FILE=tests/agents/pm/pm_agent_test.py
test-file: install
	@echo "🧪 Running unit test file: $(FILE) ..."
	$(VENV)/bin/python -m unittest $(FILE)

# Ensure test discovery works by adding __init__.py to test directories
	find . -type d -name 'agents' -exec touch {}/__init__.py \;
	find . -type d -name 'interfaces' -exec touch {}/__init__.py \;
	find . -type d -name 'tests' -exec touch {}/__init__.py \;

# =====================
# 🐳 Docker & Clean
# =====================
start-redis:
	@echo "🐳 Launching Redis container on port 6379..."
	docker run --rm -d -p 6379:6379 --name redis-dev redis:7-alpine
	@echo "✅ Redis is running in Docker (container: redis-dev)"

start-postgres:
	@echo "🐘 Launching PostgreSQL container on port 5432..."
	docker run --rm -d -p 5432:5432 --name postgres-dev -e POSTGRES_USER=agent -e POSTGRES_PASSWORD=secret -e POSTGRES_DB=agentnet postgres:15
	@echo "✅ PostgreSQL is running in Docker (container: postgres-dev)"

stop-postgres:
	@echo "🛑 Stopping PostgreSQL container..."
	docker stop postgres-dev || true
	@echo "✅ PostgreSQL container stopped."

clean:
	@echo "🧹 Cleaning up..."
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -r {} +
