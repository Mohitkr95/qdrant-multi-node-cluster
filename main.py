import logging
from qdrant_client import QdrantClient
from qdrant_client.http import models
import random

# Configure logging for your application
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Increase log level for httpx to WARNING to suppress its INFO logs
logging.getLogger("httpx").setLevel(logging.WARNING)

client = QdrantClient("localhost", port=6333)
collection_name = "sharding_collection"
key = "tempKey"

# Deleting an existing collection if it exists
response = client.delete_collection(collection_name=f"{collection_name}")
logger.info(f"Deleted collection '{collection_name}': {response}")

# Creating a new collection with specific configuration
response = client.create_collection(
    collection_name=f"{collection_name}",
    shard_number=6,
    sharding_method=models.ShardingMethod.CUSTOM,
    vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE)
)
logger.info(f"Created collection '{collection_name}' with custom sharding: {response}")

# Creating a shard key for the collection
response = client.create_shard_key(f"{collection_name}", f"{key}")
logger.info(f"Created shard key '{key}' for collection '{collection_name}': {response}")

# Counter for generating unique point IDs
point_counter = 0

# Function to generate a random vector of 768 dimensions with up to 15 decimal points
def generate_random_vector():
    return [round(random.uniform(0, 1), 15) for _ in range(768)]

# Run the loop 1000 times
for _ in range(1000):
    random_vector = generate_random_vector()
    point_counter += 1
    response = client.upsert(
        collection_name=f"{collection_name}",
        points=[
            models.PointStruct(
                id=point_counter,
                vector=random_vector,
            ),
        ],
        shard_key_selector=f"{key}",
    )
    logger.info(f"Upserted point with ID {point_counter} into collection '{collection_name}' with shard key '{key}': {response}")