SPICE4MERTIS
============

SPICE4MERTIS is a command-line or Python package tool aimed to support
BepiColombo MERTIS science operations and data analysis.

SPICE is an essential tool for scientists and engineers alike in the 
planetary science field for Solar System Geometry. Please visit the NAIF 
website for more details about SPICE.
 

Function and Purpose
--------------------

Indicating a BepiColombo MERTIS sensor and given a CCD coordinate and a time interval SPICE4MERTIS generates a table with the following parameters:

- Time in UTC
- Ephemeris time in seconds
- CCD pixel line number
- CCD pixel column number
- Planetocentric longitude of pixel boresight intersection with target in degrees
- Planetocentric latitude of pixel boresight intersection with target in degrees
- Planetocentric longitude of sub-spacecraft point on target in degrees
- Planetocentric latitude of sub-spacecraft point on target in degrees
- Planetocentric longitude of sub-solar point on target in degrees
- Planetocentric latitude of sub-solar point on target in degrees
- Observer-target distance at boresight intersection with target in kilometers
- Target angular diameter in degrees
- Local Solar Time at the pixel boresight intersection
- Phase angle at the pixel boresight intersection in degrees
- Emission angle at the pixel boresight intersection in degrees
- Incidence angle at the pixel boresight intersection in degrees


Environmental Considerations
----------------------------

SPICE4MERTIS is a Python 3.5.x package that uses a set of standard Python libraries.

Installation
------------

Download this repository and then run ``pip install -e .`` 
SPICE4MERTIS requires the BepiColombo SPICE Kernel Dataset and a working meta-kernel.


Usage
-----

Run spice4mertis -h to learn how to use it.


Known Working Environments:
---------------------------

SPICE4MERTIS is compatible with modern 64 bits versions of Linux and Mac.
If you run into issues with your system please submit an issue with details. 

- OS: OS X, Linux
- CPU: 64bit
- Python 3.5
