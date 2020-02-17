# Give It Free


# RunSchedules

### Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

### General info
Give It Free is a web application that facilitates giving gifts to charity institutions.

The project was made as part of the Coders Lab course with the front-end templates provided.

##### Link to the web page
https://give-it-free.herokuapp.com/

### Technologies
* Python 3.7.5
* Django 2.2.7
* PostgreSQL 10.10
* HTML5
* CSS3
* JavaScript
* jQuery
* Ajax

### Setup
The Give It Free application has been deployed on heroku. Here's a direct link: https://give-it-free.herokuapp.com/.


To set up a project on your device, follow the steps below.

Fork and/or clone the repository to the selected folder using git clone command.

Create a virtual environment for the project, then activate it.
```
$ virtualenv -p python3 env
$ source env/bin/activate
```
Of course, you can also use IDE tools to configure the virtual environment.

Install all dependencies.
```
$ pip install -r requirements.txt
```
Configure your database in settings.py. You must change values of NAME - database name, USER - postgresql user(role) and PASSWORD - user(role) password.
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
    }
}
```
Then execute the migration to the database.
```
$ python manage.py migrate
```
Finally, you can run the application using the command:
```
$ python manage.py runserver
```
After that go to http://127.0.0.1:8000/. If all the steps were successful, the main page of the application should be displayed.

