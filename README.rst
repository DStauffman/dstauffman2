###########
dstauffman2
###########

The "dstauffman2" module is a collection of games, applications, extended utilities and miscellaneous documentation that I (David C. Stauffer) have found useful.

Written by David C. Stauffer in March 2015.
Separated into a separate module by David C. Stauffer in November 2016.

********************
Library dependencies
********************

Many parts of this code rely on the "dstauffman" module.  That library has a bunch of dependencies and tends to push the leading edge of Python development.  However, I'll list only the additional dependencies used directly within this library.

Built-in libraries
******************

The following built-in Python libraries are used within the dstauffman2 library.

* collections
* copy
* datetime
* doctest
* enum
* getpass
* glob
* inspect
* logging
* math
* nose
* os
* pickle
* random
* shutil
* sys
* timeit
* unittest

Additional libraries
********************

The following non-standard, but for the most part very well known libraries, are also used by the dstauffman2 library.

* matplotlib
* mpl_toolkits
* numpy
* pandas
* PIL
* PyQt5
* pprofile

Additional libraries only used if trying to compile to C with Cython
********************************************************************
* pyximport
* distutils.core
* Cython.Build

Troubleshooting
***************
If you have trouble installing this library, first make sure that you have the dstauffman one up and running.
