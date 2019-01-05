# Makefile for various tasks

MEDIA=cheapiesgr/static/media
GEN_DATA=etc/fixtures/generate_data.py 
SHELL := /bin/bash
DOCKER_COMPOSE=docker-compose

PYTHON=python
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

data: download_data populate_db 

download_data:
	wget -O supermarket-data.zip https://pithos.okeanos.grnet.gr/public/eYYbrUY7m4WOzsywBNG175
	mkdir -p $(MEDIA)
	unzip supermarket-data.zip -d cheapiesgr/static/media
	
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

deps: requirements.txt
	$(PIP) install -r requirements.txt

test_db:
	mysql -e 'create database cheapies;' -u root	
	./test_database_config.sh >database.cnf
	
deploy:
	$(MAKE) deps
	$(MAKE) test_db
	$(MAKE) migrate
	$(MAKE) data

dockerize: Dockerfile docker-compose.yml
	$(DOCKER_COMPOSE) build
	$(DOCKER_COMPOSE) up
