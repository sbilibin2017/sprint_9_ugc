.PHONY: init
init:
	@echo "Installing..."
	@poetry install
	@echo "Starting services..."
	docker compose up --build -d

.PHONY: stop
stop:
	@echo "Stopping services..."
	docker compose down
	@echo "Services stopped"
