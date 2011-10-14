"""
Crushinator Exceptions.
"""
class ValidationError(Exception):
    """
    Base validation exception class. Put here so you can just catch any problems
    with validation, or take different action depending on what sort of 
    validation error has occurred.
    
    All ValidationErrors should accept a message to be sent back to the user.
    
    This means that the messages can contain reStructuredText, and should be 
    passed through a translator.
    """


class ProbeValidationError(ValidationError):
    """
    Raised when a probe tries to validate a value, and it can't.
    """
    
class InterrogationValidation(ValidationError):
    """
    Raised when an entire Interrogation is invalid. This can be due to an 
    invariant constraint check (say, two probes that collect and verify a users
    password don't match), or some other Interrogation-specific validity issue.
    """
    
class ProbeNotFound(Exception):
    """
    Raised when a probe is being located, and it does not exist.
    """
