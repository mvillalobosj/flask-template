Flask Template is designed to get you up and running with a Python Flask API with support for common auxilary features.

## Technologies Used
* [Python 3.6](https://docs.python.org/3/) - Python Programming Language
* [Flask](https://github.com/pallets/flask) - Python API MicroFramework
* [Flask-apispec](https://github.com/jmcarp/flask-apispec) - Works with Flask and marshmallow to automatically build Swagger documentation.
* [marshmallow](https://github.com/marshmallow-code/marshmallow) - Used for serialization/deserialization of request/response data.
* [sqlalchemy](https://github.com/zzzeek/sqlalchemy) - SQL ORM for querying a DB and managing DB connections.
* [yamlsettings](https://github.com/KyleJamesWalker/yamlsettings) - Configuration management 
* [yoyo-migrations](https://pypi.python.org/pypi/yoyo-migrations) - DB Migration Script management.
* [gunicorn](https://github.com/benoitc/gunicorn) - Python HTTP Server for managing multiple connections.
* [docker](https://docs.docker.com/) - Container service for abstracting deployment environment.
* [docker-compose](https://docs.docker.com/compose/) - Docker management service.

## Common Features Not Included
* User Authentication
  * While the example provided uses a User table, authenticating the user is left up to the author. Google/Facebook auth or rolling up your own are all viable strategies.
* User Permissions
  * This is tied to user authentication. While you can roll up your own with your own table or strategy for permissions, this is open-ended.
* Managed Deployment Strategies
  * There are no files here that presume one deployment strategy over another. A Dockerfile is provided which can be used.
* Secrets Management
  * This pertains to passwords of production services. These should never be checked into your repo and there are multiple strategies for managing secrets. A `settings.yml` file can be created which is part of the .gitignore which can be used to hold your secrets, however ensuring that it is secure and the correct file is running on your server is left up to the author.
* Reverse Proxy/HTTP Server
  * This is usually used to direct flow to your Python app in a sterile and managed way. [Nginx](https://nginx.org/en/docs/) is an example of such a service and for a production environment should be definitely used.
* HTML Frontend
  * The template is for an API only. Considering how many possible strategies there are for an HTML Frontend, this doesn't presume to build one. A simple one can be created through jinja templates and they work well with Flask. Refer to the Flask documentation to see how to add this.

## Installation
### Install Steps:
* install docker
* install postgres
* run following commands:
  * `createdb db`
  * `cp yoyo_template.ini yoyo.ini`
    * if using docker for mac, change `localhost` to `docker.for.mac.localhost`
  * `cp defaults.yml settings.yml`
    * if using docker for mac, change `localhost` to `docker.for.mac.localhost`

### Run Migrations
(Run whenever there are new migrations in the migrations folder)
* docker-compose run api yoyo apply

### Build App
(Run whenever `requirements.txt` or `Dockerfile` changes)
* `docker-compose build api`

### Run App
* `docker-compose up api`
* navigate to `localhost:5001/hello`` in browser to verify.
* navigate to `localhost:5001/swagger.json` to view swagger docs for the API endpoints.
