.PHONY: install dev test lint fmt run

install:
	pip install -r requirements.txt -r requirements-dev.txt

dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest

lint:
	ruff check app tests

fmt:
	ruff format app tests

run:
	docker compose up --build
