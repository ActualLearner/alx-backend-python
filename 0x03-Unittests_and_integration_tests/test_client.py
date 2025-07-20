#!/usr/bin/env python3
"""Unit tests for the functions defined in the client module.

This test suite verifies the correctness of:
- org
- get_json
- memoize
"""
import unittest
from client import GithubOrgClient
from parameterized import parameterized
from unittest.mock import patch, Mock
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Integration test for the GithubOrgClient class"""

    @parameterized.expand([
        ('google'),
        ('abc'),
    ])
    @patch('utils.get_json')
    def test_org(self, name, mock_get_json):

        mock_get_json.return_value = TEST_PAYLOAD

        client = GithubOrgClient(name)

        result = client.org()

        expected_url = "https://api.github.com/orgs/google"
        mock_get_json.assert_called_once_with(expected_url)

        self.assertEqual(result, TEST_PAYLOAD)
