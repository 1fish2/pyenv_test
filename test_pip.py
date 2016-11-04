"""
test_pip.py -- Test case for a `pip install` problem.
"""

import unittest
import numpy as np


class TestPip(unittest.TestCase):

    def test_case(self):
        a = np.arange(5)
        tot = a.sum()
        self.assertEqual(tot, 10)

if __name__ == '__main__':
    unittest.main()
