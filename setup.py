"""
Test case for a `pip install` problem.
"""

from distutils.core import setup
from Cython.Build import cythonize
import numpy as np

sum_module = cythonize("sum.pyx")
setup(name="Sum", ext_modules=sum_module, include_dirs=[np.get_include()])


"""
STEPS TO REPRODUCE ON MAC OS X

0. Background, if not already done on this computer:
    brew install pyenv
    brew install pyenv-virtualenv
    brew install pyenv-virtualenvwrapper

1. Install Python 2.7.12 into a virtualenv:
    pyenv install 2.7.12      # Install Python. Optional: Prefix it with CONFIGURE_OPTS="--enable-shared"
    pyenv local 2.7.12        # Use this version in the local directory
    pip install --upgrade pip setuptools
    pyenv rehash
    #pyenv virtualenv sum     # Optional: Create a virtual environment "sum" so it's quicker to start over
    #pyenv local sum          # Optional: Use the virtual environment in the local directory
    pip install numpy==1.9.2 Cython   # Problematic! Ditto numpy 1.9.3 or 1.10.4
    pyenv rehash

2. Try to import numpy:
    python -c "import numpy"

This should produce the traceback, below.

3. Try to build the Cython code sum.pyx:
    rm -f *.so *.pyc sum.c; python setup.py build_ext --inplace

This should produce the traceback, below.

4. Reinstall numpy (1.9.2, 1.9.3, or 1.10.4) and Cython from source:
    pip uninstall numpy Cython    # or delete and recreate the virtualenv
    pip install --no-binary :all: numpy==1.9.2 Cython
    pyenv rehash

Then build and run the test case:
    rm -f *.so *.pyc sum.c; python setup.py build_ext --inplace
    python test_pip.py

This should succeed (with the usual noisy warnings from Cythonize).

5. Reinstall numpy using version 1.11 from binary:
    pip uninstall numpy Cython    # or delete and recreate the virtualenv
    pip install numpy==1.11.2 Cython
    pyenv rehash

Then build and run the test case:
    rm -f *.so *.pyc sum.c; python setup.py build_ext --inplace
    python test_pip.py

This should succeed.

6. Either way (after step 4 or 5) running the test under kernprof fails:
    pip install line_profiler
    pyenv rehash
    kernprof -lv test_pip.py

This should produce the traceback, below.

Again, the fix is to reinstall line_profiler like this:
    pip uninstall line_profiler
    pip install "--no-binary :all:" line_profiler
    pyenv rehash


--- Step 2 Traceback: ---

Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/usr/local/var/pyenv/versions/sum/lib/python2.7/site-packages/numpy/__init__.py", line 180, in <module>
    from . import add_newdocs
  File "/usr/local/var/pyenv/versions/sum/lib/python2.7/site-packages/numpy/add_newdocs.py", line 13, in <module>
    from numpy.lib import add_newdoc
  File "/usr/local/var/pyenv/versions/sum/lib/python2.7/site-packages/numpy/lib/__init__.py", line 8, in <module>
    from .type_check import *
  File "/usr/local/var/pyenv/versions/sum/lib/python2.7/site-packages/numpy/lib/type_check.py", line 11, in <module>
    import numpy.core.numeric as _nx
  File "/usr/local/var/pyenv/versions/sum/lib/python2.7/site-packages/numpy/core/__init__.py", line 14, in <module>
    from . import multiarray
ImportError: dlopen(/usr/local/var/pyenv/versions/sum/lib/python2.7/site-packages/numpy/core/multiarray.so, 2): Symbol not found: _PyUnicodeUCS2_AsASCIIString
  Referenced from: /usr/local/var/pyenv/versions/sum/lib/python2.7/site-packages/numpy/core/multiarray.so
  Expected in: flat namespace
 in /usr/local/var/pyenv/versions/sum/lib/python2.7/site-packages/numpy/core/multiarray.so


--- Step 3 Traceback: ---

Traceback (most recent call last):
  File "setup.py", line 7, in <module>
    import numpy as np
  File "/usr/local/var/pyenv/versions/2.7.12/lib/python2.7/site-packages/numpy/__init__.py", line 170, in <module>
    from . import add_newdocs
  File "/usr/local/var/pyenv/versions/2.7.12/lib/python2.7/site-packages/numpy/add_newdocs.py", line 13, in <module>
    from numpy.lib import add_newdoc
  File "/usr/local/var/pyenv/versions/2.7.12/lib/python2.7/site-packages/numpy/lib/__init__.py", line 8, in <module>
    from .type_check import *
  File "/usr/local/var/pyenv/versions/2.7.12/lib/python2.7/site-packages/numpy/lib/type_check.py", line 11, in <module>
    import numpy.core.numeric as _nx
  File "/usr/local/var/pyenv/versions/2.7.12/lib/python2.7/site-packages/numpy/core/__init__.py", line 6, in <module>
    from . import multiarray
ImportError: dlopen(/usr/local/var/pyenv/versions/2.7.12/lib/python2.7/site-packages/numpy/core/multiarray.so, 2): Symbol not found: _PyUnicodeUCS2_AsASCIIString
  Referenced from: /usr/local/var/pyenv/versions/2.7.12/lib/python2.7/site-packages/numpy/core/multiarray.so
  Expected in: flat namespace
 in /usr/local/var/pyenv/versions/2.7.12/lib/python2.7/site-packages/numpy/core/multiarray.so


--- Step 6 Traceback: ---

Traceback (most recent call last):
  File "/usr/local/var/pyenv/versions/2.7.12/bin/kernprof", line 11, in <module>
    sys.exit(main())
  File "/usr/local/var/pyenv/versions/2.7.12/lib/python2.7/site-packages/kernprof.py", line 198, in main
    import line_profiler
  File "/usr/local/var/pyenv/versions/2.7.12/lib/python2.7/site-packages/line_profiler.py", line 25, in <module>
    from _line_profiler import LineProfiler as CLineProfiler
ImportError: dlopen(/usr/local/var/pyenv/versions/2.7.12/lib/python2.7/site-packages/_line_profiler.so, 2): Symbol not found: _PyUnicodeUCS2_Compare
  Referenced from: /usr/local/var/pyenv/versions/2.7.12/lib/python2.7/site-packages/_line_profiler.so
  Expected in: flat namespace
 in /usr/local/var/pyenv/versions/2.7.12/lib/python2.7/site-packages/_line_profiler.so

"""
