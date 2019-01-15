import os
import unittest
from unittest.mock import patch
from fsyncer import fsyncer


class TestFsyncer(unittest.TestCase):
    @patch('fsyncer.fsyncer.Github')
    def test_no_config_file(self, mock_hub):
        os.environ['SYNC_GITHUB_TOKEN'] = 'dummy token'
        fsyncer.get_repo_list()
        mock_hub.github.Github.get_user.assert_called()


if __name__ == '__main__':
    unittest.main()
