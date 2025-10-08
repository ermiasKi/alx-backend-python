import unittest
from unittest.mock import Mock, patch, PropertyMock
from client import GithubOrgClient
from parameterized import parameterized
from utils import get_json




class TestGithubOrgClient(unittest.TestCase):

    @parameterized.expand([
        ('google'),
        ('abc'),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get):

        expected_url = f"https://api.github.com/orgs/{org_name}"
        expected_payload = {"login": org_name, "id": 1234}
        mock_get.return_value = expected_payload

        instance = GithubOrgClient(org_name)
        result = instance.org
        
        mock_get.assert_called_once_with(expected_url)
        self.assertEqual(result, expected_payload)
        
    def test_public_repos_url(self):
        with patch.object(GithubOrgClient, 'org', new_callable=PropertyMock) as mock_get:
            
            expected_payload = {"repos_url": 'google.com', "id": 1234}
            mock_get.return_value = expected_payload

            instance = GithubOrgClient("google")
            result = instance._public_repos_url
            print(result)

            self.assertEqual(result, expected_payload['repos_url'])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):

        expected_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = expected_payload
        
        with patch.object(GithubOrgClient, '_public_repos_url', new_callable=PropertyMock) as mock_public_repos:
            mock_public_repos.return_value = "org_name"
            client = GithubOrgClient("test-org")
            result = client.public_repos()

            self.assertEqual(['repo1', 'repo2', 'repo3'], result)
            mock_public_repos.assert_called_once()
            mock_get_json.assert_called_once()
        

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        client = GithubOrgClient("test-org")
        result = client.has_license(repo, license_key)

        self.assertEqual(result, expected)

