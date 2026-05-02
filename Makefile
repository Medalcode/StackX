.PHONY: up down build logs shell-backend shell-frontend shell-worker shell-beat logs-worker logs-beat

up:
	docker-compose up --build

down:
	docker-compose down -v

build:
	docker-compose build

logs:
	docker-compose logs -f

shell-backend:
	docker-compose exec backend sh

shell-frontend:
	docker-compose exec frontend sh

shell-worker:
	docker-compose exec worker sh

shell-beat:
	docker-compose exec beat sh

logs-worker:
	docker-compose logs -f worker

logs-beat:
	docker-compose logs -f beat
