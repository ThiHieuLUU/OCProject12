# Project 12
## 1. About the project 12
This project is realized with Django REST framework. 
It allows to perform CRUD operators for a CRM (Customer Relationship Management) system via the endpoints of an API.
In the project, Epicevents company wishes handle securely theirs clients and theirs associated contracts and events.

## 2. The specific points implemented in the project
* There're three groups pre-built for users (see in users/migrations): Managers, Sellers and Supporters.
The Managers group has all permissions, in particular, can create a user and designate the user's role 
(is in Sellers group or is in Supporters group).
However, a seller or a supporter has some limited permissions on clients, contracts and events 
(in general, they can only handle theirs own clients with associated contracts and events).

* All the users (manager, seller, supporter) can use the admin page or the API to perform theirs CRUD operators. 
* Admin page is configured to limit permission for each authenticated user (according to his role).
Then these permissions are shared to API (via permissions.py file), this allows users can work not only 
with the API but also with the admin page.
* Sentry for Django is taken in place in order to trace bugs (see https://docs.sentry.io/platforms/python/guides/django/)
* A branch "api_nested_endpoints" can be found in this project, which allows using nested endpoint format in the API.
* The "main" branch doesn't use nested endpoint format in the API in order to make sense for filter operators.
## 3. About the main structure
* Project "epicevents_project", containing:
  * Application: users
  * Application:  events

## 4. Process
1. Clone and launch the project:
```
git clone  https://github.com/ThiHieuLUU/OCProject12.git
cd OCProject12/

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt 

cd epicevents_project/
python manage.py makemigrations
python manage.py migrate
python manage.py runserver --insecure
```
In order to perform the requests, go to http://127.0.0.1:8000/admin/ if using the admin page or http://127.0.0.1:8000/ with the endpoints of API (see Postman documentation).

## 5. Check code with flake8
* See flake8 configuration in "setup.cfg" file.
* Check code:
```bash
cd epicevents_project
flake8 --format=html --htmldir=flake8-report
```
* Result:
```bash
firefox flake8-report/index.html &
```

## 6. Postman documentation
See [here](https://www.postman.com/crimson-capsule-423643/workspace/project12) for Postman documentation of this API.