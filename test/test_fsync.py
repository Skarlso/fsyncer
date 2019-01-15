import os
import unittest
from unittest.mock import patch
from fsyncer import fsyncer


class TestFsyncer(unittest.TestCase):
    @patch('fsyncer.fsyncer.Github')
    def test_no_config_file(self, mock_hub):
        os.environ['SYNC_GITHUB_TOKEN'] = 'dummy token'
        # user = github.AuthenticatedUser
        # mock_user = unittest.mock.MagicMock()
        mock_hub.get_user.get_repos.return_value = ["weee"]
        fsyncer.get_repo_list()
        mock_hub.assert_called_with("dummy token")
        print(mock_hub.get_user.get_repos.called)
        # mock_user.get_repos.assert_called()


if __name__ == '__main__':
    unittest.main()
