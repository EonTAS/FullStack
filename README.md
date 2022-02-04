# Purpose of the Project :

The aim of this project is to build a full-stack website that allows users to suggest and fund projects from me. It is intended to have a list of items that are suggested by users but must first must be approved by an admin before they are public and possible to be funded. Once a project is funded, the user who funded the project will recieve updates on the project. 

# Database Plan

ER diagram:

<img src="ReadmeFiles/ER Diagram.png" width=33% height=33% alt="ER Diagram">


# User Stories :

updated = https://docs.google.com/spreadsheets/d/1sFLzCsseC9m3GKSms0sC3RZ0PVqjxcl9ed3mu7amAZ0/edit#gid=1897577445
old = https://docs.google.com/spreadsheets/d/1NcOiJ0tNaxB6tHOtiMbEldtN8dBKBVe7acP4-AYfuMU/edit#gid=0

# Features :

Accounts
- viewing
Administration
- adding
- editting
- deleting
Comments
Updates
Paying
Suggesting
Viewing past purchases
login/logout

# Typography and Color Scheme :



# Client Story Testing

## Formatting/Lighthouse tests


### Lighthouse

Page | Desktop: | Performance | Accessibility | Best Practices | Mobile: | Performance | Accessibility | Best Practices 
--- | --- | --- | --- | --- |--- |--- |--- |--- |



# Deployment

create heroku
add postgres resource addon
pip install dj_database_url and psycopg2-binary 
import dj_database_url into settings.py and replace teh DATABASES object with url from heroku
superuser = u="admin" p="admin" e="exampleemail@email.com"
import gunicorn
setup procfile
disable heroku collectstatic

push to heroku with
heroku git:remote -a ci-eoncustoms
git push heroku main, master doesnt work for me for some reason

add all the environ things

amazon webservices setup
    why i have to enter card details ahhh

install boto3 django-storages
