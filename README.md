# validation-server-api

### django-rest-template

[![Build Status](https://travis-ci.org/Urban Institute/django-rest-template.svg?branch=master)](https://travis-ci.org/Urban Institute/django-rest-template)
[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

Template for Django API applications. Check out the project's [documentation](http://Urban Institute.github.io/django-rest-template/).

See [cookiecutter-django-rest](https://github.com/agconti/cookiecutter-django-rest)
repository for more detail.

### Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)  

### Staging Server

* Front End Site (requires log-in): `https://validation-server-stg.urban.org`

* API (requires log-in): `https://validation-server-stg.urban.org/api/v1/`

* Documentation (requires log-in):
    - `https://validation-server-stg.urban.org/api/swagger/`
    - `https://validation-server-stg.urban.org/api/swagger.[json | yaml]`
    - `https://validation-server-stg.urban.org/api/redoc/`

### API Usage
### Local Development

** FOR LOCAL TESTING PURPOSES ONLY **

You will need a .env file with the following specifications:

```bash
MYSQL_DATABASE=mysql_data
MYSQL_ROOT_PASSWORD=root
# variables used in importing and exporting DB data
MYSQL_USER=sa
MYSQL_PASSWORD=***REMOVED***
```

Build your containers:

```bash
./deploy.sh -e development
```

If you have made changes to your models, make and apply the new migrations.

```bash
docker-compose run --rm web ./manage.py makemigrations
docker-compose run --rm web ./manage.py migrate
```

You can import from the backup sql dump:

```bash
docker-compose exec mysql  bash ./scripts/import_mysql_backup.sh
```

And export:

```bash
docker-compose exec mysql  bash ./scripts/export_mysql_backup.sh
```

Once the stack is up and running, create a super user login:

```bash
docker-compose run --rm web ./manage.py createsuperuser
```

From there you can navigate to `http://0.0.0.0:8000` in your browser and login 
using the credentials you just created.

Run a command inside the docker container:

```bash
docker-compose run --rm web [command]
```

To stop the stack:

```bash
docker-compose down
```

To run unit tests:
```bash
docker-compose run --rm web ./manage.py test
```

You can programatically hit the API. Note you will need to generate a token 
from the admin panel.

```python
import requests

token = "[YOUR TOKEN HERE]"
headers = {"Authorization": f"Token {token}"}

r = requests.get("http://0.0.0.0:8000/api/v1/runs/", headers = headers)

r.json()
```

### Notes

* If the `swagger` or `redoc` pages don't load properly, you may need to run:

```bash
docker exec -it web python manage.py collectstatic --noinput
```

to pull in the static js files from the `drf-yasg` package.