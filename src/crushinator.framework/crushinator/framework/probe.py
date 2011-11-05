"""
probes.py - base classes for building Probes
"""

class Probe(object):
    """
    Base class definition for collecting data from the user. 
    
    @ivar name: string, name of the variable used in the template, used to 
                identify it.
    @ivar default: string, default value if the user doesn't specify something 
                   new. Class default may be overridden by any Collector's in the
                   mix.
    @ivar value: the *current* value of this probe. This may change over time.
    @ivar _value: the *original* value of this probe. This should **not** change.
    @ivar label: the label (user prompt) for this probe. 
    @ivar description: a longer, more verbose explaination of what the probe wants. 
    @ivar interrogation: a reference to the probe's parent Interrogation object. 
                         Useful for probe-level invariant checking.
    
    @todo: create mechanism (setting? decorator?) to *prevent* a label, help, or 
           description property from being run through the RST transformation by
           the UI.
    @todo: Should there be a cleaning step in the probe? I think that might fall
           under the UserInterface or the Runner's jurisdiction, but it's 
           unclear at this point.
    """
    name = None
    default = ''
    _value = ''
    label = None
    description = None
    interrogation = None
    
    def __init__(self, **kwargs):
        """
        Constructor - initialize variables
        """
        for k,v in kwargs.iteritems():
            setattr(self, k, v)
        
        self.reset()
    
    def next(self, value=None):
        """
        Return a probe name, or Interrogation, given a certain
        value
        
        May raise a ProbeValidationError if the value isn't valid.
        
        Must raise StopIteration to cease looping.
        """
        return None
    
    @property
    def value(self):
        """
        Getter for the value of this probe. Provides a hook for coerce() below
        """
        return self.coerce()
    
    @value.setter
    def value(self, value):
        """
        Setter for the value of this probe. Provides a hook for save() below
        
        @todo: should this ensure the value is a string?
        """
        self.save(value)
    
    @value.deleter
    def value(self):
        """
        Deleter added for the sake of completeness. Provides hook for delete() method
        below
        """
        self.delete()
    
    def coerce(self):
        """
        Convert the string value of this probe into a python type
        
        @note: this method should not swallow any exceptions, or try to validate the value.
        @see: Probe.validate()
        """
        return self._value
        
    def save(self, value):
        """
        Provided to allow the developer to manipulate the value before its saved
        
        Stripping leading/trailing whitespace seems reasonable for most probes, so 
        the base implementation is doing it too.
        
        @TODO: would it be better to break this out into a child class?
        """
        self._value = value.strip()
        
    def delete(self):
        """
        Provided to allow the developer to do something special when the value of 
        this probe is deleted
        """
        del self._value
    
    def validate(self):
        """
        Check if this probe currently contains a valid value.
        Raises a ProbeValidationError if the value doesn't check out.
        """
        return True
        
    def reset(self):
        """
        Return to the default value
        """
        self._value = self.default
