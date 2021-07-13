# Fyyur
This is a project from Udacity. We can practice the app.py and config.py connection to database and html. It enhanced the skills in object relational map(ORM) and flask.

## enable migration
step1: initiate flask db
$ flask db init

step2:generate the initial migration:
$ flask db migrate -m "initial migration"

step3: with any other changes/ migration, always use:
$ flask db migrate -m "ANYTING CHANGED"

step4: apply the change to database
$ flask upgrade