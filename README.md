<div align="center">
  
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

</div>
  
# Table of Content
<details>
  <summary>Show</summary>
  
- [Table of Content](#table-of-content)
- [About](#about)
  - [Features](#features)
  - [Screenshots](#screenshots)
- [Configuration](#configuration)
- [Building](#building)
  - [Development](#development)
    - [Testing](#testing)
  - [Production](#production)
- [Usage](#usage)
  - [Development](#development-1)
  - [Production](#production-1)
  
</details>
  
# About
## Features

* WebUI
  * See logged hours in list view or calendar view.
  * Edit or remove existing entries.
  * Generate an API token to use the REST API.
  * Punch in or out directly from the WebUI.
* REST API
  * One simple endpoint to punch in or out if already punched in (toggle): `/api/punch`.
  * BEARER authentication.

## Screenshots
<details>
  <summary>Show</summary>
  
* List View
![List View](images/list.png)

* Calendar View
![Calendar View](images/calendar.png)

* Edit an entry
![Edit entry](images/edit_entry.png)

* Generate API Token
![Generate API Token](images/API_token.png)
  
</details>

# Configuration
See the [development `env` file](.env.dev) or the [production `env` file](.env.prod) for available configurations.

# Building
## Development
1. Build the image
```shell
$ docker compose -f docker-compose.yml up --build
```
2. Add the initial admin user
```shell
$ docker compose exec web python manage.py createsuperuser --username=admin --email=admin@example.com
```

### Testing
Run the available tests with
```shell
$ docker compose exec web python manage.py test
```

## Production
1. Build the image
```shell
$ docker compose -f docker-compose.prod.yml up --build
```
2. Create the database layout
```shell
$ docker compose exec web python manage.py migrate --no-input
```
3. Collect the static files for nginx
```shell
$ docker compose exec web python manage.py collectstatic --no-input --clear
```
4. Add the initial admin user
```shell
$ docker compose exec web python manage.py createsuperuser --username=admin --email=admin@example.com
```

# Usage
## Development

Visit the website under http://127.0.0.1:8000.

## Production

Visit the website under http://127.0.0.1.
