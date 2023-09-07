#top_api

## Description

###Sensitive data

1. Create in the project root (or obtain from team member) an `.env` file with 
environment variables required by application.

### Performing commits

1. Pre-commit hook installed, settings are in .pre-commit-config.yaml
2. To instantiate new hook settings change .pre-commit-config.yaml file
     and run     pre-commit install
3. To bypass hook checking run      git commit -m "..." --no-verify

### Local run in docker container using docker-compose

1. Ensure `.env` file has at least `POSTGRES_USER`, `POSTGRES_PASSWORD` and 
    `POSTGRES_DB` variables set to any string values.
2. Run _postgres_ in docker containers:

       docker-compose up  # run all services defined in docker-compose file


### Setup database using sql files

For work with application, you need to setup your database in docker container. To perform this:

1. While postgres docker container is running, enter it (use separate terminal):

       docker exec -it top_api bash

2. Enter inside psql terminal (inside your container):

       psql -U postgres

3. Create database for use it in our application and use it (inside psql terminal):

       CREATE DATABASE api;
       \c api;

4. Change in .env file in root directory value of POSTGRES_DB on api

5. Rebuild docker and up it, use commands:

       docker-compose build --no-cache
       docker-compose up

### Redis

1. We will use a celery that's in turn uses Redis. 
    To start a Redis server on port 6379, we can run the following command:
        docker run -p 6379:6379 -d redis:5

### Celery

1. To run celery use command in terminal
    celery -A config worker -l -P solo (-P solo for Windows)
2. To run beat service use command in terminal
    celery -A config beat
3. To upgrade celery settings run
    celery upgrade settings config/settings.py
4. To delete task from the queue
    celery -A config purge

### Performing tests

For testing application there is need to use pytest and it's plugings.
There is need to always check amount of test cases and their covering.

1. To perform created test cases, use command:

       pytest --cov

2. To load previously created fixtures, printer_fixtures.json for example, 
    we can use command  python manage.py loaddata printer_fixtures.json