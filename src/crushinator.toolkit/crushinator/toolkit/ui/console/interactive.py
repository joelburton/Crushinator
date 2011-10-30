"""
crushinator.toolkit.ui.console - Interactive console front end for code generation 
systems
"""

from crushinator.framework.ui import UserInterface
from crushinator.toolkit.collector.default import DefaultCollector

import logging
logger = logging.getLogger('crushinator.framework')

class InteractiveConsole(UserInterface):
    """
    Console (eg terminal, shell)-based interface that asks the user for Probe
    values in an interactive way, one at a time.
    
    Inspired by the PasteScript default UI.
    """
    
    def help(self, runner=None):
        """
        """
