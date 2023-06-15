# ZeroDowntimeExample
This project demonstrates a zero-downtime approach and provides solutions for critical operations that pose challenges.

## Details
It contains the migrations that allow smooth changing of the product version without downtime.

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

4. Populate db
```
```

5. Start the celery worker
```
$ python -m celery -A zerodowntime worker -B -l info
```


### Tips
- To use `pgAdmin`, open http://localhost:5051/browser/ and log in (username: pgadmin@example.com, password: `root`).
Then add `db` service from port `5432`, `username` and `password` are: `demo`.

## Project structure
Tags:
- `v0.1.0` - the initial state, this is the starting point
- `v0.1.1` - contains changes that ensure the zero-downtime approach when switching to version v0.2
- `v0.2` - the version v0.2 of the system with applied intended model changes
- `v0.3` - contains the final stage with all required operations 

Branches:
- `v0.1` - corresponds to version v0.1
- `v0.2` - corresponds to version v0.2
- `v0.3` - corresponds to version v0.3

