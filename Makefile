run-staging:
	docker-compose -f docker-compose-staging.yaml --env-file .env.example up -d --build --force-recreate
	docker exec -it api bash -c "cd /app && uv run alembic upgrade heads"
	docker exec -it api bash -c "cd /app && uv run python scripts/generate_test_data.py"

stop-staging:
	docker-compose -f docker-compose-staging.yaml down -v --remove-orphans

run-local:
	docker-compose -f docker-compose-local.yaml up -d --build --force-recreate

stop-local:
	docker-compose -f docker-compose-local.yaml down -v --remove-orphans

make-migration:
	alembic revision --autogenerate -m ${m}

migration:
	alembic upgrade heads
