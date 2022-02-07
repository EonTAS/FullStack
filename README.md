# Purpose of the Project :

The aim of this project is to build a full-stack website that allows users to suggest and fund projects from me. It is intended to have a list of items that are suggested by users but must first must be approved by an admin before they are public and possible to be funded. Once a project is funded, the user who funded the project will recieve updates on the project. 

# Database Plan

ER diagram:

<img src="ReadmeFiles/ER Diagram.png" width=33% height=33% alt="ER Diagram">


# User Stories :

final = https://docs.google.com/spreadsheets/d/1jG73GFRLvYHsPywI3yQd7GhOhZQMBknOJv9utC2AUfU/edit#gid=0

updated = https://docs.google.com/spreadsheets/d/1sFLzCsseC9m3GKSms0sC3RZ0PVqjxcl9ed3mu7amAZ0/edit#gid=1897577445

old = https://docs.google.com/spreadsheets/d/1NcOiJ0tNaxB6tHOtiMbEldtN8dBKBVe7acP4-AYfuMU/edit#gid=0


| As A..    | I want to be able to...                                                 | So that...                                                             |
| --------- | ----------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| Site user |                                                                         |                                                                        |
| \`        | Register                                                                | i can comment on, fund and suggest new projects                        |
| \`        | Login                                                                   | i can access my account                                                |
| \`        | Reset password                                                          | i can log in if i forget details                                       |
| \`        | enable/disable emails                                                   | my preferences are followed                                            |
| \`        | leave comments                                                          | my opinion is seen on the projects                                     |
| \`        | View Details on a given project                                         | i can see whats being made                                             |
| \`        | View Comments                                                           | i can view others views                                                |
| Shopper   |                                                                         |                                                                        |
| \`        | View all projects                                                       | i can see what kinds of things have been made/are currently being made |
| \`        | Sort projects                                                           | i can see projects in an order i like                                  |
| \`        | Search projects                                                         | i can find projects that fit in a description i like                   |
| Suggester |                                                                         |                                                                        |
| \`        | Suggest a project                                                       | my idea is seen and could be made                                      |
| \`        | view all projects i've suggested                                        | i can go back and see if theres any changes to them                    |
| \`        | view updates on projects i've suggested                                 | i can see what changes have been made                                  |
| \`        | recieve email updates on projects i've suggested                        | i can be notified of updates                                           |
| Funder    |                                                                         |                                                                        |
| \`        | Fund a project                                                          | it can be made and i can know its being made                           |
| \`        | Safely pay for funding with card and know that my purchase went through | my payment can be made and i can know it worked out                    |
| \`        | View all projects i've funded                                           | i can go back and see if theres any changes to them                    |
| \`        | view updates on projects i've funded                                    | i can see what changes have been made                                  |
| \`        | recieve email updates on projects i've funded                           | i can be notified of updates                                           |
| Admin     |                                                                         |                                                                        |
| \`        | Edit a project thats already up                                         | its details can be adjusted to better fit what can actually be done    |
| \`        | approve not yet approved projects so they are visible to all users      | it is visible to users to then fund                                    |
| \`        | Delete bad projects                                                     | if its not fitting to the website it can be declined                   |
| \`        | Currate comments/delete comments                                        | spam can be removed                                                    |
| \`        | Send Project updates out                                                | the people who funded/suggested it can see what progress is being made |

# Features :



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
