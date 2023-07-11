# ZeroDowntimeExample
This project demonstrates a zero-downtime approach and provides solutions for critical operations that pose challenges.

## Details
It contains the migrations that allow smooth changing of the product version without downtime.

The project consists of Django ORM, simple GraphQL API and DB on postgreSQL.

It guarantees no downtime when switching one version at a time. In this example from v0.1 to v0.2, with firstly upgrading to v.0.1.1.

It contains the solution for:
- adding a non-nullable field with default value: `is_published`
- adding unique value: `slug`
- renaming the filed `created`
- adding the DB index

## How to start

1. Create the Python virtual env and activate it
```
$ python -m venv env_name
```

2. Install the requirements
```
$ pip install requirements.txt
```

3. Start the docker containers that contain DB, pgAdmin, and redis
```
$ docker-compose up
```

4. Run the database migrations
```
$ python manage.py migrate
```

5. Populate db
You can populate the DB with sample products data with the use of `populate_db` command.
Use `--amount` argument to specify number of instances to create:
```
$ python manage.py populate_db --amount=1000
```

6. Start the celery worker
```
$ python -m celery -A zerodowntime worker -B -l info
```

7. Start the django server
```
$ python manage.py runserver
```


### Tips
- To use `pgAdmin`, open http://localhost:5051/browser/ and log in (username: pgadmin@example.com, password: `root`).
Then add `db` service from port `5432`, `username` and `password` are: `demo`.

## Project structure
Tags:
- `0.1.0` - the initial state, this is the starting point
- `0.1.1` - contains changes that ensure the zero-downtime approach when switching to version v0.2
- `0.2` - version v0.2 of the system with applied intended model changes
- `0.3` - contains the final stage with all required operations

Branches:
- `0.1` - corresponds to version v0.1
- `0.2` - corresponds to version v0.2
- `0.3` - corresponds to version v0.3


## Test the zero downtime
The best way to check the zero downtime solution is to start from v0.1.0, switching
through v0.1.1 to v0.2, and finally to v0.3.0.

Zero downtime ensures the compatibility of DB with the previous version of the system.
On each step, the upgraded DB will be compatible with the previous version of the code.

### What are the exact steps zero downtime approach?
1. Checkout to 0.1.0 tag and configure the system (start the docker, run DB migrations, populate DB with sample data, start the celery worker, and run app server).
2. Switch to tag 0.1.1 and proceed the update (see steps [below](#how-to-proceed-with-an-update))
3. After upgrading the DB, you can checkout again to the tag 0.1.0 and run some API requests (see [below](#test-the-api) how to test the API).
The DB compatibility is ensured, the previous version of the system is working with the upgraded DB!
4. You can repeat steps 1-3 for switching from 0.1.1 to 0.2.0 and from 0.2.0 to 0.3.0.

Also on all of these step, I recommended you to check the changes on the product table in the pgAdmin.

### How to proceed with an update
1. Stop the asynchronous task workers
2. Run the database migration
3. Start the asynchronous task workers of a new version


### Potential issues
You might ask yourself *But why all of this effort, what wrong might happen?* and the response it
you can test it by yourself! Just follow the steps from [What are the exact steps zero downtime approach?](#what-are-the-exact-steps-zero-downitme-approach) but with skipping the versions.

For example:
- switch from v0.1.0 directly to v0.2.0,
- switch from v0.1.0 directly to v0.3.0.

You should get errors when trying to perform API requests.


## Test the API
The easiest way to test the API is by opening the graphql playground.
After starting the server go to http://localhost:8000/graphql/ and run some queries or mutations.
