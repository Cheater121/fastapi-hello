COMPOSE := docker compose

.PHONY: up upb down logs logs-f ps bash db-psql redis-cli rebuild \
        up-mirror upb-mirror upb-host upb-host-mirror pull pull-mirror dns-test
up:
	$(COMPOSE) up -d

upb:
	$(COMPOSE) up -d --build

down:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs --no-color

logs-f:
	$(COMPOSE) logs -f --no-color

ps:
	$(COMPOSE) ps

bash:
	$(COMPOSE) exec app bash || $(COMPOSE) run --rm app bash

db-psql:
	$(COMPOSE) exec db psql -U app -d appdb

redis-cli:
	$(COMPOSE) exec redis redis-cli

rebuild:
	$(COMPOSE) build --no-cache app

up-mirror:
	$(COMPOSE) -f compose.yaml -f compose.mirror.yaml up -d

upb-mirror:
	$(COMPOSE) -f compose.yaml -f compose.mirror.yaml up -d --build

pull:
	$(COMPOSE) pull

pull-mirror:
	$(COMPOSE) -f compose.yaml -f compose.mirror.yaml pull

upb-host:
	$(COMPOSE) -f compose.yaml -f compose.build-host.yaml up -d --build

upb-host-mirror:
	$(COMPOSE) -f compose.yaml -f compose.mirror.yaml -f compose.build-host.yaml up -d --build

dns-test:
	docker run --rm busybox nslookup deb.debian.org || true
