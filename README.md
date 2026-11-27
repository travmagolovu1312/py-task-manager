# Task Manager
A web task manager for IT company .All members can create tasks , assing them to collegues or mark as complate.

## Features

-Registration, login log out 
-Tasks: list, details, create, update, delete, mark as done, assing yourself
-Workers with postitions; each worker page show complated and uncomplated tasks
-Positions , task types and tags(many-to-many with tasks)
-Pagination that keeps search query
-Overdue tasks are highlighted
-Counter of your tasks on the home page 

## Database structure

![DB diagram](docs/db-diagram.png)

## Tech stack

Python, Django, SQLite, Bootstrap 4, django-crispy-forms.

## Setup 

```Bash
git clone https://github.com/travmagolovu1312/py-task-manager.git
cd py-task-manager
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/ and log in.

## Tests and code style 

```Bash
python manage.py test
flake8
```

Please looks for my app , and give me your feedback on my GitHub account . Take care)
