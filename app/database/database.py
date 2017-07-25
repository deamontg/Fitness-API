"""
Filename: database.py
Author: George Deamont <deamontg@gmail.com>
Description: Database wrapper for our models.
"""

from sqlalchemy import exc, create_engine
from sqlalchemy.orm import sessionmaker

from .models import Exercise, Muscle
from .exceptions import NotFoundException, DuplicateEntryException


class Database(object):
    """
    The main database object class definition. Will be referenced in all resources.
    """

    def __init__(self, connection_string):
        """
        Description: Creates a SQLAlchemy session and attaches it to this instance.
        """
        super(Database, self).__init__()
        
        engine = create_engine(connection_string, echo=False)
        session = sessionmaker(bind=engine)
        self.session = session()


    def get_exercises(self):
        """
        Description: Get all exercises.
        
        Parameters: None
        
        Returns: list
        """
        exercises = self.session.query(Exercise).all()
        return [{'id': e.id, 'name': e.name} for e in exercises]


    def create_exercise(self, name, **kwargs):
        """
        Description: Create a new exercise. Will raise an exception if there is a duplicate.
        
        Parameters:
            - name: Name of the new exercise.
        
        Returns: dict
        """
        try:
            exercise = Exercise(name=name)
            self.session.add(exercise)
            self.session.commit()
        except exc.IntegrityError:
            self.session.rollback()
            raise DuplicateEntryException('Exercise with name "%s" already exists' % (name))

        return {'id': exercise.id, 'name': exercise.name}

    
    def get_exercise(self, id):
        """
        Description: Get an exercise by ID. Will raise an exception if not found.
        
        Parameters:
            - id: ID of exercise to get.
        
        Returns: dict
        """
        exercise = self.session.query(Exercise).get(id)

        if exercise == None:
            raise NotFoundException('Exercise with ID "%s" not found' % (id))
        
        return {
            'id': exercise.id,
            'name': exercise.name,
            'muscles': [{'id': m.id, 'name': m.name} for m in exercise.muscles]
        }


    def delete_exercise(self, id):
        """
        Description: Delete an exercise by ID. Will raise an exception if not found.
        
        Parameters:
            - id: ID of exercise to delete.
        
        Returns: None
        """
        exercise = self.session.query(Exercise).get(id)

        if exercise == None:
            raise NotFoundException('Exercise with ID "%s" not found' % (id))

        self.session.delete(exercise)
        self.session.commit()
    

    def get_muscles(self):
        """
        Description: Get all muscles.
        
        Parameters: None
        
        Returns: list
        """
        muscles = self.session.query(Muscle).all()
        return [{'id': m.id, 'name': m.name} for m in muscles]


    def create_muscle(self, name, **kwargs):
        """
        Description: Create a new muscle. Will raise an exception if there is a duplicate.
        
        Parameters:
            - name: Name of the new muscle.
        
        Returns: dict
        """
        try:
            muscle = Muscle(name=name)
            self.session.add(muscle)
            self.session.commit()
        except exc.IntegrityError:
            self.session.rollback()
            raise DuplicateEntryException('Muscle with name "%s" already exists' % (name))

        return {'id': muscle.id, 'name': muscle.name}


    def get_muscle(self, id):
        """
        Description: Get a muscle by ID. Will raise an exception if not found.
        
        Parameters:
            - id: ID of muscle to get.
        
        Returns: dict
        """
        muscle = self.session.query(Muscle).get(id)

        if muscle == None:
            raise NotFoundException('Muscle with ID "%s" not found' % (id))
        
        return {
            'id': muscle.id,
            'name': muscle.name,
            'exercises': [{'id': e.id, 'name': e.name} for e in muscle.exercises]
        }


    def delete_muscle(self, id):
        """
        Description: Delete a muscle by ID. Will raise an exception if not found.
        
        Parameters:
            - id: ID of muscle to delete.
        
        Returns: None
        """
        muscle = self.session.query(Muscle).get(id)

        if muscle == None:
            raise NotFoundException('Muscle with ID "%s" not found' % (id))

        self.session.delete(muscle)
        self.session.commit()