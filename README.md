# backend
Djando-Postgresql Backend for Vaanah

1- First create your virtualenv with : $ virtualenv [virtualenv-name]

If you don't have a virtualenv yet you 'll need to install it first with this command : $ pip install virtualenv.
Then create your virtualenv with the command below.

2- Activate the virtualenv : 
    * On Mac OS/Unix : $ source [virtualenv-name]/bin/activate 
    * On Windows : $ source [virtualenv-name]/Scripts/activate 

3- After install django : $ pip install django

4- Start the django project with this command : $ django-admin startproject [project-name].
Then go to project folder : cd [project-name]

5- Generate requirements file : $ pip freeze > requirements.txt

6- Install project dependencies: $ pip install -r requirements.txt

7- Then simply apply the migrations : 
    * $ python manage.py makemigrations 
    * $ python manage.py migrate

8- You can now run the development server : $ python manage.py runserver