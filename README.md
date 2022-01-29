Plan:

Make a commisions website that advertises my/someones work, gives rates and allows requests and progress updates as they are made of given projects. 

User Stories:
https://docs.google.com/spreadsheets/d/1NcOiJ0tNaxB6tHOtiMbEldtN8dBKBVe7acP4-AYfuMU/edit#gid=0

Sketches:



used

django
allauth

https://learn.codeinstitute.net/courses/course-v1:CodeInstitute+FSF_102+Q1_2020/courseware/4201818c00aa4ba3a0dae243725f6e32/a5315728ccdf4f0792a0bc3c349e8329/?child=first
https://learn.codeinstitute.net/courses/course-v1:CodeInstitute+FSF_102+Q1_2020/courseware/4201818c00aa4ba3a0dae243725f6e32/71413627006c4cac9b18a1de1e12a4ff/
pip3 install -r requirements.txt
python3 manage.py runserver

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