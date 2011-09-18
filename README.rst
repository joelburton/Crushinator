====================================================
Crushinator: A Gode Generation Framework and Toolkit
====================================================

.. note:: This document is still in heavy flux, please consult the source,
          the issue tracker, mailing list chatter, and other resources before relying
          on the contents of this document. 
          
          This notice will be removed when the package layout has stabilized. 

Welcome
=======
This is the root of the ``Crushinator`` project, a special one-stop repository
that combines the development (and installation) of several independant 
(but related) python packages:

  - ``crushinator.framework``, the core classes defining the API that all ``Crushinator``-based
    projects implment.
  - ``crushinator.toolkit``, a set of common implementations of various components covering
    many different use-cases. 
  - ``Crushinator``, a set of reference implementations showing the different types 
    of front-end user interfaces. Considered production-quality code, and safe to use in lieu 
    of (or in tandem with) another preferred front-end user interface. Installs a central
    **crushinator** script if installed directly.
  - ``crushinator.integrationtests``, a special egg containing integration tests. **Not released.** 
    
.. note:: There will most likely be a few more support packages, covering more broad implementations
          of some of the components of the ``Crushinator`` package. These will be stored in separate
          python eggs. The idea is that if you want to use a particular implementation of a component, 
          but don't need the full implementation (or you want to wrap it.)
          
          A good example might be a generation system that builds Djang-based apps. There may be a big 
          savings in time if you can extract just the ``Seletons`` and extend the ``User Interfaces``,
          instead of depending on the whole ``Crushinator`` package.
    
Consider this repository a suite of packages. Each should be autonomous (save for a dependancy on
``crushinator.framework``), and can be developed and tested separately. They're brought together here,
not just to keep the author's administration headache to a minimum, keeping issues, documentation, and other
artifacts in a central place, but also to allow a logical location for broader integration tests.

Directory Structure
===================
This README lives within a zc.buildout structure, used for testing and to provide a consistent, *almost instant*
development environment.

The ``src`` directory contains the source code for ``crushinator.framework``, and the other 
packages described above. Each subdirectory within is a complete python egg file structure. 

The ``docs`` folder contains design, implementation, and userland documentation. It (like
this file) is written in reStructuredText, and is written for documentation to be generated
with ``Sphinx``.

Each egg structure in ``src`` mirrors this one in terms of documentation. There is a ``README.rst`` file explaining what the package does and quick start/installation instructions.

Each egg also contains a ``docs`` directory, containing more detailed documentation, API references, userland docs, etc.

Unit and functional tests are located in the ``tests`` directory within the module structure (e.g. ``crushinator.framework.tests``). 

See `Developing Crushinator`_ for further details and instructions on using the 
included ``buildout.cfg`` (the recommended method), or a ``virtualenv`` environment.

See `Testing Crushinator`_ for more information about writing and running tests.

See `Documenting Crushinator`_ for documentation guidelines and instructions on generating the user manual.

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

Documenting Crushinator
=======================
Documentation Guidelines
------------------------
TODO
~~~~

Generating The User Manual
--------------------------
TODO
~~~~

Testing Crushinator
===================
Running the Tests
-----------------
TODO
~~~~


