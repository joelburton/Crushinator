"""
Tests for the various Probe implementations
"""

import unittest

invalid_floats = [
    '0.123sads',
    # weirdness
    "assdf.3123",
    "9.012as",
    "3.2.1",
    "   2.   245 ",
    '',
]

valid_floats = [
    '0.1234',
    '23.12242342',
    '123e10',
    '1.23e-10',
]

valid_integers = [
    # typical
    "12345",            # decimal
    "0777",             # octal
    "0xABC",            # hex
    "0b1110110101",     # binary
    # longs
    "12345L",
    "0777L",
    "0xABCL",
    "0b1110110101L",
    # negative
    "-12345",
    "-0777",
    "-0xABC",
    "-0b1110110101",
    # negative longs
    "-12345L",
    "-0777L",
    "-0xABCL",
    "-0b1110110101L",
    # whitespace?
    "   12345 ",           
    "   0777    ",         
    "   0xABC ",           
    "   0b1110110101",     
]

invalid_integers = [
    'abcde',
    # bigger than any known int and not a long
    # '2'*sys.maxint, <--- huuuuge on my system, probably not worth checking for
    '0xGGGA',
    '09999',
    '0.123sads',
    ''
]



# in strict mode, valid integers are also invalid
invalid_floats_strict = valid_integers + invalid_floats
# in unstrict mode, invalid integers should also be invalid
invalid_floats_nostrict = invalid_integers + invalid_floats
valid_floats_strict = valid_floats
valid_floats_nostrict = valid_integers + valid_floats

class TestValidation(unittest.TestCase):
    """
    Test the validation of the bundled probe implementations.
    
    @TODO: if these probes get any more complex, they should each have their
           own test cases.
    """
    
    def _run(self, probe, valuemap):
        """
        Given a probe, check it's validate() method for each
        value in valuemap, a list of two-tuples: (value, expected),
        
        where value is the value to check, and expected is either True or False.
        """
        for value, expected in valuemap:
            probe.value = value
            if expected is True:
                self.assertTrue(probe.validate(), "%s is not validating" % value)
            elif expected is False:
                self.assertFalse(probe.validate(), "%s is validating" % value)
    
    def test_Integer(self):
        """
        Test the Integer implementation
        """
        from crushinator.toolkit.probes import Integer
        
        to_check = [
            ('1', True),
            ('    -23', True),
            ('', False),
            ('0.2', False),
            ('-0.12421', False),
            ('a234234', False),
            ('123123123L', True),
            ('0234', True),
        ]
        
        self._run(Integer('probe'), to_check)
    
    def test_Float(self):
        """
        Test the Float implementation
        """
        from crushinator.toolkit.probes import Float
        
        to_check = [
            ('1', True),       # integers are technically valid floats
            ('    -23', True),
            ('', False),
            ('0.2', True),
            ('-0.12421', True),
            ('a234234', False),
            ('123123123L', True),
            ('0x3.a7p10', False),
            ('0234', True),
        ]
        
        self._run(Float('probe'), to_check)
    
    def test_Float_strict(self):
        """
        Test the Float implementation - strict set to True
        """
        from crushinator.toolkit.probes import Float
        
        to_check = [
            ('1', False),
            ('    -23', False),
            ('', False),
            ('0.2', True),
            ('-0.12421', True),
            ('a234234', False),
            ('123123123L', False),
            ('0x3.a7p10', False),
            ('0234', False),
        ]
        
        self._run(Float('probe', strict=True), to_check)
    
            
    def test_PythonName(self):
        """
        Test PythonName probe validation
        """
        from crushinator.toolkit.probes import PythonName
        
        to_check = [
            ('from', False),
            ('0badname', False),
            ('MyCoolVariable', True),
            ('__socool__', True),
            ('None', False),
            ('none', True),
            ('int_', True),
            ('are.namespaces.ok', False),
            ('', False),
            ('x12342', True),
            ('0x1234', False),
            ("'asdasd'", False),
            ("   myvar  ", True),
        ]
        
        self._run(PythonName('probe'), to_check)
        
    def test_PythonPackageName(self):
        """
        Test PythonPackageName probe validation
        """
        from crushinator.toolkit.probes import PythonPackageName
        
        to_check = [
            ('from', True),
            ('0badname', False),
            ('MyCoolVariable', False),
            ('__socool__', True),
            ('None', False),
            ('none', True),
            ('int_', True),
            ('are.namespaces.ok', False),
            ('', False),
            ('x12342', True),
            ('0x1234', False),
            ("'asdasd'", False),
            ("   myvar  ", True),
        ]
        
        self._run(PythonPackageName('probe'), to_check)
        
    def test_Email(self):
        """
        Test PythonPackageName probe validation
        """
        from crushinator.toolkit.probes import Email
        
        to_check = [
            ('me', False),
            ('me@', True),
            ('me@somehost@somethingelse', False),
            ('host@.com', True)
        ]
        
        self._run(Email('probe'), to_check)
        
class TestInterger(unittest.TestCase):
    """
    Put the Integer probe through its paces.
    """
    def test_getter_valid(self):
        """
        Ensure that the Integer getter returns an integer without error
        given each of the known numeric literals
        """
        from crushinator.toolkit.probes import Integer
        
        probe = Integer('probe')
        
        for integer in valid_integers:
            probe.value = integer
            self.assertTrue(isinstance(probe.value, (int)), "%s is not an integer" % integer)
        
    def test_getter_invalid(self):
        """
        Ensure that the Integer getter throws a ValueError for any improper values
        """
        from crushinator.toolkit.probes import Integer
        import sys
        
        probe = Integer('probe')
        
        for integer in invalid_integers+valid_floats:
            probe.value = integer
            try:
                x = probe.value
            except ValueError:
                pass
            else:
                self.fail("%s did not raise ValueError, coverted to %s" % (integer, x))
                
class TestFloat(unittest.TestCase):
    """
    Put the Float probe through its paces.
    """
    def test_getter_valid(self):
        """
        Ensure that the Float getter returns an float without error
        given each of the known numeric literals
        """
        from crushinator.toolkit.probes import Float
        
        probe = Float('probe')
        
        for float_ in valid_floats_nostrict:
            probe.value = float_
            self.assertTrue(isinstance(probe.value, (float)), "%s is not a float" % float_)
            
    def test_getter_valid_strict(self):
        """
        Ensure that the Float getter returns an float without error - strict mode
        """
        from crushinator.toolkit.probes import Float
        
        probe = Float('probe', strict=True)
        
        for float_ in valid_floats_strict:
            probe.value = float_
            self.assertTrue(isinstance(probe.value, (float)), "%s is not a float" % float_)
            
    def test_getter_invalid_strict(self):
        """
        Ensure that the Float getter fails when passed integers and strict is false.
        """
        from crushinator.toolkit.probes import Float
        
        probe = Float('probe', strict=True)
        
        for float_ in invalid_floats_strict:
            probe.value = float_
            try:
                x = probe.value
            except ValueError:
                pass
            else:
                self.fail("%s did not raise ValueError, coverted to %s" % (float_, x))
            
    def test_getter_invalid(self):
        """
        Ensure that the Float getter throws a ValueError for any improper values
        """
        from crushinator.toolkit.probes import Float
        import sys
        
        probe = Float('probe')
        
        for float_ in invalid_floats_nostrict:
            probe.value = float_
            try:
                x = probe.value
            except ValueError:
                pass
            else:
                self.fail("%s did not raise ValueError, coverted to %s" % (float_, x))
