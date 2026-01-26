dev:
	docker-compose up --build

stop:
	docker-compose down

test:
	pytest backend/tests/ -v

db-reset:
	rm -f data/warehouse.db
	docker-compose restart backend

logs:
	docker-compose logs -f
