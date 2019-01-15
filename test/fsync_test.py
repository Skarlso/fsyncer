import unittest
from unittest.mock import patch
from fsyncer import fsyncer

class TestFsyncer(unittest.TestCase):
    @patch('fsyncer.fsyncer.Github')
    def test_no_config_file(self, mockHub):
        print(mockHub)
        fsyncer.main()

if __name__ == '__main__':
    unittest.main()