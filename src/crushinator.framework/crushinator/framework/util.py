"""
crushinator.framework.util - common utility functions
"""
import os

def listpaths(start):
    """
    Starting at a root directory, return a list of absolute paths for 
    all files in that directory and all of its subdirectories.
    
    **generator**
    
    @param start: string, path to starting directory (assumed to be 
                  absolute... paths to be returned will also be relative if
                  a relative path is provided)
    """
    templates = os.walk(start)

    for dirpath, dirnames, filenames in templates:
        for name in dirnames+filenames:
            yield os.path.join(dirpath, name)
            
