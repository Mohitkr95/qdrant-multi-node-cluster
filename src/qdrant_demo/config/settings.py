"""
Configuration settings for the Qdrant demo.
"""

# Qdrant connection settings
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333

# Collection settings
COLLECTION_NAME = "sharding_collection"
SHARD_KEY = "tempKey"
VECTOR_SIZE = 768
SHARD_NUMBER = 4

# Data generation settings
DEFAULT_POINT_COUNT = 1000
SCORE_MIN = 0
SCORE_MAX = 10
CATEGORIES = ["electronics", "clothing", "food", "books", "sports"]

# Search settings
DEFAULT_SEARCH_LIMIT = 5
DEFAULT_BATCH_SIZE = 10
DEFAULT_BATCH_COUNT = 3 