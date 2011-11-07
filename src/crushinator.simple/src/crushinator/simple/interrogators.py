from crushinator.framework.interrogation import Interrogation
from crushinator.framework.probe import Probe


class SimpleLicense(Interrogation):
    """
    Interrogation that asks what license you want
    """
    
    __properties__ = {
        'label': 'Simple License',
        'description': 'Ask user for their preferred license'
    }
    
    # XXX: constructor should allow passing valid vocab for select
    license = Probe(label="License Name",
                    name='crushinator.probes.license')

