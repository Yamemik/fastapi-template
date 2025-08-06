# Названия сервисов и базовые переменные
COMPOSE=docker-compose
SERVICE=api

# Команды
up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

build:
	$(COMPOSE) build

rebuild:
	$(COMPOSE) down
	$(COMPOSE) build --no-cache
	$(COMPOSE) up -d

logs:
	$(COMPOSE) logs -f $(SERVICE)

sh:
	$(COMPOSE) exec $(SERVICE) sh

bash:
	$(COMPOSE) exec $(SERVICE) bash

migrate:
	$(COMPOSE) exec $(SERVICE) alembic upgrade head

makemigrations:
	$(COMPOSE) exec $(SERVICE) alembic revision --autogenerate -m "new migration"

psql:
	$(COMPOSE) exec db psql -U postgres -d fastapi_app

stop:
	$(COMPOSE) stop

start:
	$(COMPOSE) start

restart:
	$(COMPOSE) restart

# Очистка
prune:
	docker system prune -f
