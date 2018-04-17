# innometrics-ext

<<<<<<< HEAD
Visualisation + storage for some abstract activities + rest API for the data-delivery agents.
=======
Storage of Commit ID and Project URL when user enters GithubID.
>>>>>>> b08e6a3e8b2c2dd9bc6e05534b8e9593d0bb7dab

# Installation :
## Server pre-requiremnts:
1. postgreSQL, created database, created database user, granted all to this owner.
<<<<<<< HEAD
2. python3
3. pip
4. npm

## Installation:
 - pip install -r requirements.txt;
 - python manage.py syncdb;
 - cd frontend
 - npm install
 - ./node_modules/.bin/webpack -d
=======
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

## Test:
pip install coverage==3.6

coverage run manage.py test commit -v 2

>>>>>>> b08e6a3e8b2c2dd9bc6e05534b8e9593d0bb7dab
