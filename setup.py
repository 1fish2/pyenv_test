"""
Test case for a `pip install` problem under pyenv virtualenv.

0. Background, if not already done on this computer:
    brew install pyenv
    brew install pyenv-virtualenv
    brew install pyenv-virtualenvwrapper

1. Create a Python virtualenv:
    CONFIGURE_OPTS="--enable-shared" pyenv install 2.7.10   # Install Python 2.7.10
    pyenv local 2.7.10        # Use 2.7.10 in the local directory
    pip install --upgrade pip setuptools
    pyenv rehash
    pyenv virtualenv sum      # Create the "sum" virtual environment using 2.7.10 as its base
    pyenv local sum           # Use the "sum" virtual environment in the local directory
    pip install --no-binary :all: numpy==1.9.2 Cython   # Problematic w/o "--no-binary :all:"
    pyenv rehash

2. Build the Cython code:
    rm -f sum.so sum.c; python setup.py build_ext --inplace

3. If you get this far, run the test case:
    python test_pip.py

4. Try installing nose or line_profiler, rehashing, and running the test
under the installed executable nosetest or kernprof.
"""

from distutils.core import setup
from Cython.Build import cythonize
import numpy as np

sum_module = cythonize("sum.pyx")
setup(name="Sum", ext_modules=sum_module, include_dirs=[np.get_include()])


"""
--- Step 2 may fail: ---

Traceback (most recent call last):
  File "setup.py", line 31, in <module>
    import numpy as np
  File "/usr/local/var/pyenv/versions/sum/lib/python2.7/site-packages/numpy/__init__.py", line 170, in <module>
    from . import add_newdocs
  File "/usr/local/var/pyenv/versions/sum/lib/python2.7/site-packages/numpy/add_newdocs.py", line 13, in <module>
    from numpy.lib import add_newdoc
  File "/usr/local/var/pyenv/versions/sum/lib/python2.7/site-packages/numpy/lib/__init__.py", line 8, in <module>
    from .type_check import *
  File "/usr/local/var/pyenv/versions/sum/lib/python2.7/site-packages/numpy/lib/type_check.py", line 11, in <module>
    import numpy.core.numeric as _nx
  File "/usr/local/var/pyenv/versions/sum/lib/python2.7/site-packages/numpy/core/__init__.py", line 6, in <module>
    from . import multiarray
ImportError: dlopen(/usr/local/var/pyenv/versions/sum/lib/python2.7/site-packages/numpy/core/multiarray.so, 2): Symbol not found: _PyUnicodeUCS2_AsASCIIString
  Referenced from: /usr/local/var/pyenv/versions/sum/lib/python2.7/site-packages/numpy/core/multiarray.so
  Expected in: flat namespace
 in /usr/local/var/pyenv/versions/sum/lib/python2.7/site-packages/numpy/core/multiarray.so

"""
