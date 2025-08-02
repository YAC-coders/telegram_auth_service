.DEFAULT_GOAL=restart

DC = docker compose
DC_FILE = docker-compose.yml


.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort -d | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: build
build: ## build service
	${DC} -f ${DC_FILE} build
.PHONY: up
up: ## up services
	${DC} -f ${DC_FILE} up
.PHONY: logs
logs: ## show logs
	${DC} -f ${DC_FILE} logs -f
.PHONY: down
down: ## down and remove image
	${DC} -f ${DC_FILE} down --rmi local

restart: down build up
