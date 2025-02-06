SERVICE_NAME := sb-backbone
PORT 		 := 42069
POETRY 		 := poetry

.PHONY: help
help: ## Show this help message
	@echo "Available Makefile targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: start
start: ## Start the application with Uvicorn (auto-reload enabled)
	$(POETRY) run uvicorn app.main:app --host 0.0.0.0 --port $(PORT) --reload

.PHONY: install
install: ## Install project dependencies using Poetry
	$(POETRY) install

.PHONY: shell
shell: ## Activate the Poetry shell
	$(POETRY) shell

.PHONY: test
test: ## Run tests using Pytest
	$(POETRY) run pytest

.PHONY: lint
lint: ## Lint the codebase using Flake8
	$(POETRY) run flake8 app tests

.PHONY: format
format: ## Format the codebase using Black and isort
	$(POETRY) run black app tests
	$(POETRY) run isort app tests

.PHONY: lint-fix
lint-fix: ## Lint and fix errors at the same time
	$(POETRY) run autoflake --remove-all-unused-imports --remove-unused-variables --in-place --recursive app tests
	$(MAKE) format
	$(MAKE) lint

.PHONY: clean
clean: ## Clean up Python caches and build artifacts
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	$(POETRY) cache clear --all pypoetry

.PHONY: setup
setup: install pre-commit-install ## Set up the project environment
	@echo "Project setup complete."

.PHONY: pre-commit-install
pre-commit-install: ## Install pre-commit hooks
	$(POETRY) run pre-commit install
.PHONY: db-upgrade

.PHONY: migration
migration:
	@read -p "Enter migration message (default: 'Auto-generated migration'): " msg; \
	if [ -z "$$msg" ]; then \
		msg="Auto-generated migration"; \
	fi; \
	$(POETRY) run alembic revision --autogenerate -m "$$msg"

.PHONY: migrate
migrate:
	$(POETRY) run alembic upgrade head

.PHONY: rollback
rollback:
	$(POETRY) run alembic downgrade -1

.DEFAULT_GOAL := help
