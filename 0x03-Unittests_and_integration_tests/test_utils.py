#!/usr/bin/env python3
''' test_utils.py '''

import unittest
from parameterized import parameterized
from utils import access_nested_map
from typing import Any, Mapping, Sequence, Dict, Tuple


class TestAccessNestedMap(unittest.TestCase):

    @parameterized.expand([
        ({"a": 1}, ["a"], 1),
        ({"a": {"b": 2}}, ["a"], {"b": 2}),
        ({"a": {"b": 2}}, ["a", "b"], 2),
    ])
    def test_access_nested_map(
        self,
        nested_map: Mapping[str, Any],
        path: Sequence,
        expected_result: Any
    ) -> None:
        ''' test access nested map '''
        self.assertEqual(access_nested_map(nested_map, path), expected_result)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(
            self,
            nested_map: Dict,
            path: Tuple[str],
            exception: Exception,
            ) -> None:
        ''' test access nested map exception '''
        with self.assertRaises(exception):
            access_nested_map(nested_map, path)
