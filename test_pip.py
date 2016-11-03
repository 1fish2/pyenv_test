"""
test_pip.py -- Test case for a `pip install` problem.
"""

import unittest
import numpy as np
from sum import sum

class TestPip(unittest.TestCase):

    def test_case(self):
        a = np.arange(5)
        tot = sum(a)
        self.assertEqual(tot, 10)

if __name__ == '__main__':
    unittest.main()
