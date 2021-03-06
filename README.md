# Yummy-Recipes-RestAPI
[![Build Status](https://travis-ci.org/PatrickCmd/Yummy-Recipe-RestAPI.svg?branch=master)](https://travis-ci.org/PatrickCmd/Yummy-Recipe-RestAPI)
[![Coverage Status](https://coveralls.io/repos/github/PatrickCmd/Yummy-Recipe-RestAPI/badge.svg?branch=master)](https://coveralls.io/github/PatrickCmd/Yummy-Recipe-RestAPI?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/f0c47514677ca33a508d/maintainability)](https://codeclimate.com/github/PatrickCmd/Yummy-Recipe-RestAPI/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/f0c47514677ca33a508d/test_coverage)](https://codeclimate.com/github/PatrickCmd/Yummy-Recipe-RestAPI/test_coverage)
```
```
Yummy recipes app is an application that allows users  to create, save and share meeting the needs of keeping track of awesome food recipes.

*see the API Documentation by following this [url](https://yummy-recipe-api.herokuapp.com)*

## Requirements(Building Blocks)
- `Python3` - A programming language that lets us work more quickly (The universe loves speed!).
- `Flask` - A microframework for Python based on Werkzeug, Jinja 2 and good intentions
- `Virtualenv` - A tool to create isolated virtual environment
- `PostgreSQL` – Postgres database offers many advantages over others.
- `Psycopg2` – A Python adapter for Postgres.
- `Flask-SQLAlchemy` – A Flask extension that provides support for SQLAlchemy.
- `Flask-Migrate` – Offers SQLAlchemy database migrations for Flask apps using Alembic.

## Installation
First clone this repository
```
$ git clone https://github.com/PatrickCmd/Yummy-Recipe-RestAPI.git
$ cd Yummy-Recipe-RestAPI
```
Create virtual environment and install it
```
$ virtualenv --python=python3 env
$ source /env/bin/activate
```
Then install all the necessary dependencies
```
pip install -r requirements.txt
```

## Set environment varibles and setup database
### On windows
At the terminal or console type
```
set APP_SETTINGS=development
set DATABASE_URL_DEV=postgresql://postgres:@localhost/yummy_api
psql -U postgres
postgres# CREATE DATABASE yummy_api
```
### On linux/Ubuntu or Mac
At the terminal or console type
```
export APP_SETTINGS=development
export DATABASE_URL=postgresql://postgres:@localhost/yummy_api
psql -U postgres
postgres# CREATE ROLE postgres
postgres# CREATE DATABASE yummy_api
```

## Initialize the database and create database tables
```
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
```

## Run the server
At the terminal or console type
```
python run.py
```

*You could use a GUI platform like [postman](https://www.getpostman.com/) to make requests to and fro the api.*

## Functionality(endpoints)
Endpoint | Functionality| Access
------------ | ------------- | ------------- 
POST /auth/register | Registers a user | PUBLIC
POST /auth/login |Logs a user in | PUBLIC
POST /auth/logout |Logs a user out | PRIVATE
POST /recipe_category | Creates a new recipe category | PRIVATE
GET /recipe_category | Lists all created recipe categories | PRIVATE
GET /recipe_category/id | Gets a single recipe category with the suppled id | PRIVATE
PUT /recipe_category/id | Updates recipe category with the suppled id | PRIVATE
DELETE /recipe_category/id | Deletes recipe_category with the suppled id | PRIVATE
POST /recipe_category/id/recipe | Creates a new recipe in recipe category | PRIVATE
PUT /recipe_category/id/recipe/recipe_id | Updates a recipe item | PRIVATE
DELETE /recipe_category/id/recipe/recipe_id | Deletes an recipe in a recipe category | PRIVATE

To run tests run this command at the console/terminal
```
nosetests or
python manage.py test
```
To run tests with coverage run this command at the console/terminal
```
python manage.py test_cov
```
