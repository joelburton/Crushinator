"""
interrogation.py - base classes for building Interrogators (collections of questions, or 
_Probes_)
"""

from collections import OrderedDict
from crushinator.framework.probe import Probe

import logging
logger = logging.getLogger('crushinator.framework')

class __interrogation_meta__(type):
    """
    Metaclass for translating properties (probes) into a sequence
    """
    
    def __new__(cls, name, bases, dct):
        """
        Scan all of the properties of the about-to-be-created class instance,
        move any probes into the _probes collection. 
        
        Sets the 'name' property of the probe to the name of the attribute if 
        it's not already set
        
        @TODO: is it safe/smart to let the developer name the probe *and* provide it
               as an Interrogation attribute?
        @TODO: a way to change just a setting or two on a inherited probe? maybe pass
               a dict of values? A special ProbeDict object?
        """
        probes = OrderedDict()
        newdct = {}
        
        for base in bases:
            if getattr(base, '_probes', False):
                probes.update(base._probes)
                
        for k, v in dct.iteritems():
            if isinstance(v, Probe):
                if not v.name:
                    v.name = k
                probes[v.name] = v
            else:
                newdct[k] = v
        
        newdct['_probes'] = probes
        
        return type.__new__(cls, name, bases, newdct)
        

class Interrogation(object):
    """
    Base class for grouping Probes into 'ordered' lists.
    
    Works much like a dictionary (you can access an individual probe by name), 
    and also like a list (you can iterate through each probe).
    
    @note: there is no inherent or gaurenteed order here. The probe is left to 
           decide, given its value (or a suggested value) what comes next.
    """
    __metaclass__ = __interrogation_meta__
    __properties__ = {}
    
    def __init__(self, name, **kwargs):
        self.__properties__['name'] = name
        
        for k,v in kwargs.iteritems():
            self.__properties__[k] = v
            
        if self.__properties__.get('defaults') is None:
            self.__properties__['defaults'] = {}
    
    def get(self, propkey, default=""):
        """
        Easy grab of a __properties__ value, returns an empty string if
        it isn't set.
        """
        return self.__properties__.get(propkey, default)
    
    @property
    def probes(self):
        """
        Getter - returns a list of probes
        """
        return self._probes
    
    def reset(self):
        """
        Resets the interrogation so it can be looped through again, 
        sets all probe values to their default
        """
        self._processed = []
        
        for probe in self:
            probe.reset()
    
    def validate(self):
        """
        Check this Interrogation. Typically this means looping through the probes 
        and calling each probe's validate() method, but the Interrogation is
        free to use this method as it wishes. 
        
        If replicating the default implementation, you **must** let any 
        ProbeValidationError that is raised 'bubble up', so the UserInterface
        or Runner can handle it in the proper way. 
        
        Raises InterrogationVaidationError if the whole Interrogation is not 
        valid (but all Probe values check out)
        
        @note: To UserInterface writers, this is the proper way to access the 
               validity of the whole Interrogation, if all of the Probes validate.
        """
        for probe in self:
            probe.validate()
            
    def __iter__(self):
        """
        Generator; yield the next probe (or the next probe from another interrogation
        """
        for probe in self.probes:
            next = probe.next()
            
            if isinstance(next, Interrogation):
                for probe in next.probes:
                    yield probe
            elif isinstance(next, str):
                yield getattr(self, next)
            else:
                raise StopIteration
                
            yield probe
           
    
    def __getattribute__(self, key):
        """
        Override __getattr__ to try probe access first.
        
        This way you can do interrogation.probename to access a specific
        probe directly.
        
        Essentially makes the probe collection read-only
        
        @TODO: should probes be read-write?
        """
        probes = object.__getattribute__(self, '_probes')
        
        probe = probes.get(key, False)
        
        if probe:
            return probe
        else:
            try:
                return object.__getattribute__(self, key)
            except:
                raise

class InterrogationMixin(object):
    """
    Mix-in version for just adding/overriding a few probes without
    utilizing the whole 'stack'
    """
    __metaclass__ = __interrogation_meta__
    
