#!/usr/bin/env python3
"""Test module for utils functions."""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map
from utils import get_json
from utils import memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test class for access_nested_map function."""

    @parameterized.expand([
        # check if access nested map works correctly
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that access_nested_map returns the expected result."""
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected)

    # check if access nested map method raises a key error correctly
    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test that access_nested_map raises KeyError for invalid paths."""
        with self.assertRaises(KeyError) as context_manager:
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Test class for get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """Test that get_json returns the expected result."""
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)
        mock_get.assert_called_once_with(test_url)

        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test class for memoize decorator."""

    def test_memoize(self):
        """Test that memoize decorator caches the result properly."""
        class TestClass:
            """Test class for memoize testing."""

            def a_method(self):
                """Return a test value."""
                return 42

            @memoize
            def a_property(self):
                """Memoized property that calls a_method."""
                return self.a_method()

        test_instance = TestClass()

        with patch.object(test_instance, 'a_method') as mock_a_method:
            mock_a_method.return_value = 42

            result1 = test_instance.a_property()
            result2 = test_instance.a_property()

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_a_method.assert_called_once()


