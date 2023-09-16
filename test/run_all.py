import unittest
import os

loader = unittest.TestLoader()
suite = loader.discover(start_dir = os.getcwd(), pattern='*_tests.py')
runner = unittest.TextTestRunner()
runner.run(suite)
