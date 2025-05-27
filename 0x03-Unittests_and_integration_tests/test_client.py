#!/usr/bin/env python3
"""test_client.py"""

import unittest
from unittest.mock import patch, MagicMock, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient
from typing import Dict
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """
    TestGithubOrgClient class
    """

    @parameterized.expand(
        [
            ("google", {"login": "google"}),
            ("abc", {"login": "abc"}),
        ]
    )
    @patch(
        "client.get_json",
    )
    def test_org(self, org: str, resp: Dict, mocked_fxn: MagicMock) -> None:
        """testing GithubOrgClient response"""
        mocked_fxn.return_value = MagicMock(return_value=resp)
        gh_org_client = GithubOrgClient(org)
        self.assertEqual(gh_org_client.org(), resp)
        mocked_fxn.assert_called_once_with(
            f"https://api.github.com/orgs/{org}"
        )

    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """test public repos url"""
        mock_org.return_value = {
            "repos_url": "https://api.github.com/users/google/repos"
        }
        self.assertEqual(
            GithubOrgClient("google")._public_repos_url,
            "https://api.github.com/users/google/repos",
        )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos method using TEST_PAYLOAD"""
        org_payload, repos_payload, expected_names, _ = TEST_PAYLOAD[0]

        # Mock get_json to return repos_payload
        mock_get_json.return_value = repos_payload

        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=PropertyMock
        ) as mock_repos_url:
            mock_repos_url.return_value = org_payload["repos_url"]

            client = GithubOrgClient("google")
            result = client.public_repos()

            self.assertEqual(result, expected_names)
            mock_get_json.assert_called_once_with(org_payload["repos_url"])
            mock_repos_url.assert_called_once()
