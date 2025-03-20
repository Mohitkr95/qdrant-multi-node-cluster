"""
Tests for the data generator utilities.
"""

import unittest

from qdrant_demo.utils.data_generator import (
    generate_random_vector,
    generate_random_category,
    generate_payload
)
from qdrant_demo.config import settings


class TestDataGenerator(unittest.TestCase):
    """Test cases for data generator functions."""
    
    def test_generate_random_vector(self):
        """Test vector generation."""
        vector = generate_random_vector()
        self.assertEqual(len(vector), settings.VECTOR_SIZE)
        
        # Test with custom size
        custom_size = 128
        vector = generate_random_vector(custom_size)
        self.assertEqual(len(vector), custom_size)
        
        # Verify values are within range
        for val in vector:
            self.assertTrue(0 <= val <= 1)
    
    def test_generate_random_category(self):
        """Test category generation."""
        category = generate_random_category()
        self.assertIn(category, settings.CATEGORIES)
    
    def test_generate_payload(self):
        """Test payload generation."""
        payload = generate_payload()
        
        # Check payload structure
        self.assertIn("category", payload)
        self.assertIn("score", payload)
        self.assertIn("timestamp", payload)
        
        # Check payload values
        self.assertIn(payload["category"], settings.CATEGORIES)
        self.assertTrue(settings.SCORE_MIN <= payload["score"] <= settings.SCORE_MAX)
        self.assertIsInstance(payload["timestamp"], int)


if __name__ == "__main__":
    unittest.main() 