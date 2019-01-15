import os
import unittest
from unittest.mock import patch
from fsyncer import fsyncer


class TestFsyncer(unittest.TestCase):
    @patch('fsyncer.fsyncer.Github.get_user')
    def test_no_config_file(self, get_user):
        os.environ['SYNC_GITHUB_TOKEN'] = 'dummy token'
        # user = github.AuthenticatedUser
        mock_user = unittest.mock.MagicMock()
        mock_user.get_repos.return_value = ['weee']
        # mock_hub.get_user.get_repos.return_value = ["weee"]
        get_user.return_value = mock_user
        fsyncer.get_repo_list()
        get_user.assert_called()
        # mock_user.get_repos.assert_called()


if __name__ == '__main__':
    unittest.main()
