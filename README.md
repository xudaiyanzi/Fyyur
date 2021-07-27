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

## Extra work

beyond the requirements in Udacity, I also add the "edit and delete" function in "Artist" and "Shows" pages.

I also used "join" to present the shows and artists info in Venue page; and the shows and venues info in Artist page

Most importantly, the constrains in phones/weblinks are included in venue page. 

## To be improved

I should revise the constrains in phones/weblinks in both artists and venues page. I should not make it very restrictly.