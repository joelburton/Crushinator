"""
Implementation of common probe types
"""

from crushinator.framework.probe import Probe

import keyword, re, tokenize

identifier = re.compile(r'^('+tokenize.Name+r')$')
starts_with_nonalpha = re.compile(r'^[\d\s]+')

hexnumber = re.compile(r'^-?'+tokenize.Hexnumber)
octnumber = re.compile(r'^-?'+tokenize.Octnumber)
binnumber = re.compile(r'^-?'+tokenize.Binnumber)
decnumber = re.compile(r'^-?'+tokenize.Decnumber)
integer = re.compile(r'^-?'+tokenize.Intnumber)
float_ = re.compile(r'^-?'+tokenize.Floatnumber)
expfloat = re.compile(r'^-?'+tokenize.Floatnumber)

import logging
logger = logging.getLogger('crushinator.toolkit')
        

def coerce_int(value):
    """
    Given a string value, coerce it into an integer.
    
    Will raise a ValueError if it's not possible.
    """
    if value is '':
        raise ValueError
    
    if value[-1] in ('L', 'l'):
        return int(long(value, 0))
    else:
        return int(value, 0)
        
def coerce_float(value, strict=False):
    """
    Given a string value, coerce it into a float.
    
    If strict is True, throws a ValueError if value doesn't appear to be
    a float
    """
    if value is '':
        raise ValueError
        
    # appears to be an integer, - have to do both checks to catch the valid python numeric identifiers
    if not float_.match(value):
        logger.debug("integer detected: %s" % value)
        if strict:
            raise ValueError
        else:
            # so use the coerce_int() function to covert it
            return float(coerce_int(value))
    
    return float(value)

class PythonInteger(Probe):
    """
    Must be a valid Integer value for python
    
    Supports standard Python notations:
        234234223423L - Long integer
        0123 - Octal
        0xABC - Hexidecimal
        0b1101101101 - Binary
        
    No coersion is done on the back-end (e.g. self.value is always
    a string, ready to be used as a literal in python code - use Integer if 
    you need to use the number in math operations)
    
    @TODO: is it useful/practical to check if the int would be larger than sys.maxint?
    @TODO: does it make sense to manipulate the value on save()? 
    """
    def validate(self):
        try:
            coerce_int(self._value)
        except ValueError:
            logger.debug("Could not convert %s to an integer" % (self._value))
            return False
        else:
            return True
            
class Integer(PythonInteger):
    """
    Must be a valid, simple integer. Conversion to a regular integer happens when
    the value is accessed.
    
    Supports same notation as PythonInteger.
    
    @TODO: is it useful/practical to check if the int would be larger than sys.maxint?
    """
    def coerce(self):
        return coerce_int(self._value)
                
class PythonFloat(Probe):
    """
    Must be a valid python float. Suitable for embedding as a numeric literal
    in python code.
    
    Accepts the same forms of notation as PythonInteger
    
    Adds strict parameter. Set to False, integers are considered valid floats.
    
    @TODO: does it make sense to manipulate the value on save()? 
    @TODO: handle NaN, scientific notation (exponents, e.g. 
    """
    strict = False
    
    def validate(self):
        try:
            coerce_float(self._value, self.strict)
        except ValueError:
            logger.debug("Could not convert %s to a float (strict is %s)" % (self._value, self.strict))
            return False
        else:
            return True
    
    
class Float(PythonFloat):
    """
    Must be a valid, simple float. Conversion to a regular float happens when
    the value is accessed.
    
    Supports same notation as PythonFloat.
    """
    def coerce(self):
        return coerce_float(self._value, self.strict)
            
class PythonName(Probe):
    """
    Must be a valid python identifier
    
    This means it's NOT a keyword *and* it matches http://docs.python.org/reference/lexical_analysis.html#identifiers
    
    @TODO: catch other language quirks like 'can't assign to None'
    """
    _other_bad_ids = ('None',)
    
    def validate(self):
        # if it starts with one or more non-alpha characters, it's invalid
        if starts_with_nonalpha.match(self._value):
            logger.debug("%s begins with a non-alphanumeric character" % self._value)
            return False
        
        if not identifier.match(self._value):
            logger.debug("%s doesn't look like a proper identifier" % self._value)
            return False
            
        if keyword.iskeyword(self._value):
            logger.debug("%s is a python keyword" % self._value)
            return False
        
        if self._value in ('None'):
            logger.debug("%s is one of (%s)" % (self._value, ','.join(self._other_bad_ids)))
            return False
        
        return True
        
class PythonPackageName(Probe):
    """
    Must be a valid identifier, but not necessarily a keyword.
    
    Also must be lower case.
    
    @TODO: check if this is importable?
    """
    def validate(self):
        lowercase = self._value.islower()
        isidentifier = identifier.match(self._value)
        
        return (lowercase and isidentifier)
        
class Email(Probe):
    """
    Simple e-mail check (just looks for a single @ character)
    """
    def validate(self):
        if self._value.count('@') == 1:
            return True
        else:
            return False
