# backend

Djando-Postgresql Backend for Vaanah

## How to setup this project

1- First install virtualenv with this command : $ pip install virtualenv

2- Then create your virtualenv with : $ virtualenv [virtualenv-name]

3- Activate the virtualenv :

* On Mac OS/Unix : $ source [virtualenv-name]/bin/activate
* On Windows : $ source [virtualenv-name]/Scripts/activate

4- You can now run the development server : $ python3 manage.py runserver


## Run the project with Docker

### Before building the image, make sure you have [docker](https://docs.docker.com/engine/install/) and [docker-compse](https://docs.docker.com/compose/install/) installed on your machine

You can run the application with this command ```docker-compose up --build -d```

The application is running in the port 8000
