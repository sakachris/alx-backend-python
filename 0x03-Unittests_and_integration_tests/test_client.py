#!/usr/bin/env python3
''' test_client.py '''

import unittest
from unittest.mock import patch
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    '''
    TestGithubOrgClient class
    '''
    @patch('client.get_json')
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    def test_org(self, org_name: str) -> None:
        ''' tests the class '''
        expected_url = f"https://api.github.com/orgs/{org_name}"

        with patch('client.get_json') as mock_get_json:
            mock_get_json.return_value = {}
            client = GithubOrgClient(org_name)
            org_info = client.org()

            mock_get_json.assert_called_once_with(expected_url)
            self.assertEqual(org_info, mock_get_json.return_value)
