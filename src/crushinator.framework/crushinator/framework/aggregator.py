"""
templer.framework.aggregator
"""

from pkg_resources import iter_entry_points, load_entry_point

class Aggregator(object):
    """
    Base class - retrieves all entry points based on an internal identifier.
    """
    _group = None
    
    def __call__(self):
        """
        Returns all of the entry points for this Aggregator
        """
        return iter_entry_points(group=self._group)
        
    def __iter__(self):
        """
        Generator; returns a single entry point.
        """
        for entry_point in iter_entry_points(group=self._group):
            yield entry_point
        
class RunnerAggregator(Aggregator):
    _group = "crushinator.runner"
    
class CollectorAggregator(Aggregator):
    _group = "crushinator.collector"
    
