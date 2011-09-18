"""
collector.py  - Base classes for collecting default values from common locations.
"""
import ConfigParser
import os, sys, types
import argparse
from crushinator.framework.runner import Runner

import logging
logger = logging.getLogger('crushinator.framework')

class BaseCollector(object):
    """
    Base class to define method signatures. Separated from Collector due to 
    implementation code.
    """
    
    def __init__(self, **kwargs):
        """
        Any run-time, out-of-band defaults, or overrides can be specified in the
        constructor.
        
        @param kwargs: all keyword arguments passed will be added as final global
                       values
        """

    def __call__(runner=None):
        """
        Returns a dictionary of values for a specific Runner class; ignores
        runner-class sections if caller is not specified.
        
        @param runner: string, class object, or Runner instance.
        """


class Collector(BaseCollector):
    """
    Typical, base implemetation for a Crushinator Collector. 
    
    Looks in the following locations for values:
        - $HOME/.crushinator, a file.
        - $CWD/.crushinator, a file.
        - --config command-line option specifying a file path.
        - $ARGV, name=value after any other commands are processed.
        - keyword arguments passed to the Collector.__init__() method.
        
    The file structure is like this:
    
    .. 
    
        [global]
        user = jj
        email = something@somewhere.net
        licence = BSD
        
        [crushinator.toolkit.PythonEgg]
        licence = GPL
        
    Each section, save for *global* is named after a Runner class.
    """

    _defaults = None
    dotfile = '.crushinator'
    commandline = '--config'
    
    def __init__(self, **kwargs):
        """
        Any run-time, out-of-band defaults, or overrides.
        
        @param kwargs: all keyword arguments passed will be added as final global
                       values
        """
        self._defaults = kwargs

    def _load_params(self, filepath, section=None):
        """
        Given a path, if it exists, read it, and return a dictionary of the
        values within a given section (defaults to the global section).
        
        If the file path does not exist, it is silently ignored.
        
        @return: dict, values from the file, merged with the ones from the global
                 section
        
        @param fielpath: string, path to a ConfigParser-compatible file.
        @param section: string, section to grab. Defaults to 'global'
        
        @todo: should this raise an error if the file is not found?
        @todo: produce better errors if ConfigParser gets a bad or unreadable file.
        """
        
        global_values = {}
        section_values = {}
        
        if os.path.isfile(filepath):
            config = ConfigParser.SafeConfigParser()
            config.read(filepath)
            
            try:
                global_values = dict(config.items('global'))
            except ConfigParser.NoSectionError:
                logger.debug("crushinator.framework.collector.Collector: Global section was not found")
            try:
                if section:
                    section_values = dict(config.items(section))
            except ConfigParser.NoSectionError:
                logger.debug("crushinator.framework.collector.Collector: Section '%s' was not found" % (section))
        else:
            logger.warn("crushinator.framework.collector.Collector: file %s was not found" % (filepath))
        
        value = section_values
        value.update(global_values)
        
        return value
    
    def _load_home_params(self, section=None):
        """
        Loads the ``.crushinator`` file from the users $HOME directory.
        """
        path = os.path.join(os.path.expanduser("~"), self.dotfile)
        
        return self._load_params(path, section)

        
    def _load_cwd_params(self, section=None):
        """
        Loads the ``.crushinator`` file from the current working directory.
        """
        
        path = os.path.join(os.getcwd(), self.dotfile)
        
        return self._load_params(path, section)   
    
    def _load_commandline_file_params(self, section=None):
        """
        Loads a configparser file specified as a command line option.
        """
        path = None
        
        try:
            index = sys.argv.index(self.commandline)
            path = sys.argv[index+1]
        except ValueError:
            logger.debug("crushinator.framework.collector.Collector: %s option not specified on the command line" % (self.commandline))
        except KeyError:
            logger.debug("crushinator.framework.collector.Collector: %s option specified on the command line, but no followup argument exists in sys.argv" % (self.commandline))
            
        if path:
            return self._load_params(path, section)
        else:
            logger.debug("crushinator.framework.collector.Collector: %s option not specified on the command line" % (self.commandline))
            return {}
        
        
    def _load_argv_pairs(self):
        """
        Grabs name=value pairs out of the command line arguments
        """
        opts = sys.argv
        
        values = {}
        
        for opt in opts:
            if '=' in opt:
                key, val = opt.split('=', 1)
                values[key] = val
                
        return values
        
    def __call__(self, runner=None):
        section = None
        
        if runner:
            if isinstance(runner, types.StringTypes):
                section = runner
            elif issubclass(runner.__class__, Runner):
                section = runner.__class__.__name__
            elif isinstance(runner, types.ClassType):
                section = runner.__name__
            else:
                raise ValueError, "runner parameter, if specified, must be a Runner object, a class object, or a string"
        
        values = {}
        from_home = self._load_home_params(section)
        
        from_cwd = self._load_cwd_params(section)

        from_cli_file = self._load_commandline_file_params(section)
        
        from_argv = self._load_argv_pairs()
        
        values.update(from_home)
        values.update(from_cwd)
        values.update(from_cli_file)
        values.update(from_argv)
        
        return values
                
         
        
