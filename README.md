# Test case for a `pip install` problem

The steps-to-reproduce and expected error messages are in `setup.py`.

The key step is
    pip install numpy==1.9.2 Cython
It completes normally but sets up setup.py for failure unless you included the install option `--no-binary :all:` (or omitted the numpy version 1.9.2).

Even then, 
    pip install line_profiler
will install a broken kernprof unless you use the pip install option `--no-binary :all:`.


## License

[Public domain](https://github.com/1fish2/pyenv_test/blob/master/LICENSE.md).
