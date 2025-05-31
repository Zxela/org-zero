# Makefile

# Variables
VENV ?= .venv
PYTHON := python3
PIP := $(VENV)/bin/pip
REDIS_URL := localhost
REDIS_PORT := 6379

.PHONY: all setup install check run-pm run-api run-dev start-redis clean

all: install

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
	@timeout 1 bash -c "</dev/tcp/$(REDIS_URL)/$(REDIS_PORT)" || (echo "❌ Redis not reachable at $(REDIS_URL):$(REDIS_PORT). Run \`make start-redis\` or install Redis locally."; exit 1)
	@echo "✅ Redis is online."

run-pm: install check
	@echo "👷 Starting PM Agent..."
	PYTHONPATH=. $(VENV)/bin/python scripts/run_pm.py

run-api: install check
	@echo "🚀 Starting FastAPI server..."
	PYTHONPATH=. $(VENV)/bin/uvicorn interfaces.api.main:app --reload

run-dev: install check
	@echo "🚀 Starting dev environment (PM agent + API)..."
	@echo "Tip: Use separate terminals if needed for logs."
	@echo "👉 Starting PM Agent..."
	@PYTHONPATH=. $(VENV)/bin/python scripts/run_pm.py & \
	sleep 1 && \
	echo "👉 Starting API server..." && \
	PYTHONPATH=. $(VENV)/bin/uvicorn interfaces.api.main:app --reload

start-redis:
	@echo "🐳 Launching Redis container on port 6379..."
	docker run --rm -d -p 6379:6379 --name redis-dev redis:7-alpine
	@echo "✅ Redis is running in Docker (container: redis-dev)"

clean:
	@echo "🧹 Cleaning up..."
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -r {} +
