#!/usr/bin/env python3

import fixtures
import unittest
from client import GithubOrgClient
from unittest.mock import patch, PropertyMock
from parameterized import parameterized_class, parameterized


class TestGithubOrgClient(unittest.TestCase):

    @parameterized.expand([
        ("google"),
        ("abc"),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        test_payload = {"name": org_name, "repos_url": f"https://api.github.com/orgs/{org_name}/repos"}
        mock_get_json.return_value = test_payload
        
        # Create client instance
        client = GithubOrgClient(org_name)
        
        # Call the org property twice (should use memoization)
        result1 = client.org()
        result2 = client.org()
        
        # Verify get_json was called exactly once with correct URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        
        # Verify both calls return the expected payload
        self.assertEqual(result1, test_payload)
        self.assertEqual(result2, test_payload)
        
        # Verify both results are the same object (memoization working)
        self.assertIs(result1, result2)


    def test_public_repos_url(self):
        """Test that GithubOrgClient._public_repos_url returns the expected value"""
        # Test payload with known repos_url
        test_payload = {
            "repos_url": "https://api.github.com/orgs/testorg/repos",
            "name": "testorg",
            "other_data": "value"
        }
        
        # Create client instance
        client = GithubOrgClient("testorg")
        
        # Patch the org property to return our test payload
        with patch('client.GithubOrgClient.org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = test_payload
            
            # Call the _public_repos_url property
            result = client._public_repos_url
            
            # Verify the result is the expected repos_url from our test payload
            self.assertEqual(result, "https://api.github.com/orgs/testorg/repos")
            
            # Verify the org property was accessed (since _public_repos_url uses it)
            mock_org.assert_called_once()

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that GithubOrgClient.public_repos returns the expected list of repos"""
        # Mock payload for repos
        test_repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": None},
        ]
        mock_get_json.return_value = test_repos_payload
        
        # Mock _public_repos_url property
        test_repos_url = "https://api.github.com/orgs/testorg/repos"
        
        # Create client instance
        client = GithubOrgClient("testorg")
        
        with patch('client.GithubOrgClient._public_repos_url', 
            new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = test_repos_url
            
            # Call public_repos without license filter
            repos = client.public_repos()
            
            # Verify the list of repo names is correct
            expected_repos = ["repo1", "repo2", "repo3"]
            self.assertEqual(repos, expected_repos)
            
            # Verify _public_repos_url was accessed once
            mock_public_repos_url.assert_called_once()
            
            # Verify get_json was called once with the correct URL
            mock_get_json.assert_called_once_with(test_repos_url)
        
    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected_result):
        """Test that GithubOrgClient.has_license returns the expected result"""
        # Call the static method
        result = GithubOrgClient.has_license(repo, license_key)
        
        # Verify the result matches expected value
        self.assertEqual(result, expected_result)

@parameterized_class([
    {
        'org_payload': fixtures.TEST_PAYLOAD[0][0],
        'repos_payload': fixtures.TEST_PAYLOAD[0][1],
        'expected_repos': fixtures.TEST_PAYLOAD[0][2],
        'apache2_repos': fixtures.TEST_PAYLOAD[0][3],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Set up class method to mock requests.get"""
        cls.get_patcher = patch('client.requests.get')
        cls.mock_get = cls.get_patcher.start()
        
        # Configure the mock to return different payloads based on URL
        def side_effect(url):
            if url == "https://api.github.com/orgs/google":
                mock_response = unittest.mock.Mock()
                mock_response.json.return_value = cls.org_payload
                return mock_response
            elif url == cls.org_payload["repos_url"]:
                mock_response = unittest.mock.Mock()
                mock_response.json.return_value = cls.repos_payload
                return mock_response
            else:
                return unittest.mock.Mock()  # Default mock for other URLs
        
        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Tear down class method to stop the patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos without license filter"""
        client = GithubOrgClient("google")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos with Apache 2.0 license filter"""
        client = GithubOrgClient("google")
        repos = client.public_repos("apache-2.0")
        self.assertEqual(repos, self.apache2_repos)

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized_class
import fixtures
from client import GithubOrgClient


@parameterized_class([
    {
        'org_payload': fixtures.TEST_PAYLOAD[0][0],
        'repos_payload': fixtures.TEST_PAYLOAD[0][1],
        'expected_repos': fixtures.TEST_PAYLOAD[0][2],
        'apache2_repos': fixtures.TEST_PAYLOAD[0][3],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Set up class method to mock requests.get"""
        cls.get_patcher = patch('client.requests.get')
        cls.mock_get = cls.get_patcher.start()
        
        # Configure the mock to return different payloads based on URL
        def side_effect(url):
            if url == "https://api.github.com/orgs/google":
                mock_response = unittest.mock.Mock()
                mock_response.json.return_value = cls.org_payload
                return mock_response
            elif url == cls.org_payload["repos_url"]:
                mock_response = unittest.mock.Mock()
                mock_response.json.return_value = cls.repos_payload
                return mock_response
            else:
                return unittest.mock.Mock()  # Default mock for other URLs
        
        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Tear down class method to stop the patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos without license filter"""
        client = GithubOrgClient("google")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)
        
        # Verify the mocked requests.get was called twice:
        # 1. For org data (to get repos_url)
        # 2. For repos data
        self.assertEqual(self.mock_get.call_count, 2)
        
        # Verify the correct URLs were called
        calls = self.mock_get.call_args_list
        self.assertIn("https://api.github.com/orgs/google", str(calls[0]))
        self.assertIn(self.org_payload["repos_url"], str(calls[1]))

    def test_public_repos_with_license(self):
        """Test public_repos with Apache 2.0 license filter"""
        client = GithubOrgClient("google")
        repos = client.public_repos("apache-2.0")
        self.assertEqual(repos, self.apache2_repos)
        
        # Verify the mocked requests.get was called twice:
        # 1. For org data (to get repos_url)
        # 2. For repos data
        self.assertEqual(self.mock_get.call_count, 2)
        
        # Verify the correct URLs were called
        calls = self.mock_get.call_args_list
        self.assertIn("https://api.github.com/orgs/google", str(calls[0]))
        self.assertIn(self.org_payload["repos_url"], str(calls[1]))