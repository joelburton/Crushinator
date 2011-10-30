"""
crushinator.framework.skeleton - base class for processing template skeletons.
"""
import os, shutil

from string import Template

from crushinator.framework.util import listpaths
from crushinator.framework.exceptions import SkeletonFileExists

import logging
logger = logging.getLogger('crushinator.framework')

class Skeleton(object):
    """
    A Skeleton object takes a directory of template files, a dictionary of template
    variables, and a dectination directory.
    
    When processed, the Skeleton executes the templates, uses the template values
    to replace placeholders in the file names, and places the result in
    the destination directory.
    """
    
    # destination directory
    dest = None
    
    # parameters, dictionary of template variables from the Runner
    params = None
    
    # set to True to prevent any actual files from being changed
    dryrun = False
    
    # source directory - where to pull templates from
    source = None
        
    # string format for doing path replacement
    # default is +%s+
    pathmatch = '+%s+'
    
    # string to match for identifying template files - at the end of the path
    # default matches /my/file.py_tmpl
    templatematch = '_tmpl'
    
    # list of already handled source, dest tuples
    _processed = None
    
    # the last handled source, dest tuple
    _lastpair = None
    
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        
        self._processed = []
    
    def render_template(self, template_path):
        """
        Take a single template file, and return a string containing the translated 
        contents
        
        @param template: a path to a template file
        @return: string, the contents of the file translated using the current value of self.params
        
        @note: Default implementation is less-than-ideal for the sake of keeping 
               the framework requirements to a minimum. See crushinator.toolkit for
               implementations using 3rd party template libraries.
               
        @todo: should exceptions here be caught and re-raised? Ignored?
        @todo: would it be better to abstract the template interaction into a specialized class?
        
        @see: PEP 292 http://www.python.org/dev/peps/pep-0292/ for template syntax.
        """
        template_data = open(template_path, 'rb').read()
        
        template = Template(template_data)
        
        return template.substitute(self.params)
    
    def is_template(self, path):
        """
        Given a path, returns true if it's a template file 
        
        By default this means it's not a directory, and it ends with
        self.templatematch
        """
        if os.path.isdir(path):
            return False
        
        parts = path.rpartition(self.templatematch)
        
        if parts[:2] == ('',''):
            return False
        else:
            return True
    
    def render_path(self, path):
        """
        Given a path, replace all variables. Return the result.
        
        This will do the substitution, and chop off the _tmpl bits.
        """
        translated = path
        for key, val in self.params.iteritems():
            translated = translated.replace(self.pathmatch % (key), val)
        
        template_stripped = translated.rpartition(self.templatematch)
        if template_stripped[:2] == ('',''):
            logger.debug("No template found in path %s" % (translated))
            return translated
        else:
            return template_stripped[0]
        
    def destpath(self, sourcepath):
        return os.path.join(self.dest, os.path.relpath(sourcepath, self.source))
    
    def list_templates(self):
        """
        Return a list of two-tuples, containing two strings:
        
            ('/absolute/source/path', '/absolute/dest/path')
            
        The first string is the absolute path to a given template file or
        directory in the template skeleton. 
        
        The second is an absolute path to the destination directory
        
        Note: variable substitution will happen in the process() method below -
        NOT HERE. This way errors in translation will be caught when they can
        be recovered from.
        """
        # this gets the base paths
        paths = listpaths(self.source)
        
        for s in paths:
            pair = (s, self.destpath(s))
            if pair not in self._processed:
                yield pair
            else:
                logger.debug("%s has already been processed" % (s))
    
    
    def create_dest_dir(self, dest):
        """
        Creates a destination directory. 
        
        @return: boolean, true if the file is created, false if not (note that
                 a false return value may not mean an error condition)
        """
        if os.path.exists(dest):
            logger.debug('Directory %s already exists. Skipping' % (dest))
            return False
        else:
            logger.debug('Attempting to create, recursively %s' % (dest))
            
            if self.dryrun:
                logger.warn('dryrun detected, %s not created' % (dest))
                return False
            
            os.makedirs(dest)
            if os.path.exists(dest):
                logger.debug('%s created successfully' % (dest))
                return True
            
            return False
            
         
    def _write_dest_file(self, source, dest):
        """
        Helper method for write_dest_file(). Does the actual writing of the file.
        
        Overwrites files if they exist.
        """
        if self.dryrun:
            logger.debug('DRYRUN: Skipping %s.' % (dest))
            return
        
        # if the source file ends in _tmpl, it needs to be processed.
        if self.is_template(source):
            logger.debug('Parsing %s as a template' % (source))
            logger.debug('Writing %s to %s' % (source, dest))
            destfile = open(dest, 'wb')
            destfile.write(self.render_template(dest))
            destfile.close()
        # otherwise, just copy it.
        else:
            logger.debug('%s is not a template file.' % (source))
            logger.debug('Copying %s to %s' % (source, dest))
            shutil.copyfile(source, dest)
    
    def write_dest_file(self, source, dest, overwrite=False):
        """
        Parses a template file and puts its contents into place in the
        destination directory.
        
        Respects the dryrun setting.
        
        @param source: string, path to a template
        @param dest: string, destination path
        @param overwrite: boolean, if True, will overwrite an existing file. If false, raises SkeletonFileExists.
        """
        if os.path.exists(dest):
            if overwrite:
                logger.debug('Overwriting %s.' % (dest))
                self._write_dest_file(source, dest)
            else:
                logger.debug('Overwrite is False. Raising exception for %s.' % (dest))
                raise SkeletonFileExists(dest)
        else:
             self._write_dest_file(source, dest)   
    
    def source_to_dest_path(self, source, dest, overwrite=False):
        """
        Given a source and dest path, do the right thing with it. 
        
        If source is a directory, it will be created as dest.
        
        If source is a template file, it will be processed and written to dest.
        
        If source is not a template file, it will be copied.
        
        dest will be processed through render_path()
        """
        
        dest = self.render_path(dest)
        
        if os.path.isdir(source):
            self.create_dest_dir(dest)
        elif os.path.isfile(source):
            self.write_dest_file(source, dest, overwrite)
        else:
            logger.debug("%s is neither a file or directory" % (source))
    

    
    def __iter__(self):
        for source, dest in self.list_templates():
            self._lastpair = (source, dest)
            self.source_to_dest_path(source, dest)
            self._processed.append((source, dest))
            yield (source, dest)
        
    def reset(self):
        """
        In the event that you've iterated through all of the templates and
        you want to reset the skeleton.
        """
        self._processed = []
    
    def retry(self, overwrite=True):
        """
        In the event that looping over the Skeleton has failed, and you want to
        try the last template again, optionally forcing an overwrite.
        """
        self.source_to_dest_path(*self._lastpair, overwrite=overwrite)
        
        pair = self._lastpair
        self._processed.append(pair)
        
        self._lastpair = None
        
        return pair
