.PHONY: help install test clean lint format notebook

help:
	@echo "Market Intelligence ML - Available Commands:"
	@echo "  make install     Install package and dependencies"
	@echo "  make test        Run unit tests"
	@echo "  make lint        Run linting checks"
	@echo "  make format      Format code with black"
	@echo "  make notebook    Launch Jupyter notebook server"
	@echo "  make clean       Remove cache and temp files"

install:
	pip install -r requirements.txt
	pip install -e .

test:
	pytest tests/ -v --cov=src --cov-report=html

lint:
	flake8 src/ tests/
	mypy src/

format:
	black src/ tests/

notebook:
	jupyter notebook notebooks/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete
