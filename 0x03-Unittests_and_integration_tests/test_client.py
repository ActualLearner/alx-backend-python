#!/usr/bin/env python3
"""Unit tests for the GithubOrgClient class"""
import unittest
from client import GithubOrgClient
from parameterized import parameterized
from unittest.mock import patch, Mock
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

    @patch('client.get_json')
    def test_public_repos_url(self, mock_get_json: Mock):
        """Test the GithubOrgClient.public_repos_url method."""
        mock_get_json.return_value = {"json": "google"}
        payload = {"login": "google"}
        with patch("client.GithubOrgClient.org") as mock_org:
            mock_org.return_value = payload
            client = GithubOrgClient('google')
            result = client._public_repos_url()
            self.assertEqual(result, payload)
            mock_get_json.assert_called_once()
            mock_org.assert_called_once()
