"""
interrogation.py - base classes for building Interrogators (collections of questions, or 
_Probes_)
"""

class Interrogation(object):
    """
    Base class for grouping Probes into ordered lists.
    
    Works much like a dictionary (you can access an individual probe by name), 
    and also like a list (you can iterate through each probe).
    
    @note: there is no inherent or gaurenteed order here. The probe is left to 
           decide, given its value (or a suggested value) what comes next.
    """
    
    def __init__(self):
        pass
    
    
    def validate(self):
        """
        Check this Interrogation. Typically this means looping through the probes 
        and calling each probe's validate() method, but the Interrogation is
        free to use this method as it wishes. 
        
        If replicating the default implementation, you **must** let any 
        ProbeValidationError that is raised 'bubble up', so the UserInterface
        or Runner can handle it in the proper way. 
        
        @return: 
        
        @note: To UserInterface writers, this is the proper way to access the 
               validity of the whole Interrogation, if all of the Probes validate.
        """
        return True
    
    
