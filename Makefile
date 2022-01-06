ps:  # watch all containers
	sudo docker ps -a

images:  # watch all images
	sudo docker images

stop:
	sudo docker-compose stop

build:
	sudo docker-compose build

up:  build
	sudo docker-compose up -d

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

set-test-env:
	python app/tests/change_env.py 'test'

set-prod-env:
	python app/tests/change_env.py 'prod'

test: stop set-test-env
	-pytest app/tests
	set-prod-env

cov: stop set-test-env
	-coverage run -m pytest app/
	set-prod-env
	coverage report -m
