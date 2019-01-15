import unittest
from unittest.mock import patch
from fsyncer import fsyncer


class TestFsyncer(unittest.TestCase):
    @patch('fsyncer.fsyncer.Github')
    def test_no_config_file(self, mock_hub):
        fsyncer.main()
        self.assertTrue(mock_hub.get_user.called, "get_user was not called")


if __name__ == '__main__':
    unittest.main()
