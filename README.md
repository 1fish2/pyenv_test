# Test case for a `pip install` problem under pyenv virtualenv

The how-to-repro instructions and the expected error Traceback are in `setup.py`.

The `CONFIGURE_OPTS="--enable-shared"` argument is not (always?) required to reproduce the problem. I didn't test whether the problem reproduces without pyenv and virtualenv.

The key step is `pip install numpy==1.9.2 Cython`. It doesn't fail but sets up setup.py for failure unless you include the option `--no-binary :all:` or remove the numpy version specifier `==1.9.2`.

It's also possible to get through the setup.py stage and encounter a dynamic-library load error like `ImportError: dlopen(.../_line_profiler.so, 2): Symbol not found: _PyUnicodeUCS2_Compare` when running the code under kernprof or nosetests. (You must first install them via `pip install line_profiler nose; pyenv rehash`). Again, the fix is to add the `--no-binary :all:` option to `pip install`.


## License

[Public domain](https://github.com/1fish2/pyenv_test/blob/master/LICENSE.md).
