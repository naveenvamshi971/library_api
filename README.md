1. First I ran the following command to create the given project library_api
django-admin startproject library_api
cd library_api

I have django installed aleady

python -m pip install Django

2. Created another app called books
python manage.py startapp books

3. Updated INSTALLED_APPS in library_management/settings.py:

python
Copy code
INSTALLED_APPS = [
    'rest_framework',
    'books',  
]

4. Changed the Database to PostgreSQL in settings.py:

python
Copy code
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'librarydatabase',
        'USER': 'xxxxx',
        'PASSWORD': 'xxxxx',
        'HOST': 'localhost',
        'PORT': 'xxxx',
    }
}

Note we need PostgreSQL to be installed prior to this.

5. Create View, Define URLs register model and now make migrations
python manage.py makemigrations books
python manage.py migrate

6. I got error related to DRF. Install DRF
pip install django djangorestframework

Also, for token based authentication
pip install djangorestframework-simplejwt

7. To run server
python manage.py runserver

8. In the process,I created superuser 
python manage.py createsuperuser


http://127.0.0.1:8000/api/token/ to generate token for the user created

Now using this Bearer token, we can test all the API end points. To see the tests,refer Postman collections I have shared.

9. I've used DRF’s built-in documentation features to document my API endpoints using drf_yasg library
pip install drf_yasg
