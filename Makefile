.PHONY: install install-backend install-frontend dev dev-backend dev-frontend test docker-up docker-down

install: install-backend install-frontend

install-backend:
	pip install -r backend/requirements.txt

install-frontend:
	cd frontend && npm install

dev: dev-backend

dev-backend:
	uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend:
	cd frontend && npm run dev

test:
	cd backend && pytest -q

docker-up:
	docker compose up --build

docker-down:
	docker compose down
