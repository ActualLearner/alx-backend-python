#!/usr/bin/env python3
"""Unit tests for the GithubOrgClient class"""
import unittest
from client import GithubOrgClient
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, Mock, PropertyMock
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient."""
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct payload"""
        test_payload = {
            "name": org_name,
            "repos_url": f"https://api.github.com/orgs/{org_name}/repos"
        }
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org

        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, test_payload)
        mock_get_json.reset_mock()

    def test_public_repos_url(self):
        """Test the GithubOrgClient.public_repos_url method."""
        payload = {"repos_url": "google"}
        with patch.object(
                GithubOrgClient,
                "org",
                new_callable=PropertyMock) as mock_org:
            mock_org.return_value = payload
            client = GithubOrgClient('google')
            result = client._public_repos_url
            self.assertEqual(result, payload['repos_url'])

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos method"""
        repos_payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = repos_payload

        with patch.object(
                GithubOrgClient,
                "_public_repos_url",
                new_callable=PropertyMock) as mock_public_repos_url:

            client = GithubOrgClient("google")
            expected_url = f"https://api.github.com/orgs/{client._org_name}"
            mock_public_repos_url.return_value = expected_url

            result = client.public_repos()

            self.assertEqual(result, [repo['name'] for repo in repos_payload])
            mock_get_json.assert_called_once_with(expected_url)
            mock_public_repos_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license"),
        ({"license": {"key": "other_license"}}, "other_license"),
    ])
    def test_has_license(self, license, license_key):
        result = GithubOrgClient.has_license(license, license_key)
        self.assertTrue(result)


@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": TEST_PAYLOAD[0][2],
        "apache2_repos": TEST_PAYLOAD[0][3],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            if url.endswith("/orgs/google"):
                mock_response = Mock()
                mock_response.json.return_value = TEST_PAYLOAD[0][0]
                return mock_response
            elif url.endswith("/orgs/google/repos"):
                mock_response = Mock()
                mock_response.json.return_value = TEST_PAYLOAD[0][1]
                return mock_response

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()
