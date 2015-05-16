help:
	@echo "server           run dev server"
	@echo "rqworker         run rqworker"
	@echo "shell            open a python shell"
	@echo "dbshell          open a database shell"
	@echo "mkmigrate        makemigrations
	@echo "migrate          migrate
	@echo "clean            clean"
	@echo "tests            run tests"
	@echo "lint             run flake8 check"

server:
	@python chendian/manage_dev.py runserver 0.0.0.0:8000

rqworker:
	@python chendian/manage_dev.py rqworker

shell:
	@python chendian/manage_dev.py shell

dbshell:
	@python chendian/manage_dev.py dbshell

mkmigrate:
	@python chendian/manage_dev.py makemigrations

migrate:
	@python chendian/manage_dev.py migrate

clean: clean-build clean-pyc
	@rm -fr cover/

clean-build:
	@rm -fr build/
	@rm -fr dist/
	@rm -fr *.egg-info

clean-pyc:
	@find . -type f -name '*.pyc' -delete
	@find . -type f -name '*.pyo' -delete
	@find . -type f -name '*~' -delete
	@find . -type f -name '*,cover' -delete

lint:
	@flake8 chendian
	@flake8 tests --ignore=E501

tests:
	@py.test

up:
	@cd chendian && qn_cli -d chendian static/ -v

.PHONY: server shell dbshell clean clean-build clean-pyc lint tests migrate mkmigrate
