# Makefile for various tasks

MEDIA=cheapiesgr/static/media
GEN_DATA=etc/fixtures/generate_data.py
SHELL := /bin/bash
DOCKER_COMPOSE=docker-compose
APT=apt-get install -y
PYTHON=python3
MANAGE=$(PYTHON) manage.py
PIP=pip3

help:
	@echo "Usage"
	@echo "data    Download data and populate database"
	@echo "deps    Install requirements"
	@echo "database_config Make database configuration file"
	@echo "deploy  Run deployment routine"
	@echo "tests   Run tests"
	@echo "dockerize Dockerize application"
	@echo "runsslserver Run ssl dev server"

data: download_data populate_db

download_data:
	wget -O supermarket-data.zip https://pithos.okeanos.grnet.gr/public/eYYbrUY7m4WOzsywBNG175
	mkdir -p $(MEDIA)
	unzip -qq supermarket-data.zip -d cheapiesgr/static/media

clean:
	rm -rf supermarket-data.zip
	rm -rf products.json user.json categories.json shop.json

populate_db: supermarket-data.zip
	$(PYTHON) $(GEN_DATA) -d $(MEDIA)/supermarket_crawlers -t shop -n 20 --apply
	$(PYTHON) $(GEN_DATA) -d $(MEDIA)/supermarket_crawlers -t categories -n 10 --apply
	$(PYTHON) $(GEN_DATA) -d $(MEDIA)/supermarket_crawlers -t user -n 10 --apply
	$(PYTHON) $(GEN_DATA) -d $(MEDIA)/supermarket_crawlers -t products -n 3000 --apply

migrate:
	$(MANAGE) makemigrations
	$(MANAGE) migrate
	$(MANAGE) makemessages
	$(MANAGE) compilemessages

test:
	$(MANAGE) test

py_deps: requirements.txt
	$(PIP) install -r requirements.txt

deps:
	$(APT) mysql-client libmysqlclient-dev libgdal-dev python3-gdal
	$(MAKE) py_deps


test_db:
	mysql -e 'create database cheapies;' -u root
	./test_database_config.sh >database.cnf

deploy:
	$(MAKE) py_deps
	$(MAKE) test_db
	$(MAKE) migrate

dockerize: Dockerfile docker-compose.yml
	$(DOCKER_COMPOSE) build
	$(DOCKER_COMPOSE) up

certificate_gen:
	openssl genrsa -des3 -out server.key 1024
	openssl req -new -key server.key -out server.csr
	cp server.key server.key.org
	openssl rsa -in server.key.org -out server.key
	openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt

runsslserver:
	$(PYTHON) manage.py runsslserver --certificate server.crt --key server.key

softeng18b_tests:
	@echo "Resetting DB"
	$(PYTHON) manage.py reset_db
	@echo "Migrations"
	$(PYTHON) manage.py migrate
	@echo "Create Superuser"
	echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', '1234')" | $(PYTHON) manage.py shell
	@echo "Start web application"
	$(PYTHON) manage.py runsslserver --certificate server.crt --key server.key

softeng18b_demo:
	@echo "Preparing DB"
	$(PYTHON) manage.py reset_db
	$(PYTHON) manage.py makemigrations
	$(PYTHON) manage.py migrate
	@echo "Filling DB with data"
	$(MAKE) data
	echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', '1234')" | $(PYTHON) manage.py shell
	@echo "Run functional tests"
	$(PYTHON) manage.py runsslserver --certificate server.crt --key server.key
