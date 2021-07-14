import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql://yanxu@localhost:5432/fyyur'

# supporess the warnings
### "SADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress this warning.
  #'SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and'"
SQLALCHEMY_TRACK_MODIFICATIONS = False