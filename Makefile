
build:
	docker-compose build
	make migration

run:
	docker-compose run --service-ports -e --rm api bash -c "python -m app"

run_bash:
	docker-compose run --service-ports -e --rm api bash

run_pytest:
	docker-compose run --service-ports --no-deps -e --rm api bash -c "pytest app/"

run_pylint:
	docker-compose run --service-ports --no-deps -e --rm api bash -c "pylint -E app/"

run_black:
	docker-compose run --service-ports --no-deps -e --rm api bash -c "black ."

run_flake8:
	docker-compose run --service-ports --no-deps -e --rm api bash -c "flake8 ."

run_isort:
	docker-compose run --service-ports --no-deps -e --rm api bash -c "isort ."

run_code_convention:
	make run_black
	make run_flake8
	make run_pylint

poetry_add:
	docker-compose run --service-ports --no-deps -e --rm api bash -c "poetry add ${@}"

migrate:
	docker-compose run --service-ports -e --rm api bash -c "alembic revision --autogenerate -m ${@}"

migration:
	docker-compose run --service-ports -e --rm api bash -c "alembic upgrade head"
