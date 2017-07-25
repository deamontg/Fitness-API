"""
Filename: exercises.py
Author: George Deamont <deamontg@gmail.com>
Description: Exercise resources.
"""

import falcon, json

from app.database import NotFoundException, DuplicateEntryException

from .base import BaseResource


def validate_exercise_data(data):
    """
    Description:
        Validate the incoming POST data. Will raise an HTTPBadRequest
        exception on any validation errors.

    Parameters:
        - data: dict (should contain 'name' key and value should be a string.)

    Returns: dict
    """
    try:
        name = data['name']
    except KeyError:
        message = "Missing required data. Expected 'name' in the body."
        raise falcon.HTTPBadRequest(title='Bad Request', description=message)

    if name == None:
        message = "'name' must not be null."
        raise falcon.HTTPBadRequest(title='Bad Request', description=message)

    if not isinstance(name, str):
        message = "'name' must be a string."
        raise falcon.HTTPBadRequest(title='Bad Request', description=message)

    name = name.strip()
    
    if name == '':
        message = "'name' must not be empty."
        raise falcon.HTTPBadRequest(title='Bad Request', description=message)

    return {'name': name}


class ExerciseListResource(BaseResource):
    """
    Resource for the list of exercises.
    """

    def on_get(self, req, resp):
        """
        GET list of exercises.
        """
        exercises = self.db.get_exercises()
        resp.body = json.dumps(exercises)
        resp.status = falcon.HTTP_200


    def on_post(self, req, resp):
        """
        POST a new exercise.
        """
        data = req.context['data']
        validated_data = validate_exercise_data(data)
        
        try:
            exercise = self.db.create_exercise(**validated_data)
            resp.body = json.dumps(exercise)
            resp.status = falcon.HTTP_201
        except DuplicateEntryException as e:
            raise falcon.HTTPConflict(title='Conflict Error', description=str(e))


class ExerciseResource(BaseResource):
    """
    Resource for an individual exercise.
    """

    def on_get(self, req, resp, id):
        """
        GET an exercise by ID.
        """
        try:
            exercise = self.db.get_exercise(id)
            resp.body = json.dumps(exercise)
            resp.status = falcon.HTTP_200
        except NotFoundException as e:
            raise falcon.HTTPNotFound(title='Not Found', description=str(e))


    def on_delete(self, req, resp, id):
        """
        DELETE an exercise by ID.
        """
        try:
            self.db.delete_exercise(id)
            resp.status = falcon.HTTP_204
        except NotFoundException as e:
            raise falcon.HTTPNotFound(title='Not Found', description=str(e))