# Test case for a `pip install` problem

The steps-to-reproduce and expected error messages are in `setup.py`.

The key step is
    pip install numpy==1.9.2 Cython line_profiler nose
It completes normally but sets up setup.py and kernprof for failure unless you included the install option `--no-binary :all:` (or omitted the numpy version 1.9.2).


## License

[Public domain](https://github.com/1fish2/pyenv_test/blob/master/LICENSE.md).
