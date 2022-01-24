```sh
$ cd ecodex
```
 
### Install dependencies
```sh
$ sudo apt-get install sqlite3 libsqlite3-mod-spatialite libgdal-dev
$ python -m venv venv
$ source venv/bin/activate # for linux based
$ pip install -r requirements.txt # or $ pipenv install
```
 
### Setup the application for running locally
 
```sh
$ python manage.py migrate
$ python manage.py makemigrations django_sslcommerz # if this is not listed in migration
$ python manage.py migrate django_sslcommerz
$ python manage.py oscar_populate_countries
$ python manage.py createsuperuser # enter valid information
```

### Run the application locally

```sh
$ python manage.py runserver
```

Open your browser and verify http://localhost:8000/
