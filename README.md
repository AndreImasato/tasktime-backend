# TASKTIME - BACKEND
TaskTime is an application for you to register your execution times for your projects tasks.

This repository must be used with its frontend counterpart, [TASKTIME - FRONTEND](https://github.com/AndreImasato/tasktime-frontend).


### Application Standalone Execution

#### Local Execution

##### PostgreSQL dependencies
This repository uses ```psycopg2``` package, thus it is required that PostgreSQL and its dev dependencies are installed.

List of dependencies:
<li>
    libpq-dev
</li>
<br>

##### Python dependencies

This repository uses ```python3.10```. It is **recommended** to use a **virtual environment**. Having one activated, install the dependencies by running the following command.
```bash
python -m pip install -r requirements.txt
```

##### Running a local server
Make the migrations by running the following command
```bash
python manage.py makemigrations

python manage.py migrate
```

To start the server, run the following command (having a virtual environment activated)
```bash
python manage.py runserver
```
**Note:** by default it is used a local SQLite database. If you wish, you can configure a PostgreSQL database and change the local .env as displayed in docker example (```envs/docker/.env```)

#### Docker Container Execution
To run this application in a docker container, first build the container images by running the following command
```bash
make build-containers
```

Then, to run the containers, run the following command
```bash
make up-containers
```

To stop the containers and bring them down, run the command
```bash
make down-containers
```

### About the Backend

This backend is built based on [Django Rest Framework](https://www.django-rest-framework.org/) combined with a few other packages.

The API documentation can be found by accessing ```http://<your-ip-address>/docs/```, which is built using [drf-spectactular](https://drf-spectacular.readthedocs.io/en/latest/). The Django admin panel can be accessed as well in the folloing URL ``http://<your-ip-address/admin/>`.

**Note:** ```your-ip-address``` can be your localhost (and port, in case the default 80 port couldn't be used) you your Nginx docker container host. To get this container local ip address, run the following command.

```bash
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' tasktime_nginx
```