app:
	docker-compose -f docker-compose.yml up --build -d
stop:
	docker-compose down