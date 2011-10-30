"""
crushinator.toolkit.skeletons.package - python package-related Skeletons.
"""

from crushinator.framework.skeleton import Skeleton
import os

class BasePackage(Skeleton):
    """
    Implements boilerplate common to all python packages
    """
    
    def __init__(self, **kwargs):
        super(Skeleton, self).__init__()
        self.source = os.path.join(os.path.dirname(__file__), 'templates')
