"""
Utilities for generating random vector data and categories.
"""

import random
import time
from typing import List, Dict, Any

from qdrant_demo.config import settings


def generate_random_vector(vector_size: int = settings.VECTOR_SIZE) -> List[float]:
    """
    Generate a random vector with specified dimensions.
    
    Args:
        vector_size: Size of the vector to generate
        
    Returns:
        List of float values representing a random vector
    """
    return [round(random.uniform(0, 1), 15) for _ in range(vector_size)]


def generate_random_category() -> str:
    """
    Generate a random category from predefined options.
    
    Returns:
        A randomly selected category string
    """
    return random.choice(settings.CATEGORIES)


def generate_payload() -> Dict[str, Any]:
    """
    Generate a random payload for a vector point.
    
    Returns:
        Dictionary containing category, score and timestamp
    """
    return {
        "category": generate_random_category(),
        "score": round(random.uniform(settings.SCORE_MIN, settings.SCORE_MAX), 2),
        "timestamp": int(time.time())
    } 