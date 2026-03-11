build-dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build

build-prod:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

down-dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml down

down-prod:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml down

start-dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml start

start-prod:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml start
stop-dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml stop

stop-prod:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml stop

restart-dev:
	docker compose down && docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build

restart-prod:
	docker compose down && docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

logs:
	docker compose logs -f