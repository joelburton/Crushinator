"""
Test the basic implementation of the Skeleton class
"""

import unittest

class TestSkeleton(unittest.TestCase):
    def _templatepath(self, filename, templateset="skeleton_templates"):
        """
        Return an absolute path to one of the template files/directories
        
        @param filename: relative path of the file
        @param templateset: which template set are you using?
        """
        import os
        
        return os.path.join(os.path.dirname(__file__), 'data', templateset, filename)
    
    def _makefile(self, path):
        """
        Create an empty file
        """
        f = open(path, 'w')
        f.write('\n')
        f.close()
        
    def _makedestfile(self, *relpath):
        """
        Create an empty file inside of self._dest
        """  
        import os
        abspath = os.path.join(self._dest, *relpath)
        
        self._makefile(abspath)
        
        return abspath
        
    def _makedestdir(self, *relpath):
        """
        Create relpath inside of self._dest
        """
        import os
        
        abspath = os.path.join(self._dest, *relpath)
        
        if not os.path.exists(abspath):
            os.mkdir(abspath)
        
        return abspath
        
    def _skeleton(self, **kwargs):
        """
        Helper method to return a Skeleton object
        """
        from crushinator.framework.skeleton import Skeleton
        import os
        
        skeleton = Skeleton()
        
        skeleton.source = os.path.join(os.path.dirname(__file__), 'data', 'skeleton_templates')
        skeleton.dest = self._dest
        
        skeleton.__dict__.update(kwargs)
        
        return skeleton
    
    def setUp(self):
        import tempfile
        self._dest = tempfile.mkdtemp()
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self._dest)
    
    def test_is_template(self):
        """
        Test the is_template method
        """        
        skeleton = self._skeleton()
        
        # make a directory that looks like a template file
        tmpl_like_dir = self._makedestdir('path_tmpl')
        # a file that looks like a template
        self._makedestdir('some')
        self._makedestdir('some', 'path_tmpl')
        tmpl_file = self._makedestfile('some', 'path_tmpl', 'setup.txt_tmpl')
        
        self.assertTrue(skeleton.is_template(tmpl_file))
        self.assertFalse(skeleton.is_template(tmpl_like_dir))
    
    
    def test_render_path_default(self):
        """
        basic functionality of the render_path() method - default params
        """
        skeleton = self._skeleton(params={'name':'myname', 'foo':'bar'})
        
        result = skeleton.render_path('/my/+name+/is/+foo+/setup.py_tmpl')
        
        self.assertEqual(result, '/my/myname/is/bar/setup.py')
        
    def test_render_path_nofile(self):
        """
        Render a path that is a directory
        """
        skeleton = self._skeleton(params={'name':'myname', 'foo':'bar'})
        
        result = skeleton.render_path('/my/+name+/is/+foo+')
        
        self.assertEqual(result, '/my/myname/is/bar')
        
    def test_render_path_tmpl_in_middle(self):
        """
        Render a path where the template file indicator (_tmpl) is elsewhere
        in the path, and in multiple places.
        """
        skeleton = self._skeleton(params={'name':'myname', 'foo':'bar'})
        
        result = skeleton.render_path('/my/+name+_tmpl/is_tmpl/+foo+/__init__.py_tmpl')
        
        self.assertEqual(result, '/my/myname_tmpl/is_tmpl/bar/__init__.py')
        
        
    def test_list_templates(self):
        """
        List all of the templates in our test templates directory.
        """
        import os
        
        skeleton = self._skeleton(
            params={'bar':'myname', 'foo':'dddd', 'baz':'1234'}, 
            source=os.path.join(os.path.dirname(__file__), 'data', 'skeleton_templates'),
            dest="/not/a/real/path",
        )
        
        result = skeleton.list_templates()
        
        expected = [
            (os.path.join(skeleton.source, '+foo+'),os.path.join(skeleton.dest, '+foo+')),
            (os.path.join(skeleton.source, 'setup.py_tmpl'),os.path.join(skeleton.dest, 'setup.py_tmpl')),
            (os.path.join(skeleton.source, '+foo+', '+baz+'),os.path.join(skeleton.dest, '+foo+', '+baz+')),
            (os.path.join(skeleton.source, '+foo+', 'doc'),os.path.join(skeleton.dest, '+foo+', 'doc')),
            (os.path.join(skeleton.source, '+foo+', 'README_+baz+.txt_tmpl'),os.path.join(skeleton.dest, '+foo+', 'README_+baz+.txt_tmpl')),
            (os.path.join(skeleton.source, '+foo+', '__init__.py'),os.path.join(skeleton.dest, '+foo+', '__init__.py')),
            (os.path.join(skeleton.source, '+foo+', '+bar+.py'),os.path.join(skeleton.dest, '+foo+', '+bar+.py')),
            (os.path.join(skeleton.source, '+foo+', 'doc', 'README.rst_tmpl'),os.path.join(skeleton.dest, '+foo+', 'doc', 'README.rst_tmpl')),
        ]
        
        self.assertEqual([x for x in result], expected)
    
    def test_render_template(self):
        """
        Test the render_template() method - typical use case
        """
        import os
        
        skeleton = self._skeleton(
            params={'bar':'myname', 'foo':'dddd', 'baz':'1234'},
        )
        
        output = skeleton.render_template(os.path.join(skeleton.source, 'setup.py_tmpl'))
        
        expected = "from someplace import dddd\n"+\
                   "\n"+\
                   "Some text here, 1234 and some more. $500.00 reward for myname"
        
        self.assertEqual(output, expected)
        
    def test_render_template_error(self):
        """
        Test the render_template() method - malformed templates
        """  
        import os
        
        skeleton = self._skeleton(
            params={'bar':'myname', 'foo':'dddd', 'baz':'1234'}, 
            source=os.path.join(os.path.dirname(__file__), 'data', 'malformed_templates'),
        )
        
        self.assertRaises(KeyError, skeleton.render_template, (os.path.join(skeleton.source, 'unknown_value.tmpl')))
        
        self.assertRaises(ValueError, skeleton.render_template, (os.path.join(skeleton.source, 'bad_syntax.tmpl')))
        
        
    def test_render_template_not_found(self):
        """
        Test the render_template() method - template file can not be opened.
        """
        import os
        
        skeleton = self._skeleton(
            params={'bar':'myname', 'foo':'dddd', 'baz':'1234'}, 
        )
        
        self.assertRaises(IOError, skeleton.render_template, (os.path.join(skeleton.source, 'not_a_real_file')))
    
    def test_create_dest_dir_typical(self):
        """
        Create a destination directory - typical successfull creation
        """
        import os
        
        skeleton = self._skeleton()
        
        testdir = os.path.join(self._dest, 'mydir')
        
        skeleton.create_dest_dir(testdir)
        
        self.assertTrue(os.path.exists(testdir) and os.path.isdir(testdir))
        
    def test_create_dest_dir_nested(self):
        """
        Create a destination directory - nested path
        """
        import os
        
        skeleton = self._skeleton()
        
        testdir = os.path.join(skeleton.dest, 'mydir', 'mysubdir', 'mysubsubdir')
        
        skeleton.create_dest_dir(testdir)
        
        self.assertTrue(os.path.exists(testdir) and os.path.isdir(testdir))
        
    def test_create_dest_dir_existing(self):
        """
        Create a destination directory - file exists at that path
        """
        import os
        
        skeleton = self._skeleton()
        
        testdir = os.path.join(skeleton.dest, 'mydir')
        
        self._makefile(testdir)
        
        skeleton.create_dest_dir(testdir)
        
        # returns True when the dest dir is created successfully
        self.assertFalse(skeleton.create_dest_dir(testdir))
        
    def test_create_dest_dir_existing(self):
        """
        Create a destination directory - directory exists at that path
        """
        import os
        
        skeleton = self._skeleton()
        
        testdir = os.path.join(self._dest, 'mydir')
        
        os.mkdir(testdir)
        
        skeleton.create_dest_dir(testdir)
        
        # returns True when the dest dir is created successfully
        self.assertFalse(skeleton.create_dest_dir(testdir))
    
    def test_create_dest_dir_dryrun(self):
        """
        Create a destination directory - dry run mode
        """
        import os
        
        skeleton = self._skeleton(dryrun=True)
        
        testdir = os.path.join(skeleton.dest, 'mydir')
        
        # returns True when the dest dir is created successfully
        self.assertFalse(skeleton.create_dest_dir(testdir))
    
    def test_write_dest_file_template(self):
        """
        Write a destination file based on a template
        """
        import os
        
        skeleton = self._skeleton(
            params={'bar':'myname', 'foo':'dddd', 'baz':'1234'}, 
        )
        
        source = self._templatepath('setup.py_tmpl')
        dest = skeleton.destpath(source)
        
        target = skeleton.render_path(dest)
        
        self._makedestdir(os.path.dirname(target))
        
        skeleton.write_dest_file(source, target)
        
        self.assertTrue(os.path.exists(target))
        
    def test_write_dest_file_nontemplate(self):
        """
        Write a destination file based on a non-template file
        """
        import os
        
        skeleton = self._skeleton(
            params={'bar':'myname', 'foo':'dddd', 'baz':'1234'}, 
        )
        
        source = self._templatepath('+foo+/__init__.py')
       
        dest = skeleton.destpath(source)
        
        target = skeleton.render_path(dest)
        self._makedestdir(os.path.dirname(target))
             
        skeleton.write_dest_file(source, target)
        
        self.assertTrue(os.path.exists(target))
    
    def test_write_dest_file_template_dryrun(self):
        """
        Make sure the file is not ever created in DRYRUN mode
        """
        import os
        
        skeleton = self._skeleton(
            params={'bar':'myname', 'foo':'dddd', 'baz':'1234'},
            dryrun=True,
        )
        
        source = self._templatepath('+foo+/__init__.py')
       
        dest = skeleton.destpath(source)
        
        target = skeleton.render_path(dest)
        self._makedestdir(os.path.dirname(target))
             
        skeleton.write_dest_file(source, target)
        
        self.assertFalse(os.path.exists(target))
        
    def test_write_dest_file_template_dryrun(self):
        """
        Make sure the file is not ever created in DRYRUN mode
        """
        import os
        
        skeleton = self._skeleton(
            params={'bar':'myname', 'foo':'dddd', 'baz':'1234'},
            dryrun=True,
        )
        
        source = self._templatepath('setup.py_tmpl')
        dest = skeleton.destpath(source)
        
        target = skeleton.render_path(dest)
        
        self._makedestdir(os.path.dirname(target))
        
        skeleton.write_dest_file(source, target)
        
        self.assertFalse(os.path.exists(target))
    
    def test_process_typical(self):
        """
        Test a typical run of the process() method.
        """
        import os
        
        skeleton = self._skeleton(
            params={'bar':'myname', 'foo':'dddd', 'baz':'1234'}, 
        )
        
        result = []
        
        for source, dest in skeleton:
            result.append((source, dest))
        
        # necessary for list_templates() to return anything
        skeleton.reset()
        
        self.assertEqual(len(result), len([x for x in skeleton.list_templates()]))
        
    def test_process_error(self):
        """
        Test running process when a file exists.
        """
        import os
        from crushinator.framework.exceptions import SkeletonFileExists
        
        skeleton = self._skeleton(
            params={'bar':'myname', 'foo':'dddd', 'baz':'1234'}, 
        )
        
        self._makedestfile('setup.py')
        
        try:
            for source, dest in skeleton:
                pass
        except SkeletonFileExists:
            pass
        else:
            self.fail("SkeletonFileExists not raised")
            
    def test_process_retry(self):
        """
        Test retrying with overwright
        """
        import os
        from crushinator.framework.exceptions import SkeletonFileExists
        
        skeleton = self._skeleton(
            params={'bar':'myname', 'foo':'dddd', 'baz':'1234'}, 
        )
        
        self._makedestfile('setup.py')
        processed = []
        
        while 1:
            try:
                for source, dest in skeleton:
                    processed.append((source, dest))
                
                break
            except SkeletonFileExists:
                processed.append(skeleton.retry(overwrite=True))
        
        skeleton.reset()
        
        self.assertEqual(len(processed), len([x for x in skeleton.list_templates()]))
        
        
