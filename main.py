import logging
from qdrant_client import QdrantClient
from qdrant_client.http import models

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
    shard_number=1,
    sharding_method=models.ShardingMethod.CUSTOM,
    vectors_config=models.VectorParams(size=3, distance=models.Distance.COSINE)
)
logger.info(f"Created collection '{collection_name}' with custom sharding: {response}")

# Creating a shard key for the collection
response = client.create_shard_key(f"{collection_name}", f"{key}")
logger.info(f"Created shard key '{key}' for collection '{collection_name}': {response}")

# Upserting points into the collection
response = client.upsert(
    collection_name=f"{collection_name}",
    points=[
        models.PointStruct(
            id=1111,
            vector=[0.1, 0.2, 0.3],
        ),
    ],
    shard_key_selector=f"{key}",
)
logger.info(f"Upserted points into collection '{collection_name}' with shard key '{key}': {response}")
