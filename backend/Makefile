.PHONY: help install migrate run celery test clean

help:
	@echo "Available commands:"
	@echo "  make install       - Install dependencies"
	@echo "  make migrate       - Run database migrations"
	@echo "  make makemigrations - Create new migrations"
	@echo "  make run           - Run development server"
	@echo "  make celery        - Run Celery worker"
	@echo "  make celery-beat   - Run Celery beat scheduler"
	@echo "  make shell         - Open Django shell"
	@echo "  make superuser     - Create superuser"
	@echo "  make test          - Run tests"
	@echo "  make lint          - Run code linting"
	@echo "  make format        - Format code with black"
	@echo "  make clean         - Clean pyc files"

install:
	pip install -r requirements/dev.txt

migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

run:
	python manage.py runserver 0.0.0.0:8000

celery:
	celery -A config worker -l info

celery-beat:
	celery -A config beat -l info

shell:
	python manage.py shell_plus

superuser:
	python manage.py createsuperuser

test:
	pytest

lint:
	flake8 apps/ config/
	pylint apps/ config/

format:
	black apps/ config/
	isort apps/ config/

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

