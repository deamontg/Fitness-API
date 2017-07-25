"""
Filename: models.py
Author: George Deamont <deamontg@gmail.com>
Description: API database models.
"""

from sqlalchemy import Table, Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import backref, relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


exercise_muscle_association_table = Table(
    'exercise_muscle_association',
    Base.metadata,
    Column('exercise_id', Integer, ForeignKey('exercise.id')),
    Column('muscle_id', Integer, ForeignKey('muscle.id'))
)


class Exercise(Base):
    """
    """
    __tablename__ = 'exercise'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    
    muscles = relationship(
        'Muscle',
        secondary=exercise_muscle_association_table,
        backref='exercises'
    )

    def __repr__(self):
        """
        """
        return "<Exercise('id'='%s', name='%s')>" % (self.id, self.name)


class Muscle(Base):
    """
    """
    __tablename__ = 'muscle'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __repr__(self):
        """
        """
        return "<Muscle('id'='%s', name='%s')>" % (self.id, self.name)