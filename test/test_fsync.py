import os
import unittest
from unittest.mock import patch, mock_open, MagicMock
from fsyncer import fsyncer


class TestFsyncer(unittest.TestCase):
    @patch('fsyncer.fsyncer.Github.get_user')
    def test_get_repo_list(self, get_user):
        os.environ['SYNC_GITHUB_TOKEN'] = 'dummy token'
        mock_repo = MagicMock()
        mock_repo.fork.return_value = True
        mock_repo.owner.name = 'skarlso'

        mock_user = MagicMock()
        mock_user.get_repos.return_value = [mock_repo]
        mock_user.name = 'skarlso'

        get_user.return_value = mock_user
        repos = fsyncer.get_repo_list()
        get_user.assert_called()
        self.assertEqual(1, len(repos), "len of %d did not equal 1" % len(repos))

    @patch('fsyncer.fsyncer.Path.is_file')
    @patch("builtins.open", new_callable=mock_open, read_data="mock_repo1\n")
    @patch("fsyncer.fsyncer.sync_list")
    @patch('fsyncer.fsyncer.get_repo_list')
    def test_main_with_config_file(self, mock_repo_list, mock_sync_list, _, mock_path):
        # self.skipTest("not working on travis")
        os.environ['SYNC_GITHUB_TOKEN'] = 'dummy token'
        mock_repo1 = MagicMock()
        mock_repo1.fork.return_value = True
        mock_repo1.owner.name = 'skarlso'
        mock_repo1.name = 'mock_repo1'
        mock_repo2 = MagicMock()
        mock_repo2.fork.return_value = True
        mock_repo2.owner.name = 'skarlso'
        mock_repo2.name = 'mock_repo2'        
        mock_repo_list.return_value = [mock_repo1, mock_repo2]

        mock_path.return_value = True
        fsyncer.main()
        mock_sync_list.assert_called_with([mock_repo1])
        mock_path.assert_called()

    @patch('fsyncer.fsyncer.Path.is_file')
    @patch('fsyncer.fsyncer.run')
    @patch('fsyncer.fsyncer.get_repo_list')
    def test_main_without_config_file(self, mock_repo_list, mock_call, mock_path):
        os.environ['SYNC_GITHUB_TOKEN'] = 'dummy token'
        mock_repo = MagicMock()
        mock_repo.fork.return_value = True
        mock_repo.owner.name = 'skarlso'
        mock_repo.name = 'mock_repo'
        mock_repo_list.return_value = [mock_repo]
        mock_path.return_value = False
        fsyncer.main()
        mock_call.assert_called_with(['rm', '-fr', 'mock_repo'])
        mock_path.assert_called()


if __name__ == '__main__':
    unittest.main()
