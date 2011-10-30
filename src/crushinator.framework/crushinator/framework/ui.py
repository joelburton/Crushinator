"""
ui.py - base classes for building User Interfaces
"""

class UserInterface(object):
    """
    Base class for all Crushinator U.I.'s
    
    Responsible for proxying information back and fourth between the user and
    the Runner class(es) in play.
    """
    
    def __init__(self):
       """
       Parameters from the factory function can be accepted here.
       """

    def collector(self):
        """
        Return a Collector object. Typically not overloaded unless additional
        collectors are required.
        """

    def __call__(self):
        """
        The nerve center of the class; communicates with Runners and the User.
        """

    def defaults(self):
        """
        Return a dictionary of all default values, passed to the default Collector
        object. Alows the User Interface to pull defaults from places the collector
        may not understand (e.g. the Windows Registry, or CGI variables, etc)
        """

    def help(self, runner=None):
        """
        A common API method to assist users with use. Would be invoked upon a lack of
        user input or a certain command-line switch (--help)
        """  
        
    def runners(self):
        """
        Return a list of registered Runner classes for this UserInterface.
        """
        


