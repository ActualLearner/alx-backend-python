import unittest
from parameterized import parameterized
from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):
    """Unit test for utils.py"""
    
    @parameterized.expand([
        ({'a': 1}, ("a",), 1),
        ({'a': {'b': 2}}, ('a',), 2),
        ({'a': {'b': 2}}, ('a', 'b'), 2)]
    )
    def test_access_nested_map(self, nested_map, path, expected) -> bool:
        """Test access_nested_map function"""
        self.assertEqual(access_nested_map(nested_map, path), expected)
        
