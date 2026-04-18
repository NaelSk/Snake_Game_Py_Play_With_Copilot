.PHONY: test run clean help all

help:
	@echo "Available commands:"
	@echo "  make test     - Run all unit tests"
	@echo "  make run      - Run the game"
	@echo "  make clean    - Remove cache and temporary files"
	@echo "  make all      - Run tests and clean"

test:
	@echo "Running tests..."
	python -m unittest test_game.py -v

test-verbose:
	@echo "Running tests with detailed output..."
	python -m unittest test_game.py -v

test-quick:
	@echo "Running tests (minimal output)..."
	python -m unittest test_game.py 2>&1 | tail -5

run:
	@echo "Starting Rock-Paper-Scissors game..."
	python game.py

clean:
	@echo "Cleaning up..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name ".DS_Store" -delete 2>/dev/null || true
	@echo "✅ Cleanup complete"

all: test clean
	@echo "✅ All tasks complete"
