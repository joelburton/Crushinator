"""
collector.py  - Base class for collecting default values from common locations.
"""

class BaseCollector(object):
    """
    Base class to define method signatures. Separated from Collector due to 
    implementation code.
    """
    
    def __init__(self, **kwargs):
        """
        Any run-time, out-of-band defaults, or overrides can be specified in the
        constructor.
        
        @param kwargs: all keyword arguments passed will be added as final global
                       values
        """

    def __call__(runner=None):
        """
        Returns a dictionary of values for a specific Runner class; ignores
        runner-class sections if caller is not specified.
        
        @param runner: string, class object, or Runner instance.
        """
