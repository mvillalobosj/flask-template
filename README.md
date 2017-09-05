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
* navigate to `localhost:5001/test`` in browser to verify.
