"""
TestEnv.py -- Test case for pyenv, pyenv virtualenv, Cythonize.
"""

import unittest
import numpy as np
from sum import sum

class TestEnv(unittest.TestCase):

    def test_case(self):
        a = np.arange(5)
        tot = sum(a)
        self.assertEqual(tot, 10)

if __name__ == '__main__':
    unittest.main()
