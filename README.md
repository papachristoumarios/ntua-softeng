# cheapies.gr

[![Build Status](https://travis-ci.com/papachristoumarios/ntua-softeng.svg?token=DxqFuX4UzFjiGRipqjph&branch=master)](https://travis-ci.com/papachristoumarios/ntua-softeng) ![PyPI - Django Version](https://img.shields.io/pypi/djversions/djangorestframework.svg)  ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django.svg) ![APMLicense](https://img.shields.io/badge/license-MIT-green.svg)


:money_with_wings: Price observatory to find the best bargains!



## :question: Project Description

This project aims to provide a web-based "price observatory", which will allow the users to post product prices from different stores. Volunteers will record the prices of various items and share them via the application.

Beyond the basic capabilities of product, store, time and space registration footprint and price as well as the facilities for their search, monitoring and opposition data (tables, charts, charts, etc.), special emphasis should be put on the possibility the interconnection of third-party applications with the observatory through appropriate web-based APIs.


_This repository hosts the [Software Engineering](https://courses.softlab.ntua.gr/softeng/2018b/) assignment for NTUA Course "Software Engineering" (Fall 2018)._

:snake: The application is developed using the Django Web Framework in Python 3.5.



## Team

This project was curated by "mycoderocks" team comprising of (alphabetical order):
 * Dimitris Christou
 * [Ioannis Daras](https://github.com/giannisdaras) (AM: 03115018, daras.giannhs@gmail.com)
 * Dimitris Kelesis
 * Marios Papachristou
 * Ioannis Siachos
 * Konstantinos Stavropoulos



## :nut_and_bolt: Setup/Usage

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

### Install requirements

Install the requirements with pip:

```bash
pip3 install -r requirements.txt
```

### Run the development webserver

Run webserver with:

```bash
python3 manage.py runserver
```

Make the migrations with:

```
python3 manage.py makemigrations
```

Migrate with:

```
python3 manage.py migrate
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



## :hammer: Technologies Used

* Back-end
  * Python v3.5
  * Django v2.1
  * MySQL v14.14
  * Django REST Framework
  * Google Maps Geocoding API
* Front-end
  * Bootstrap v4.1.3
  * Tachyons v4.1
  * wow.js
  * Mapbox v0.5
  * jQuery
  * slick.js
* Deployment
  * Gunicorn
  * nginx
  * Docker
* Continuous Integration & Unit Testing
  * Travis CI


## :newspaper: Guidelines

### Language

The application language is [Greek](https://en.wikipedia.org/wiki/Greek_language).


### Code Formatting

* Back-end: [PEP8](https://www.python.org/dev/peps/pep-0008/) and [Django Coding Style](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/)
* Front-end: [Bootstrap CSS Coding Standards](http://www.w3big.com/bootstrap/bootstrap-css-codeguide-html.html)

### Creating a view

When creating a view, let's say `example` you should notice the following things:

* The view name matches the template name, so you should create `example.html`

* If you use any static JS code, place it into `<app_name>/static/js/example.js` file.

* The main styling should go into `<app_name>/static/main.css`. Inside the HTML file you should declare

  ```html
  {% extends layout.html %}
  {% block content %}
  <section id="example">
  	<div class="a">
          <!-- SOME CODE HERE -->
      </div>

  <!-- CODE HERE -->

  </section>

  {% endblock %}
  ```

  and inside `main.css` you should declare

  ```css
  section.example {
      .a {
          /* CSS Formatting of a inside example */
      }
  }
  ```

  for view-specific CSS. Otherwise, you should put it inside `main.css`




### Contributing Workflow

We are using the [Git Branch Workflow](https://es.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow). In the future we will migrate to [fork & pull-request](https://gist.github.com/Chaser324/ce0505fbed06b947d962) workflow. The project status is kept inside [GitHub Projects](https://github.com/papachristoumarios/ntua-softeng/projects) following the [Kanban System](https://en.wikipedia.org/wiki/Kanban)

The project tasks are [tracked with GitHub projects](https://github.com/papachristoumarios/ntua-softeng/projects) following the [Kanban Scheduling Methodology](https://en.wikipedia.org/wiki/Kanban).


### Project Structure

* `docs/`  Project-level documentation needs to be stored here and be written in Markdown. Module-specific documentation may be located only in source files.
* `etc/`  Extra files that accompany the project, such as configuration of external tools etc.
* `<app_name>/` Django applications that reside inside the project
    * `<app_name>/urls.py` Application-level urls
    * `<app_name>/views.py` Application-level views
    * `<app_name>/models.py` Application-level models
    * `<app_name>/templates/<template.html>` HTML Templates
    * `<app_name>/static/{css, js}/{file.css, file.js}` CSS and JavaScript Static files
        * CSS Static files contain a `main.css` that contains the basic CSS for the web application
        * JS Static files are organized per view (e.g. `product.js` refers to `product.html`).
* `project/`
    * `urls.py`  Top-level routing instructions.
* `manage.py`  Django command-line tool.
* `_version.py` Contains a `__version__` variable to indicate the current version of the website. Semantic versioning is used.
* `setup.py`  Setup script.
* `requirements.txt`  Pinned production dependencies.
