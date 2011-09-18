from setuptools import setup, find_packages
import os

version = '0.1.0'

setup(name='Crushinator',
      version=version,
      description="",
      long_description="",
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='Josh Johnson',
      author_email='lionface.lemonface@gmail.com',
      url='https://github.com/jjmojojjmojo/Crushinator/',
      license='GPL',
      packages=find_packages(),
      namespace_packages=['crushinator'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
