"""
Tests for the Interrogation base implementation.
"""

import unittest

class TestInterrogation(unittest.TestCase):
    """
    Run through the basic functionality of the base Interrogation class.
    """
    @property
    def _class(self):
        """
        Build the test class when the testcase is instantiated.
        """
        from crushinator.framework.interrogation import Interrogation
        from crushinator.framework.probe import Probe
        
        class newinterrogation(Interrogation):
            name = Probe()
            email = Probe()
            
            __properties__ = {
                'name':"helloworld",
                'title':"hello world",
                'description':"this is a hello world interrogation"
            }
            
        return newinterrogation
        
    @property
    def _childclass(self):
        from crushinator.framework.probe import Probe
        
        class extender(self._class):
            email2 = Probe()
            email = Probe(label="booo")
            
        return extender
        
    @property
    def _mixinclass(self):
        from crushinator.framework.probe import Probe
        from crushinator.framework.interrogation import InterrogationMixin
        
        class mixer(InterrogationMixin):
            email = Probe(label="mixed-in override")
            mixedin = Probe()
            
        return mixer
        
    def test_probelookup(self):
        """
        Test the probe lookup
        """
        intero = self._class('helloworld')
        
        self.assertEqual(intero.name.name, 'name')
        
    def test_probe_iter(self):
        """
        Make sure that looping over the Interrogation produces the probes in the 
        right order
        """
        
        
    def test_probe_process(self):
        """
        Test the process() method of the Interrogation
        """
        
    def test_interrogation_jump_probe_iter(self):
        """
        Test what happens when iterating through an Interrogation and a probe 
        returns a different probe.
        """
        
    def test_interrogation_jump_interrogation_iter(self):
        """
        Test what happens when iterating through an Interrogation and a probe
        returns an interrogation
        """
        
    def test_properties(self):
        """
        Make sure the get() method works.
        """
        intero = self._class('helloworld')
        
        self.assertEqual(intero.get('title'), "hello world")
        
    def test_inheritence(self):
        """
        Make sure we can extend an interrogation 
        """
        interro = self._childclass('hello2')
        
        self.assertEqual(interro.email.label, 'booo')
        self.assertEqual(interro.email2.name, 'email2')
        
    def test_inheritence_multiple(self):
        """
        Test multiple inheritence: straight descendance
        """
        from crushinator.framework.probe import Probe
        
        class grandchild(self._childclass):
            email = Probe(label="grandchild")
            email3 = Probe()
        
        interro = grandchild('hello3')
        
        self.assertEqual(interro.email.label, 'grandchild')
        self.assertEqual(interro.email2.name, 'email2')
        self.assertEqual(interro.email3.name, 'email3')
        
        
    def test_inheritence_mixin(self):
        """
        Test multiple inheritence: mixin class
        """
        from crushinator.framework.probe import Probe
        
        class allmixedup(self._childclass, self._mixinclass):
            email = Probe(label="grandchild")
        
        interro = allmixedup('mixed')
        
        self.assertEqual(interro.email.label, 'grandchild')
        self.assertEqual(interro.mixedin.name, 'mixedin')
           
        
