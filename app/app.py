"""
Filename: exercises.py
Author: George Deamont <deamontg@gmail.com>
Description: WSGI application setup.
"""

import falcon

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.middleware import JSONBodyParser

from app.resources import (
    MuscleResource,
    MuscleListResource,
    ExerciseResource,
    ExerciseListResource
)

from app.database import Database


# Middleware
middleware = [JSONBodyParser()]

# Initialize the API object
api = falcon.API(middleware=middleware)

# Initialize our database
db = Database(connection_string='postgres:///fitness-api')

# Initialize API resources
muscle = MuscleResource(db=db)
muscles = MuscleListResource(db=db)

exercise = ExerciseResource(db=db)
exercises = ExerciseListResource(db=db)

# Add routes
version = 'v1'

# TODO: implement related resources for attaching and detaching
api.add_route('/%s/muscles' % (version), muscles)
api.add_route('/%s/muscles/{id}' % (version), muscle)

api.add_route('/%s/exercises' % (version), exercises)
api.add_route('/%s/exercises/{id}' % (version), exercise)
