# Test case for a `pip install` problem

The key step is
    pip install numpy==1.9.2
It completes normally but sets up "import numpy" for failure unless you included the install option `--no-binary :all:` (or omitted the numpy version 1.9.2).

Even then, 
    pip install line_profiler
will install a broken kernprof unless you use the pip install option `--no-binary :all:`.


## Steps to reproduce on Mac OS X

0. Background, if not already done on this computer:
    brew install pyenv
    brew install pyenv-virtualenv
    brew install pyenv-virtualenvwrapper

1. Install Python 2.7.12 into a virtualenv:
    cd pyenv_test
    pyenv install 2.7.12      # Install Python. Optional: Prefix it with CONFIGURE_OPTS="--enable-shared"
    pyenv local 2.7.12        # Use this version in the local directory
    pip install --upgrade pip setuptools
    pyenv rehash
    #pyenv virtualenv sum; pyenv local sum  # Optional: Create a virtual environment "sum" (so it's quicker to start over) and use it in the local directory
    pip install numpy==1.9.2  # Problematic! Ditto numpy 1.9.3 or 1.10.4
    pyenv rehash

Interestingly, after `pyenv local 2.7.12`,
    pip list
prints
    pip (9.0.0)
    setuptools (28.7.1)
    virtualenv (15.0.3)

while after `pyenv virtualenv sum; pyenv local sum`,
    pip list
prints
    pip (9.0.0)
    setuptools (28.7.1)
    wheel (0.30.0a0)

2. Try to import numpy:
    python -c "import numpy"

This should produce the traceback, below.

3. Try to run the unit test:
    python test_pip.py

4. Reinstall numpy (1.9.2, 1.9.3, or 1.10.4) from source:
    pip uninstall numpy     # or delete and recreate the virtualenv
    pip install --no-binary :all: numpy==1.9.2
    pyenv rehash

Then run the test:
    python test_pip.py

It should succeed.

5. Reinstall numpy using version 1.11 from binary:
    pip uninstall numpy     # or delete and recreate the virtualenv
    pip install numpy==1.11.2
    pyenv rehash

Then run the test:
    python test_pip.py

It should succeed.

6. Either way (after step 4 or 5) running the test under kernprof fails:
    pip install line_profiler
    pyenv rehash
    kernprof -lv test_pip.py

This should produce the traceback, below.

7. Again, a fix is to reinstall line_profiler from source:
    pip uninstall line_profiler
    pip install --no-binary :all: line_profiler
    pyenv rehash
    python test_pip.py


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
  File "test_pip.py", line 6, in <module>
    import numpy as np
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


--- Step 6 Traceback: ---

Traceback (most recent call last):
  File "/usr/local/var/pyenv/versions/sum/bin/kernprof", line 11, in <module>
    sys.exit(main())
  File "/usr/local/var/pyenv/versions/2.7.12/envs/sum/lib/python2.7/site-packages/kernprof.py", line 198, in main
    import line_profiler
  File "/usr/local/var/pyenv/versions/2.7.12/envs/sum/lib/python2.7/site-packages/line_profiler.py", line 25, in <module>
    from _line_profiler import LineProfiler as CLineProfiler
ImportError: dlopen(/usr/local/var/pyenv/versions/2.7.12/envs/sum/lib/python2.7/site-packages/_line_profiler.so, 2): Symbol not found: _PyUnicodeUCS2_Compare
  Referenced from: /usr/local/var/pyenv/versions/2.7.12/envs/sum/lib/python2.7/site-packages/_line_profiler.so
  Expected in: flat namespace
 in /usr/local/var/pyenv/versions/2.7.12/envs/sum/lib/python2.7/site-packages/_line_profiler.so


## License

[Public domain](https://github.com/1fish2/pyenv_test/blob/master/LICENSE.md).
