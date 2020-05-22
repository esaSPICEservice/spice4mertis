#!/usr/bin/python
"""

@author: mcosta

"""
from setuptools import setup, find_packages
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))


# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


def get_version():

    with open('spice4mertis/config/version', 'r') as f:
        for line in f:
            version = line

    return version

setup(
        name='spice4mertis',

        version=get_version(),

        description='SPICE based application to support BepiColombo MERTIS',
        url="https://github.com/esaSPICEservice/spice4mertis.git",

        author='Marc Costa Sitja (ESA SPICE Service)',
        author_email='esa_spice@sciops.esa.int',

        # Classifiers
        classifiers=[
            # How mature is this project? Common values are
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Planetary Scientists, Science Operations Engineers and Developers',
            'Topic :: Git :: Planetary Science :: Geometry Computations',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
        ],

        # Keywords
        keywords=['esa', 'spice', 'naif', 'planetary', 'space', 'geometry', 'mercury', 'bepicolombo'],

        # Packages
        packages=find_packages(),

        # Include additional files into the package
        include_package_data=True,

        # Dependent packages (distributions)
        python_requires='>=3',

        # Scripts
        entry_points = {'console_scripts': ['spice4mertis=spice4mertis.command_line:main']}

      )