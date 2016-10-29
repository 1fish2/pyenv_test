# Test case for a `pip install` problem under pyenv virtualenv

The how-to-repro instructions and the expected error Traceback are in `setup.py`.

The `CONFIGURE_OPTS="--enable-shared"` argument is not (always?) required to reproduce the problem.

The key step is `pip install numpy==1.9.2 Cython`. It doesn't fail but sets up setup.py for failure unless you include the option `--no-binary :all:` or remove the numpy version specifier `==1.9.2`.

It's also possible to get through the setup.py stage and encounter the error `ImportError: dlopen(.../_line_profiler.so, 2): Symbol not found: _PyUnicodeUCS2_Compare` when running the code under kernprof. (You must first install it via `pip install line_profiler; pyenv rehash`).


## License

[MIT License](https://github.com/1fish2/BBQTimer/blob/master/LICENSE.md).
