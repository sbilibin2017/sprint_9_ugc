PENV = .venv
PYTHON = $(PENV)/bin/python
PYRIGHT = $(PENV)/bin/pyright
TOML_SORT = $(PENV)/bin/toml-sort

PROJECT_FOLDERS= elk benchmark action_api

.PHONY: init
init:
	@echo "Installing..."
	@poetry install


.PHONY: lint
lint:
	@echo 'Running poetry checks...'
	@poetry check

	@echo 'Running black checks...'
	@$(PYTHON) -m black --check .

	@echo 'Running isort checks...'
	@$(PYTHON) -m isort --check .

	@echo 'Running toml-sort checks...'
	@$(TOML_SORT) --check pyproject.toml
	@echo ''

	@echo 'Running pylint checks...'
	@$(PYTHON) -m pylint .

	@echo 'Running pyright checks...'
	@$(PYRIGHT)

.PHONY: ci-lint-fix
lint-fix:
	@echo "Running poetry autofixes..."
	@poetry check
	@poetry lock --no-update

	@echo "Running black autofixes..."
	@$(PYTHON) -m black --safe .

	@echo "Running isort autofixes..."
	@$(PYTHON) -m isort --atomic .

	@echo "Running toml-sort autofixes..."
	@$(TOML_SORT) --in-place pyproject.toml

	@echo "Running sort-all autofixes..."
	@find $(PROJECT_FOLDERS) -name "*.py" -type f -exec $(PYTHON) -m sort_all "{}" \;

	@echo "Running pyupgrade autofixes..."
	@find $(PROJECT_FOLDERS) -name "*.py" -type f -exec $(PYTHON) -m pyupgrade --py311-plus "{}" \;

	@echo "Running pylint checks..."
	@$(PYTHON) -m pylint .

	@echo "Running pyright checks..."
	@$(PYRIGHT)

