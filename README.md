<h1 align="center" style="display: block; font-size: 2.5em; font-weight: bold; margin-block-start: 1em; margin-block-end: 1em;">
  <br /><br /><strong>Blog Application</strong>
</h1>

# Introduction[](#introduction)
Test project similar to blogs. This project is built with Django and Django Ninja Framework.

---

# Table of Contents

- [Prerequisites](#prerequisites)
- [Settings](#settings)
  - [Security and Debug](#security-and-debug)
  - [Database](#database)
  - [Email Service](#email-service)
  - [Redis and Celery](#redis)
- [Deployment](#deployment)
  - [Clone the Project](#clone-the-project)
  - [Set Environment Variables](#set-environment-variables)
  - [Build and Deploy](#build-and-deploy)

---

# Prerequisites
Before deploying the project you have to make sure that you have the following pre-requisites installed:

- Docker
- Docker Compose
- Git

---

# Settings[](#settings)
There are some configurations needed before starting the deployment. These
configurations are saved as environment variables. To add an environment variable, you must
create a `.env` file at the root of the project and add the variables in that file similar to the example below:

```dotenv
VARIABLE_NAME=VARIABLE_VALUE
```

You can find a sample `.env` file, containing all the fields, in the root of the project named `.env.sample`.

## Security and Debug

- `SECRET_KEY`
  - A long random string as the secret key of the project.
- `DEBUG`
  - If `True` the project will run in debug mode.  Default value is `True`.
  - If `False` the project will run in production mode.
- `ALLOWED_HOSTS`
  - Sets the `ALLOWED_HOSTS` setting in django.
  - Should at least contain `mydomain.com`.
  - Can add more domains if needed as a comma separated string.
  - For development use, you can set it to `*` to allow all hosts.

## Database

To connect your django project to your database, you should set
the following environment variables:

- `DB_NAME`
  - Name of the database you want to connect to.
- `DB_USER`
  - Username of the user you want to connect to the database with.
- `DB_PASS`
  - Password of the user you want to connect to the database with.
- `DB_HOST`
  - The host to use when connecting to the database. Default value is `localhost`.
- `DB_PORT`
  - The port to use when connecting to the database. Default value is `5432`.

We use PostgreSQL as our database. For our database to initialize the database and the user,
we need to set some of the environment variables in the `.env.postgres` file. You can find a sample
`.env.postgres` file, containing all the fields, in the root of the project named `.env.postgres.sample`.

The environment variables are as follows:

- `POSTGRES_USER`
  - Username of the user you want to connect to the database with. Should be the same as `DB_USER` in the `.env` file.
- `POSTGRES_PASSWORD`
  - Password of the user you want to connect to the database with. 
Should be the same as `DB_PASS` in the `.env` file.
- `POSTGRES_DB`
  - Name of the database you want to connect to. Should be the same as `DB_NAME` in the `.env` file.

## Email Service
You have to set up an email service to be able to send emails. You can still deploy the project
without setting these fields, in this case you won't be able to send any emails through this project. 

Email environment variables are as follows:

- `EMAIL_HOST`
  - The host to use for sending email.
- `EMAIL_HOST_USER`
  - Username to use for the SMTP server.
- `EMAIL_HOST_PASSWORD`
  - Password to use for the SMTP server.
- `EMAIL_PORT`
  - Port to use for the SMTP server.
- `DEFAULT_FROM_EMAIL`
  - Default email address to send the emails from.

## Redis

- `REDIS_HOST`
  - The host to use when connecting to Redis. Default value is `localhost`.

---

# Deployment
### Clone the Project
Clone the project and cd into the project directory.
```shell
git clone git@github.com:RuhollahSeka/BlogApp.git
cd BlogApp/
```

### Set Environment Variables
Add the `.env` and `.env.postgres` files created in the [settings](#settings) section to this directory.

### Build and Deploy

Enter the following command to build and deploy the project:

```shell
docker-compose build && docker-compose up -d
```

Congratulations! The project is now deployed and running on port 8000 of your localhost.

---

# Testing

To run the tests, you can use the following command:

```shell
docker-compose exec -it <CONTAINER_NAME> python manage.py test
```

Also, after each push to the repository, the tests will be run automatically by GitHub Actions.

---

# Linting

Flake8 is used for linting in this project.
To configure flake8, you can edit the `.flake8` file in the root of the project.

To run the linting, you can use the following command:

```shell
docker-compose exec -it <CONTAINER_NAME> flake8
```

Also, after each push to the repository, the linting will be run automatically by GitHub Actions.

---

# CI

This project uses GitHub Actions for CI. You can find the workflow files in the `.github/workflows` directory.

---

# API Documentation
After deploying the project, you can access the API documentation at `/api/docs/`.
