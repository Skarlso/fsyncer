import os
import unittest
from unittest.mock import patch, mock_open
from fsyncer import fsyncer


class TestFsyncer(unittest.TestCase):
    @patch('fsyncer.fsyncer.Github.get_user')
    def test_get_repo_list(self, get_user):
        os.environ['SYNC_GITHUB_TOKEN'] = 'dummy token'
        mock_repo = unittest.mock.MagicMock()
        mock_repo.fork.return_value = True
        mock_repo.owner.name = 'skarlso'

        mock_user = unittest.mock.MagicMock()
        mock_user.get_repos.return_value = [mock_repo]
        mock_user.name = 'skarlso'

        get_user.return_value = mock_user
        repos = fsyncer.get_repo_list()
        get_user.assert_called()
        self.assertEqual(1, len(repos), "len of %d did not equal 1" % len(repos))

    @patch('fsyncer.fsyncer.Path.is_file')
    @patch("builtins.open", new_callable=mock_open, read_data="test_repo")
    @patch("fsyncer.fsyncer.sync_list")
    def test_main_with_config_file(self, mock_sync_list, mock_file, mock_path):
        mock_file = ['test_repo']
        mock_path.return_value = True
        fsyncer.main()
        mock_sync_list.assert_called_with(['test_repo'])
        mock_path.assert_called()

    @patch('fsyncer.fsyncer.Path.is_file')
    @patch('fsyncer.fsyncer.call')
    @patch('fsyncer.fsyncer.get_repo_list')
    def test_main_without_config_file(self, mock_repo_list, mock_call, mock_path):
        mock_repo_list.return_value = ['no_config_test_repo']
        mock_path.return_value = False
        fsyncer.main()
        mock_call.assert_called_with(['rm', '-fr', 'no_config_test_repo'])
        mock_path.assert_called()


if __name__ == '__main__':
    unittest.main()
