# innometrics-ext

Storage of Commit ID and Project URL when user enters GithubID.

# Installation :
## Server pre-requiremnts:
1. postgreSQL, created database, created database user, granted all to this owner.
2. python 3 or 2.7
3. pip

## Installation:
pip install -r requirements;
python manage.py makemigrations;
python manage.py migrate;
python manage.py runserver;


## Database Settings:
Go to: InnoMetricsserver/settings and change the name of database and add user and password for postgre.
 Example:
 DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'innometric',
        'USER': 'admin',
        'PASSWORD': '1234',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

## On Broswer:
Go to:
1. http://127.0.0.1:8000/commit/githubuser/
2. Enter Github ID of the user 
3. Commit data is in database. (Measurements,Activity)
