# Performance Tuning Guide

This guide provides recommendations for optimizing the performance of your Qdrant multi-node cluster deployment. Fine-tuning your configuration can significantly improve search speed, throughput, and resource utilization.

## Cluster Configuration

### Optimizing Node Count

The number of nodes in your Qdrant cluster affects both performance and availability:

- **Rule of thumb**: Start with 3-5 nodes for a balanced deployment
- **Scaling factor**: Add 1 node for every ~5-10 million vectors (depends on vector size)
- **Search performance**: More nodes typically improve search throughput but may slightly increase latency due to network overhead

To adjust the node count, modify the `docker-compose.yml` file by adding or removing node definitions.

### Shard Configuration

Sharding is critical for distributing data across nodes:

```python
# In settings.py
SHARD_NUMBER = 4  # Default value
```

Recommended shard numbers:
- Small deployments (<1M vectors): 2-4 shards
- Medium deployments (1-10M vectors): 4-8 shards
- Large deployments (>10M vectors): 8-16 shards

Relation to nodes:
- **Best practice**: Configure `(shards ≥ nodes)` for better data distribution
- **Over-sharding**: Too many shards can increase overhead

To change the shard count:
1. Modify `SHARD_NUMBER` in `src/qdrant_demo/config/settings.py`
2. Update the collection creation in `QdrantClusterDemo.setup_collection()`

## Vector Indexing Optimization

### HNSW Parameters

Qdrant uses HNSW (Hierarchical Navigable Small World) for vector indexing. Key parameters:

```python
client.create_collection(
    collection_name="optimized_collection",
    vectors_config=models.VectorParams(
        size=768,
        distance=models.Distance.COSINE,
        hnsw_config=models.HnswConfigDiff(
            m=16,               # Number of edges per node
            ef_construct=100,   # Size of the dynamic candidate list during construction
            full_scan_threshold=10000  # Threshold for using HNSW vs exhaustive search
        )
    ),
    # ... other parameters
)
```

Parameter recommendations:
- `m`: 12-16 for most use cases (higher values = more accuracy but more memory)
- `ef_construct`: 100-200 (higher values = better index quality but slower construction)
- `full_scan_threshold`: 5000-20000 depending on vector dimensions

### Optimization Thresholds

Configure when optimization processes occur:

```python
client.create_collection(
    # ... other parameters
    optimizers_config=models.OptimizersConfigDiff(
        indexing_threshold=20000,    # When to start building index
        memmap_threshold=50000,      # When to switch to disk-based storage
        default_segment_number=5     # Target number of segments
    ),
)
```

Recommended values:
- `indexing_threshold`: 10000-50000 (batch inserts should exceed this)
- `memmap_threshold`: ~2-5x the indexing threshold
- `default_segment_number`: 3-7 (fewer segments = faster search but slower updates)

## Vector Storage Configuration

### Memory vs. Disk

Configure on-disk storage for better scalability:

```python
client.create_collection(
    # ... other parameters
    on_disk_payload=True,    # Store payload on disk
    on_disk=False            # Store vectors in memory (faster searches)
)
```

Guidelines:
- For fastest performance: `on_disk=False`, `on_disk_payload=True`
- For largest dataset size: `on_disk=True`, `on_disk_payload=True`
- Balance: Keep vectors in memory and payloads on disk

### Memory Allocation

For Docker-based deployments, allocate sufficient memory:

```yaml
qdrant_node1:
  # ... other configuration
  deploy:
    resources:
      limits:
        memory: 4G
```

Memory sizing guidelines:
- **Vector storage**: ~(vector_size * 4 bytes * number_of_vectors)
- **HNSW index**: ~(vector_size * 8-16 bytes * number_of_vectors)
- **Overhead**: Add 20-30% for operational overhead

## Query Optimization

### Filtering Strategies

Combine vector search with efficient filtering:

```python
client.search(
    collection_name="my_collection",
    query_vector=query_vector,
    query_filter=models.Filter(
        must=[
            models.FieldCondition(
                key="category",
                match=models.MatchValue(value="electronics")
            )
        ]
    ),
    limit=10
)
```

Performance tips:
- **Create payload indexes** for frequently filtered fields:
  ```python
  client.create_payload_index(
      collection_name="my_collection",
      field_name="category",
      field_schema=models.PayloadSchemaType.KEYWORD
  )
  ```
- **Filter cardinality**: Filtering on high-cardinality fields (many unique values) is more expensive
- **Filter order**: Place the most selective filters first in the `must` array

### Search Parameters

Fine-tune search accuracy vs. speed:

```python
client.search(
    collection_name="my_collection",
    query_vector=query_vector,
    limit=10,
    params=models.SearchParams(
        hnsw_ef=128,             # Size of the dynamic candidate list
        exact=False              # Use approximate search
    )
)
```

Guidelines:
- `hnsw_ef`: 50-500 (higher = more accurate but slower)
- `exact`: Set to `True` only when perfect recall is critical (much slower)
- `limit`: Request only as many results as needed

## Batch Operations

For better throughput when inserting data:

```python
# Instead of inserting one point at a time
points = []
for i in range(1000):
    points.append(models.PointStruct(
        id=i,
        vector=generate_random_vector(768),
        payload=generate_payload()
    ))

# Insert in a single batch operation
client.upsert(
    collection_name="my_collection",
    points=points
)
```

Batch operation tips:
- **Optimal batch size**: 100-1000 points per batch
- **Frequency**: Less frequent, larger batches are more efficient than many small batches
- **Parallel processing**: For multiple batches, use multiple threads/processes

## Monitoring Performance

Use the included Prometheus and Grafana setup to monitor:

1. **Query latency**: Track p95/p99 search times
2. **CPU/Memory usage**: Watch for resource bottlenecks
3. **Disk I/O**: Important when using on-disk storage

Key metrics to watch:
- `qdrant_requests_total`: Request count by type
- `qdrant_request_duration_seconds`: Request duration histogram
- `qdrant_segments_total`: Number of segments (affects search speed)

## Production Deployment Recommendations

### Hardware Recommendations

For production deployments, consider:

- **CPU**: 4-8 cores per node (vector operations benefit from multiple cores)
- **Memory**: 16-32GB for medium-sized collections
- **Disk**: SSD or NVMe storage for on-disk collections (avoid HDD)
- **Network**: Low-latency, high-throughput networking between nodes

### Cloud Deployment

When deploying to cloud environments:

- Use instance types optimized for memory
- Ensure nodes are in the same region/zone for lower inter-node latency
- Consider dedicated storage solutions for persistent data

### Load Balancing

For high-availability setups:
- Deploy a load balancer in front of Qdrant nodes
- Configure health checks based on the `/readiness` endpoint
- Direct client traffic to the load balancer rather than individual nodes 