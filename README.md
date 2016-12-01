# Test case for a `pip install` problem (now fixed)

The key steps are

    pyenv local 2.7.12          # pyenv-install Python 2.7.*
    pip install numpy==1.9.2    # pip-install numpy 1.9 or 1.10
    python -c "import numpy"    # try to load numpy

`pip install` completes normally but sets up "import numpy" for failure unless you either included the install option `--no-binary :all:` or let pip default to numpy version 1.11.

Similarly,

    pip install line_profiler

will install a broken kernprof unless you use the pip install option `--no-binary :all:`.

_The problem only happens with a Python installed by pyenv._


## Steps to reproduce on Mac OS X 10.11.6 El Capitan

1. Preparation, if not already done on this computer:

        brew install pyenv
        brew install pyenv-virtualenv
        brew install pyenv-virtualenvwrapper

    This installs pyenv 1.0.4, pyenv-virtualenv 1.0.0, and pyenv-virtualenvwrapper 20140609.

    See `brew info pyenv`, `brew info pyenv-virtualenv`, and maybe [pyenv#homebrew-on-mac-os-x](https://github.com/yyuu/pyenv#homebrew-on-mac-os-x) for more steps on installing pyenv, in short, put:
        export PYENV_ROOT=/usr/local/var/pyenv
        if which pyenv-virtualenv-init > /dev/null; then eval "$(pyenv virtualenv-init -)"; fi
    into your `.profile` file and either run it manually or restart the shell.

2. Install Python 2.7.12 and numpy into a virtualenv:

        cd pyenv_test
        pyenv install 2.7.12      # Install Python. Optional: Prefix it with CONFIGURE_OPTS="--enable-shared"
        pyenv local 2.7.12        # Use this version in the local directory
        pip install --upgrade pip setuptools
        pyenv rehash
        #pyenv virtualenv sum; pyenv local sum  # Optional: Create a virtual environment "sum" (so you can delete the virtual environment and restart the experiment from here without uninstalling python) and use it in the local directory
        pip install numpy==1.10.4  # Problematic! Ditto numpy 1.9.2 or 1.9.3
        pyenv rehash

    Now

        pip list

    prints

        numpy (1.10.4)
        pip (9.0.1)
        setuptools (29.0.1)
        wheel (0.29.0)      # <-- if you created a virtualenv

    *Note:* The bug last reproduced with pip 9.0.0 and setuptools 28.7.1 but not with pip 9.0.1 and setuptools 29.0.1! Yay!

3. Try to import numpy:

        python -c "import numpy"

    This should produce the traceback, below.

4. Try to run the unit test:

        python test_pip.py

    This should produce the traceback, below.

5. Reinstall numpy (1.9.2, 1.9.3, or 1.10.4) from source:

        pip uninstall numpy     # or delete and recreate the virtualenv
        pip install --no-binary :all: numpy==1.9.2
        pyenv rehash

    Then run the test:

        python test_pip.py

    It should succeed.

6. Reinstall numpy using version 1.11 from binary:

        pip uninstall numpy     # or delete and recreate the virtualenv
        pip install numpy==1.11.2
        pyenv rehash

    Then run the test:

        python test_pip.py

    It should succeed.

7. Either way (after step 4 or 5) running the test under kernprof fails:

        pip install line_profiler
        pyenv rehash
        kernprof -lv test_pip.py

    This should produce the traceback, below.

8. Again, a fix is to reinstall line_profiler from source:

        pip uninstall line_profiler
        pip install --no-binary :all: line_profiler
        pyenv rehash
        kernprof -lv test_pip.py


### Step 3 Traceback

```
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
```

### Step 4 Traceback

```
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
```

### Step 7 Traceback

```
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
```

## License

[Public domain](https://github.com/1fish2/pyenv_test/blob/master/LICENSE.md).
