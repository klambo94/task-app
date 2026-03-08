dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build

prod:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

down-dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml down

down-prod:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml down

down-dev-nuke:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml down -v

down-prod-nuke:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml down -v

logs:
	docker compose logs -f

restart-dev:
	docker compose down && docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build

restart-prod:
	docker compose down && docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build