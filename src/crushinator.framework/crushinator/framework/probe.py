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
    default = None
    value = None
    _value = None
    label = None
    description = None
    interrogation = None
    
    def __init__(self, name, **kwargs):
        self.name = name
        
        self.__dict__.update(kwargs)
    
    def next(self, value=None):
        """
        Return a probe name, the next Probe or Interrogation, given a certain
        value
        
        May raise a ProbeValidationError if the value isn't valid.
        
        Must raise StopIteration if there are no more Probes or Interrogations to
        move to.
        
        @param value: string, used in place of the current value of this Probe. 
                      Useful for peeking into what might be coming.
                      
        """
        
    def validate(self, value=None):
        """
        Check if this probe currently contains a valid value, or pass a value
        to check against (useful for prevalidating). 
        
        Raises a ProbeValidationError if the value doesn't check out.
        """
        return True
