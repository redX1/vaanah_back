# Build and run a PostgreSQL image locally

### Before building the image, make sure you have [docker](https://docs.docker.com/engine/install/) installed on your machine

### Follow these steps :

1. Build the image by running this command : ```docker build -t give_a_tag -f- . < Dockerfile.postgres``` *provide the tag you want to your image(ex eg_postgresql)*
2. Run the image with this command : ```docker run -d --rm -p listening_port:5432 given_tag``` *provide a free port of your machine *


### During the image launch, this is what was created:

1. A user with this credentials :
 - username : *vaanah_user*
 - password : *secret*

*you can change the user credentials by changing the line 31 of the Dockerfile, ```CREATE USER provide_a_username WITH SUPERUSER PASSWORD 'provide a password'```, you have to build and run the image to see the changes*

2. A database called *vaanahdb*

*you can change the database name by changing the line 32 of the Dockerfile, ```createdb -O provide_the_database_owner provide_a_database_name```, you have to build and run the image to see the changes*