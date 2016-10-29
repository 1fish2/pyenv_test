"""
0. Background, if not already done on this computer:
    * Install pyenv, pyenv-virtualenv, pyenv-virtualenvwrapper

1. Create a Python virtualenv like this:
    CONFIGURE_OPTS="--enable-shared" pyenv install 2.7.10   # Install Python 2.7.10
    pyenv local 2.7.10        # Use 2.7.10 in the local directory
    pip install --upgrade pip setuptools
    pyenv virtualenv sum      # Create the "sum" virtual environment using 2.7.10 as its base
    pyenv local sum           # Use the "sum" virtual environment in the local directory
    pip install numpy==1.9.2 Cython
    pyenv rehash

2. Build the Cython code like this:
    rm -f sum.so sum.c; python setup.py build_ext --inplace

3. Then run the test case like this:
    python testenv.py
"""

from distutils.core import setup
from Cython.Build import cythonize

import numpy as np
import os

sum_module = cythonize("sum.pyx")

setup(
    name = "Sum",
    ext_modules = sum_module,
    include_dirs = [np.get_include()]
    )
