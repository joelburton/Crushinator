====================================================
Crushinator: A Gode Generation Framework and Toolkit
====================================================

.. note:: This document is still in heavy flux, please consult the source,
          the issue tracker, mailing list chatter, and other resources before relying
          on the contents of this document. 
          
          This notice will be removed when the package layout has stabilized. 

Welcome
=======
This is the root of the ``Crushinator`` project, a special one-stop package
that combines the development (and installation) of several independant 
(but related) python packages:

  - ``crushinator.framework``, the core classes defining the API that all ``Crushinator``-based
    projects implment.
  - ``crushinator.toolkit``, a set of common implementations of various components covering
    many different use-cases. 
  - ``crushinator.frontends``, a set of reference implementations showing the different types 
    of front-end user interfaces. Considered production-quality code, and safe to use in lieu 
    of (or in tandem with) another preferred front-end user interface.
  - ``crushinator.runners``, complete implementations for a few code generation systems
    considered of universal appeal. Also serves as the 'proof-of-concept' implementations
    of the framework.
    
The general idea is that if you want to work on the ``Crushinator`` project, you are
encouraged to clone this entire repository, and run **all** of the tests. 

This will ensure that the 'batteries' that are included will continue to be properly 
*charged*.

Directory Structure
===================
This README is at the root of a python egg, ``Crushinator``, which provides the
``crushinator.framework`` package. 

The ``src`` directory contains the source code for ``crushinator.framework``, and the other 
packages described above. With the exception of ``crushinator.framework``, each subdirectory
within is a complete python egg file structure. 

The ``docs`` folder contains design, implementation, and userland documentation. It (like
this file) is written in reStructuredText, and is written for documentation to be generated
with ``Sphinx``. 

Installation of the main ``Crushinator`` egg in this package does **not** install the other packages,
nor does installing one of them automatically install any others (at least not the version 
you've got checked out; any dependant packages will be pulled from PyPi in the event 
they've been released). 

See `Developing Crushinator`_ for further details and instructions on using the 
included ``buildout.cfg`` (the recommended method), or a ``virtualenv`` environment.

Release Numbers Explained
=========================
The ``Crushinator`` packages are versioned incrementally, using a 3 part numeric notation (e.g., 1.2.3). There is no
anticpated limit for any of the component numbers (so 100202202.212121243123412.242345345423563456 is theoretically possible, but not likely).

All numbers start at 0.

 - The first number (**5**.1.43) indicates 'feature' or 'major' releases. This includes additional package-level functionality, API changes, etc. The 0.x.x versions are considered pre-release versions.
 - The second number (5.**1**.43) is used for smaller, but still significant, releases *within* a feature release. This number is reset to 0 when the feature release number 
   is incremented (so the next major release would be (6.0.0). API changes are **not** allowed within a 'first dot' release. New features can be added, but when they are incorporated
   is up to the release manager.
 - The third number (5.1.**43**) is strictly for defects (bugs, security flaws, documentation updates). New features are not allowed, nor are API changes. These versions can be released at will, and
   should be entirely safe for all users of the particular X.X.Y release to upgrade to. This number resets to zero when the 'first dot' number is incremented or rolled over.
   
Alphas, Betas, Release Candidates, and other specialized releases will be indicated with a dash (-) and a few characters to indicate the purpose. Some examples:

 - 0.1.0-alpha: an 'alpha', or very early release of the 0.1.0 version. As bugs are fixed within that alpha, the third number increments as in 'typical' releases.
 - 5.2.0-RC1: a 'release candidate' of the 5.2.0 version. A second release candate would be 5.2.0-RC2. 
 
With the exception of a very few situations, special releases will always be on 'full' releases, e.g., a version with no bugs (e.g. X.X.0)

A quick counting example:

.. note:: This may not reflect the actual release cycle; At this point there's no indication that a release candidate step or alphas/betas will be strictly necessary.

  - 0.1.0-alpha: initial release
  - 0.1.1-alpha: first bug found and fixed
  - 0.1.2: a bunch of bugs are fixed
  - 0.1.0: 'full' release of the alpha (skipped over beta because it had adequate test coverage, documentation and all bugs were fixed)
  - 0.2.0-alpha: new featre is added, released for developer testing
  - 0.2.0-beta: initial release to 'regular' users
  - 0.2.0: actual release
  - 1.0.0-alpha: developer work on the first feature-complete, API-stable release.
  - 1.0.0-beta: beta of that release
  - 1.0.1-beta: first batch of bugs fixed
  - 1.0.2-beta: small bug found and fixed
  - 1.0.0-RC1: initial release candidate submitted for testing and review, otherwise feature complete, full test coverage, full docs and no bugs)
  - 1.0.1-RC1: one bug was found and fixed
  - 1.0.0: 'official' release.
  
  
Developing Crushinator
======================

Using the Included Buildout
---------------------------
TODO
~~~~

Using a Virtualenv
------------------
TODO
~~~~
