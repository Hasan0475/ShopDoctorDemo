# ShopDoctor — developer shortcuts
# Usage: make <target>

.PHONY: help install backend-install frontend-install dev backend frontend test lint docker-up docker-down clean

help:
	@echo "install          Install backend + frontend dependencies"
	@echo "backend          Run FastAPI dev server on :8000"
	@echo "frontend         Run Vite dev server on :5173"
	@echo "test             Run backend tests"
	@echo "docker-up        Build & run the full stack via docker compose"
	@echo "docker-down      Stop docker compose stack"
	@echo "clean            Remove build artefacts and local DB"

install: backend-install frontend-install

backend-install:
	cd backend && python -m venv .venv && . .venv/bin/activate 2>/dev/null || . .venv/Scripts/activate; pip install -r requirements.txt

frontend-install:
	cd frontend && npm install

backend:
	cd backend && (uvicorn app.main:app --reload --port 8000 || .venv/Scripts/python.exe -m uvicorn app.main:app --reload --port 8000)

frontend:
	cd frontend && npm run dev

test:
	cd backend && python -m pytest -q

docker-up:
	docker compose up --build

docker-down:
	docker compose down

clean:
	rm -f backend/shopdoctor.db
	rm -rf frontend/dist frontend/node_modules/.vite
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
