"""
Tests for the Collector base implementation.
"""

import unittest

class TestCollector(unittest.TestCase):
    """
    Basic tests for the Collector
    """  
    def setUp(self):
        import tempfile, os
        self.working = tempfile.mkdtemp()
        self.current = os.getcwd()
        
        os.chdir(self.working)
        
    def tearDown(self):
        import shutil, os
        os.chdir(self.current)
        shutil.rmtree(self.working)
    
    def _write_simple_config(self, path):
        """
        Create a simple, well-formed config file
        """
        config = open(path, 'w')
        print >>config, "[crushinator.framework.testsection]"
        print >>config, "username = jj"
        print >>config, "license = GPL"
        config.close()
    
    def test_loadFromHomeDirectory(self):
        """
        Attempt to load and parse a well formed config file from ~/.crushinator
        """
        import os
        from crushinator.framework import Collector
        
        os.environ['HOME'] = self.working
        
        self._write_simple_config(os.path.join(self.working, '.crushinator'))
        
        collector = Collector()
        
        result = collector._load_home_params('crushinator.framework.testsection')
        
        self.assertEquals(result['license'], 'GPL')
        
    def test_loadFromCurrentDirectory(self):
        """
        Attempt to load and parse a well formed config file from $CWD/.crushinator
        """
        import os
        from crushinator.framework import Collector
        
        self._write_simple_config(os.path.join(self.working, '.crushinator'))
        
        collector = Collector()
        
        result = collector._load_cwd_params('crushinator.framework.testsection')
        
        self.assertEquals(result['license'], 'GPL')
        
    def test_loadFromCurrentDirectory(self):
        """
        Attempt to load and parse a well formed config file from the --config 
        command-line arguement
        """
        import os, sys
        from crushinator.framework import Collector
        
        path = os.path.join(self.working, 'test.cfg')
        self._write_simple_config(path)
        
        collector = Collector()
        
        sys.argv = ['--config',  path,]
        
        result = collector._load_commandline_file_params('crushinator.framework.testsection')
        
        self.assertEquals(result['license'], 'GPL')
        
    def test_loadValuesFromARGV(self):
        """
        Set values as name=vaule pairs on the command line
        """
        import os, sys
        from crushinator.framework import Collector
        
        collector = Collector()
        
        sys.argv = ['license=BSD',  'author=jj']
        
        result = collector._load_argv_pairs()
        
        self.assertEquals(result['license'], 'BSD')

        
class TestCollectorFunctional(unittest.TestCase):
    """
    Basic functional tests for the Collector
    """  
    def setUp(self):
        import tempfile, os
        self.working = tempfile.mkdtemp()
        self.home = tempfile.mkdtemp()
        
        self.homefile = os.path.join(self.home, '.crushinator')
        self.cwdfile = os.path.join(self.working, '.crushinator')
        self.clifile = os.path.join(self.working, 'config.cfg')
        
        self.current = os.getcwd()
        os.chdir(self.working)
        
    def tearDown(self):
        import shutil, os
        os.chdir(self.current)
        shutil.rmtree(self.working)     
        
    def _home_file(self):
        config = open(self.homefile, 'w')
        print >>config, "[global]"
        print >>config, "username = jj"
        print >>config, "email = jj@someserver.com"
        print >>config, "license = GPL"
        print >>config, "homefile = Value1"
        print >>config
        print >>config, "[my.bsdapp]"
        print >>config, "license = BSD"
        print >>config, "from = homefile"
        config.close()
        
    def _cwd_file(self):
        config = open(self.cwdfile, 'w')
        print >>config, "[global]"
        print >>config, "username = cwdjj"
        print >>config, "email = cwdjj@someserver.com"
        print >>config, "license = GPL"
        print >>config, "cwdfile = Value2"
        print >>config
        print >>config, "[crushinator.framework.testsection]"
        print >>config, "username = jdj"
        print >>config
        print >>config, "[my.bsdapp]"
        print >>config, "license = BSD"
        print >>config, "from = cwdfile"
        config.close()
        
    def _cli_file(self):
        config = open(self.clifile, 'w')
        print >>config, "[global]"
        print >>config, "clifile = Value3"
        print >>config        
        print >>config, "[crushinator.framework.testsection]"
        print >>config, "username = jdj"
        print >>config
        print >>config, "[my.bsdapp]"
        print >>config, "license = BSD"
        print >>config, "from = clifile"
        config.close()
        
        
    def test_globals_basic(self):
        """
        The 'global' section should set values when they are otherwise not 
        specified.
        """
        from crushinator.framework import Collector
        import os, sys
        
        os.environ['HOME'] = self.home
        sys.argv = ['--config', self.clifile, 'command1=value3']
        
        
        self._home_file()
        self._cwd_file()
        self._cli_file()
        
        collector = Collector()
        
        result = collector()
        
        self.assertEquals(result['homefile'], 'Value1')
        self.assertEquals(result['clifile'], 'Value3')
        self.assertEquals(result['cwdfile'], 'Value2')
        
        
    def test_globals_basic(self):
        """
        The 'global' section should be overridden by other sections.
        """
        from crushinator.framework import Collector
        import os, sys
        
        os.environ['HOME'] = self.home
        sys.argv = ['--config', self.clifile, 'command1=value3']
        
        
        self._home_file()
        self._cwd_file()
        self._cli_file()
        
        collector = Collector()
        
        result = collector('my.bsdapp')
        
        self.assertEquals(result['license'], 'BSD')
        
        
    def test_cwd_override(self):
        """
        Values from the .crushinator file in the current working directory
        should override the ones in file in the users home directory.
        """
        from crushinator.framework import Collector
        import os, sys
        
        os.environ['HOME'] = self.home
        
        self._home_file()
        self._cwd_file()
        
        collector = Collector()
        
        result = collector('my.bsdapp')
        
        self.assertEquals(result['from'], 'cwdfile')
        
    def test_cli_home_override(self):
        """
        Values from the .crushinator file specified on the command line overrides
        the .crushinator file in the users home directory
        """
        from crushinator.framework import Collector
        import os, sys
        
        os.environ['HOME'] = self.home
        sys.argv = ['--config', self.clifile, 'command1=value3']
        
        
        self._home_file()
        self._cli_file()
        
        collector = Collector()
        
        result = collector('my.bsdapp')
        
        self.assertEquals(result['from'], 'clifile')
        
        
    def test_cli_cwd_override(self):
        """
        Values from the .crushinator file specified on the command line overrides
        the .crushinator file in the current working directory
        """
        from crushinator.framework import Collector
        import os, sys
        
        os.environ['HOME'] = self.home
        sys.argv = ['--config', self.clifile, 'command1=value3']
        
        
        self._cwd_file()
        self._cli_file()
        
        collector = Collector()
        
        result = collector('my.bsdapp')
        
        self.assertEquals(result['from'], 'clifile')
    
    def test_all_overrides(self):
        """
        Make sure that all values to be overridden values are overriden.
        """
        from crushinator.framework import Collector
        import os, sys
        
        os.environ['HOME'] = self.home
        sys.argv = ['--config', self.clifile, 'from=argv']
        
        
        self._home_file()
        self._cwd_file()
        self._cli_file()
        
        collector = Collector()
        
        result = collector('my.bsdapp')
        
        self.assertEquals(result['from'], 'argv')
        self.assertEquals(result['homefile'], 'Value1')
        self.assertEquals(result['clifile'], 'Value3')
        self.assertEquals(result['cwdfile'], 'Value2')
        
        
        
        
        
        
        
        
        
        
        
        
        
