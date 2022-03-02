# Maktabkhoone Challenge

This service is a rest api django web application that manages users, teachers, courses and their reviews.

###


## Running tests

* in order to run tests run the following command in mysite directory: `python manage.py test`


## Deployment

simply use

* `docker-compose up -d --build`

or if used with swarm :

* `docker stack deploy -c docker-compose.yaml --with-registry-auth maktabkhoone`

and then service will start on port 80. you can change port in docker-compose file.