# Makefile for WhatsApp CV Manager

.PHONY: help install setup run test clean deploy check

help:
	@echo "WhatsApp CV Manager - Available Commands"
	@echo "========================================="
	@echo ""
	@echo "  make check      - Quick system check"
	@echo "  make install    - Install dependencies"
	@echo "  make setup      - Initial setup (venv + install + migrate)"
	@echo "  make run        - Run Django development server"
	@echo "  make ngrok      - Start ngrok tunnel"
	@echo "  make verify     - Verify API configurations"
	@echo "  make test-cv    - Test CV extraction with sample"
	@echo "  make clean      - Clean temporary files"
	@echo "  make deploy     - Deploy to Railway"
	@echo ""

check:
	python3 check_setup.py

install:
	pip install --upgrade pip
	pip install -r requirements.txt

setup:
	python3 -m venv venv
	. venv/bin/activate && pip install --upgrade pip
	. venv/bin/activate && pip install -r requirements.txt
	. venv/bin/activate && python manage.py migrate
	@echo ""
	@echo "✅ Setup complete!"
	@echo "Next steps:"
	@echo "1. Copy .env.example to .env and configure"
	@echo "2. Add credentials.json for Google Sheets"
	@echo "3. Run: make verify"
	@echo ""

run:
	python manage.py runserver

ngrok:
	ngrok http 8000

verify:
	python manage.py verify_config

test-cv:
	python manage.py test_cv_extraction sample_cvs/sample_text_cv.txt

test-cv-no-save:
	python manage.py test_cv_extraction sample_cvs/sample_text_cv.txt --no-save

migrate:
	python manage.py migrate

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".DS_Store" -delete
	rm -rf media/temp/*
	@echo "✅ Cleaned temporary files"

deploy:
	@echo "Deploying to Railway..."
	railway up
	@echo "✅ Deployed! Configure environment variables in Railway dashboard"

superuser:
	python manage.py createsuperuser

shell:
	python manage.py shell

logs:
	tail -f logs/*.log 2>/dev/null || echo "No logs found"
