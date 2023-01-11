# Sway (Backend)
Django (Python) API for Sway's mobile application

# Overview
Sway is a mindfulness web-app that provides numerous features to help a user achieve their goals.

## Code Installation:
Clone or download the repository and run the following within the terminal:
- Enter virtual environment for project: virtualenv env && source env/bin/activate
- Install dependencies: pip install -r requirements.txt
- Make migrations: python manage.py makemigrations
- Migrate: python manage.py migrate
- Load the seed data for each Django app (articles, comments, jwt_auth, meditations, notes) by replacing ‘app’ with the app name: python manage.py loaddata app/seeds.json
- NB at this stage you can run python manage.py runserver and view the web-app in its static form.
- Initialise the backend server: python manage.py runserver

### Existing Web Version
<img width="712" alt="Screenshot 2021-12-28 at 12 01 07" src="https://user-images.githubusercontent.com/89992629/147564313-68ae0ae7-9c23-421b-bb22-b8224bd34129.png">

# Technologies Used

### Back-End
- Django
- Django REST Framework
- Psycopg2
- PyJWT
- Python

### Front-End

- React Native
- Expo

### Development Tools
- Jira (project management)
- Cloudinary (media hosting)
- Git
- GitHub
- Miro (planning)
- NPM
- Postman
- VS Code
