# cheapies.gr

:money_with_wings: Price observatory to find the best bargains!

## Project Description

This project aims to provide a web-based "price observatory", which will allow the users to post product prices from different stores. Volunteers will record the prices of various items and share them via the application.

Beyond the basic capabilities of product, store, time and space registration footprint and price as well as the facilities for their search, monitoring and opposition data (tables, charts, charts, etc.), special emphasis should be put on the possibility the interconnection of third-party applications with the observatory through appropriate web-based APIs.


_This repository hosts the [Software Engineering](https://courses.softlab.ntua.gr/softeng/2018b/) assignment for NTUA Course "Software Engineering" (Fall 2018)._

:snake: The application is developed using the Django Web Framework in Python 3.5.

## Team

This project was curated by "mycoderocks" team comprising of (alphabetical order):
 * Dimitris Christou
 * Ioannis Daras
 * Dimitris Kelesis
 * Marios Papachristou
 * Ioannis Siachos
 * Konstantinos Stavropoulos


## Setup/Usage

### Install requirements

Install the requirements with pip:

```bash
pip3 install -r requirements.txt
```

### Setup MySQL database

The web application uses MySQL as a database for holding data.

1. Setup MySQL
```bash
sudo apt-get install mysql libmysqlclient-dev
```
2. Login into mysql from the command line and create the database
```sql
create database cheapies character set utf8;
```
3. Create a `database.cnf` file containing the following information
```
[client]
database = cheapies
user = user
password = password
default-character-set = utf8
```

### Run the development webserver

Run webserver with:

```bash
python3 manage.py runserver
```

Run tests with:

```bash
python3 manage.py test
```

### Building a Docker Image

This project can be dockerized. The configuration is located at `Dockerfile` and `docker-compose.yml`

1. Build the docker image using `docker-compose`
```bash
export DOCKER_HOST=127.0.0.1
sudo docker-compose build
```
2. Run the image with
```bash
sudo docker-compose up
```

## Technologies Used

 * Development:
  * Python 3.5
  * Django Web Framework
  * MySQL
  * Mapbox
 * Deployment & Operations:
  * Docker
  * Travis CI
