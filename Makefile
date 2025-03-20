.PHONY: install test run clean deploy

# Set default target
default: help

# Help command
help:
	@echo "Qdrant Multi-Node Cluster Demo - Available commands:"
	@echo "  make install     - Install the package in development mode"
	@echo "  make test        - Run tests"
	@echo "  make run         - Run the demo application"
	@echo "  make deploy      - Deploy the Qdrant cluster using Docker Compose"
	@echo "  make clean       - Clean up build artifacts"
	@echo "  make help        - Show this help message"

# Install package in development mode
install:
	pip install -e .

# Run tests
test:
	python -m unittest discover -s tests

# Run the demo application
run:
	python src/run_demo.py

# Deploy Qdrant cluster using Docker Compose
deploy:
	cd deployments/docker && docker-compose up -d

# Stop Qdrant cluster
stop:
	cd deployments/docker && docker-compose down

# Clean up build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name "*.pyd" -delete 