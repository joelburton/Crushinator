"""
Tests for the Aggregator base implementation.
"""

import unittest

def dummy_entry_point(self):
    return "Blah"

class TestAggregator(unittest.TestCase):
    """
    Basic tests for the Aggregator
    """  
    
    def setUp(self):
        from pkg_resources import EntryPoint
        
        spec = """
            ep1=crushinator.framework.tests.test_aggregator:dummy_entry_point
            ep2=crushinator.framework.tests.test_aggregator:dummy_entry_point
        """
        
        self.runner_entry_points = EntryPoint.parse_group('crushinator.runner', spec)
        self.collector_entry_points = EntryPoint.parse_group('crushinator.collector', spec)
    
    def test_entry_point_registered_call(self):
        """
        Check for registered entry points - crushinator.runner
        """
        from crushinator.framework.aggregator import RunnerAggregator
        
        r = RunnerAggregator()
        
        entry_points = r()
        
        raise
        
    def test_entry_point_nonexistent(self):
        """
        See what happens when an entry point doesn't exist.
        """
