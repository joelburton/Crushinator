"""
Interrogations relevant to generating python package structures.
"""

from crushinator.framework.interrogation import Interrogation
from crushinator.framework.probe import Probe

from crushinator.framework.probes import PythonIdentifier, PythonPackageName, Email

class PackageMeta(Interrogation):
    """
    Interrogation that holds basic meta data for a python package
    """
    __properties__ = {
        'title': 'Package Metadata',
        'description': "Common metadata used for submission to PYPI",
    }
    author = Probe(label="Author's Name")
    email = Email(label="Author's E-mail Address")
