"""
Filename: muscles.py
Author: George Deamont <deamontg@gmail.com>
Description: Muscle resources.
"""

import falcon, json

from app.database import NotFoundException, DuplicateEntryException

from .base import BaseResource


def validate_muscle_data(data):
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


class MuscleListResource(BaseResource):
    """
    Resource for the list of muscles.
    """

    def on_get(self, req, resp):
        """
        GET list of muscles.
        """
        muscles = self.db.get_muscles()
        resp.body = json.dumps(muscles)
        resp.status = falcon.HTTP_200


    def on_post(self, req, resp):
        """
        POST a new muscle.
        """
        data = req.context['data']
        validated_data = validate_muscle_data(data)

        try:
            muscle = self.db.create_muscle(**validated_data)
            resp.body = json.dumps(muscle)
            resp.status = falcon.HTTP_201
        except DuplicateEntryException as e:
            raise falcon.HTTPConflict(title='Conflict Error', description=str(e))


class MuscleResource(BaseResource):
    """
    Resource for an individual muscle.
    """

    def on_get(self, req, resp, id):
        """
        GET a muscle my ID.
        """
        try:
            muscle = self.db.get_muscle(id)
            resp.body = json.dumps(muscle)
            resp.status = falcon.HTTP_200
        except NotFoundException as e:
            raise falcon.HTTPNotFound(title='Not Found', description=str(e))


    def on_delete(self, req, resp, id):
        """
        DELETE a muscle my ID.
        """
        try:
            self.db.delete_muscle(id)
            resp.status = falcon.HTTP_204
        except NotFoundException as e:
            raise falcon.HTTPNotFound('Not Found', str(e))