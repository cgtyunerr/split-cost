SHELL=/bin/bash
.DEFAULT_GOAL := default

.PHONY: venv
venv:
	@echo "---------------------------"
	@echo "- Activating poetry shell -"
	@echo "---------------------------"
	poetry shell

.PHONY: install
install:
	@echo "---------------------------"
	@echo "- Installing dependencies -"
	@echo "---------------------------"
	poetry shell
	poetry install

.PHONY: update
update:
	@echo "-------------------------"
	@echo "- Updating dependencies -"
	@echo "-------------------------"
	poetry shell
	poetry update

.PHONY: run
run:
	@echo "----------------------"
	@echo "- Running API server -"
	@echo "----------------------"
	uvicorn app.api.main:app --reload --log-level debug
