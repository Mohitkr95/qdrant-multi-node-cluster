# API Reference

This document provides a detailed reference for the key classes and methods in the Qdrant Multi-Node Cluster project. Understanding these APIs will help you interact with the Qdrant cluster and build your own vector search applications.

## QdrantClusterDemo Class

The `QdrantClusterDemo` class is the primary interface for interacting with the Qdrant cluster. It provides methods for collection management, data insertion, and vector search operations.

```python
from qdrant_demo.core.cluster_demo import QdrantClusterDemo

demo = QdrantClusterDemo(host="localhost", port=6333)
```

### Constructor

```python
def __init__(self, host: str = settings.QDRANT_HOST, port: int = settings.QDRANT_PORT)
```

**Parameters:**
- `host` (str): Hostname or IP address of the Qdrant server
- `port` (int): Port number of the Qdrant server

**Returns:**
- An instance of the `QdrantClusterDemo` class

### Methods

#### run_demo

```python
def run_demo(self) -> None
```

Runs the complete demonstration, including setting up a collection, inserting data, demonstrating vector search, and displaying collection statistics.

**Parameters:** None

**Returns:** None

#### setup_collection

```python
def setup_collection(self) -> None
```

Sets up a collection with advanced configuration, including sharding and replication.

**Parameters:** None

**Returns:** None

**Example:**
```python
demo = QdrantClusterDemo()
demo.setup_collection()
```

#### insert_data

```python
def insert_data(self, count: int = settings.DEFAULT_POINT_COUNT) -> None
```

Inserts a specified number of random vectors with payload data.

**Parameters:**
- `count` (int): Number of vector points to insert

**Returns:** None

**Example:**
```python
# Insert 1000 random vectors
demo.insert_data(1000)
```

#### demonstrate_vector_search

```python
def demonstrate_vector_search(self) -> None
```

Demonstrates basic vector search capabilities, including filtered searches.

**Parameters:** None

**Returns:** None

**Example:**
```python
demo.demonstrate_vector_search()
```

#### demonstrate_scrolling

```python
def demonstrate_scrolling(
    self, 
    batches: int = settings.DEFAULT_BATCH_COUNT, 
    batch_size: int = settings.DEFAULT_BATCH_SIZE
) -> None
```

Demonstrates the scrolling API for paginating through large result sets.

**Parameters:**
- `batches` (int): Number of batches to retrieve
- `batch_size` (int): Size of each batch

**Returns:** None

**Example:**
```python
# Retrieve 5 batches of 20 points each
demo.demonstrate_scrolling(batches=5, batch_size=20)
```

#### get_cluster_stats

```python
def get_cluster_stats(self) -> None
```

Retrieves and displays collection and cluster statistics.

**Parameters:** None

**Returns:** None

**Example:**
```python
demo.get_cluster_stats()
```

## Data Generator Utilities

The `data_generator` module provides utilities for generating random vector data.

```python
from qdrant_demo.utils import data_generator
```

### Functions

#### generate_random_vector

```python
def generate_random_vector(vector_size: int = settings.VECTOR_SIZE) -> List[float]
```

Generates a random vector of specified dimensions.

**Parameters:**
- `vector_size` (int): Size of the vector to generate

**Returns:**
- List[float]: A list of float values representing a random vector

**Example:**
```python
# Generate a random vector with 768 dimensions
vector = data_generator.generate_random_vector(768)
```

#### generate_random_category

```python
def generate_random_category() -> str
```

Generates a random category from the predefined list.

**Parameters:** None

**Returns:**
- str: A random category name

**Example:**
```python
category = data_generator.generate_random_category()
```

#### generate_payload

```python
def generate_payload() -> Dict[str, Any]
```

Generates a random payload for a vector point.

**Parameters:** None

**Returns:**
- Dict[str, Any]: A dictionary containing category, score, and timestamp

**Example:**
```python
payload = data_generator.generate_payload()
```

## Direct Qdrant Client Usage

For more advanced use cases, you can use the Qdrant client directly:

```python
from qdrant_client import QdrantClient
from qdrant_client.http import models

client = QdrantClient(host="localhost", port=6333)
```

### Creating a Collection

```python
client.create_collection(
    collection_name="my_collection",
    shard_number=4,
    vectors_config=models.VectorParams(
        size=768, 
        distance=models.Distance.COSINE
    ),
    optimizers_config=models.OptimizersConfigDiff(
        indexing_threshold=20000,
        memmap_threshold=50000
    ),
    on_disk_payload=True
)
```

### Inserting Points

```python
client.upsert(
    collection_name="my_collection",
    points=[
        models.PointStruct(
            id=1,
            vector=[0.1, 0.2, 0.3, ...],
            payload={"category": "electronics", "score": 7.5}
        ),
    ],
)
```

### Vector Search

```python
search_result = client.search(
    collection_name="my_collection",
    query_vector=[0.1, 0.2, 0.3, ...],
    limit=5
)
```

### Filtered Vector Search

```python
filtered_search_result = client.search(
    collection_name="my_collection",
    query_vector=[0.1, 0.2, 0.3, ...],
    query_filter=models.Filter(
        must=[
            models.FieldCondition(
                key="category",
                match=models.MatchValue(value="electronics")
            ),
            models.FieldCondition(
                key="score",
                range=models.Range(
                    gte=5.0,
                )
            )
        ]
    ),
    limit=5
)
```

### Pagination with Scrolling

```python
offset = None
batch_size = 10

while True:
    scroll_result = client.scroll(
        collection_name="my_collection",
        limit=batch_size,
        offset=offset,
        with_payload=True,
        with_vectors=False,
    )
    points, offset = scroll_result
    
    # Process points here...
    
    if offset is None:
        break  # No more points to retrieve
```

### Getting Collection Information

```python
collection_info = client.get_collection("my_collection")
```

## Command Line Interface

The project provides a command-line interface for running the demo:

```bash
python src/run_demo.py --host localhost --port 6333 --points 2000
```

### Arguments

- `--host`: Hostname or IP address of the Qdrant server (default: localhost)
- `--port`: Port number of the Qdrant server (default: 6333)
- `--points`: Number of random points to generate and insert (default: 1000) 