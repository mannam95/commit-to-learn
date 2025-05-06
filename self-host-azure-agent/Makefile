# Build the docker image
build:
	docker compose build

# Run the docker container
up:
	docker compose up

# Run the docker container in detached mode
up-d:
	docker compose up -d

# Stop the docker container
down:
	docker compose down

# Clean up the docker container
clean:
	docker compose down
	docker volume prune -f
	docker system prune -f