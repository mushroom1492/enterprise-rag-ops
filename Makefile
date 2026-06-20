.PHONY: install test lint run docker-build docker-up ingest eval

install:
	pip install -r requirements.txt

test:
	pytest tests/

lint:
	ruff check .

run:
	uvicorn src.api.main:app --reload

docker-build:
	docker build -t enterprise-rag-ops -f infra/docker/Dockerfile .

docker-up:
	docker-compose -f infra/docker/docker-compose.yml up

ingest:
	python -c "from src.core.rag_engine import RAGEngine; RAGEngine().ingest_documents()"

eval:
	python src/eval/evaluator.py
