import unittest
from unittest import mock
from fsyncer import fsyncer

class TestFsyncer(unittest.TestCase):
    @mock.patch('fsyncer.get_repo_list')
    def test_no_config_file(self):
        fsyncer.main()

if __name__ == '__main__':
    unittest.main()