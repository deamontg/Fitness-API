"""
Filename: exceptions.py
Author: George Deamont <deamontg@gmail.com>
Description: 
"""


class NotFoundException(Exception):
    """
    Database entry not found.
    """
    pass


class DuplicateEntryException(Exception):
    """
    Integrity error.
    """
    pass