ps:  # watch all containers
	sudo docker ps -a

images:  # watch all images
	sudo docker images

build:
	sudo docker-compose build

up:  build
	sudo docker-compose up -d --remove-orphans

prune-volumes:
	sudo docker volume prune --force

prune-containers:
	sudo docker container prune --force

prune-images:
	sudo docker image prune --force --all

web-shell:  # cd files_data --> rm *.txt --> to clean all files
	sudo docker exec -it weather_project-web-1 bash

postgres-shell:  # psql -U postgres --> \c postgres -->
	sudo docker exec -it weather_project-db-1 bash
