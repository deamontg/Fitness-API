"""
Filename: base.py
Author: George Deamont <deamontg@gmail.com>
Description: BaseResource definition.
"""

class BaseResource(object):
    """
    All resources have a database connector.
    """

    def __init__(self, db):
        """
        """
        super(BaseResource, self).__init__()
        self.db = db