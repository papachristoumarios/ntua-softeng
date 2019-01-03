# Makefile for various tasks

MEDIA=cheapiesgr/static/media
GEN_DATA=etc/fixtures/generate_data.py 
SHELL := /bin/bash

PYTHON=python

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
