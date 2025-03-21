# Troubleshooting Guide

This guide addresses common issues you might encounter when working with the Qdrant Multi-Node Cluster project and provides solutions to resolve them.

## Docker Deployment Issues

### Containers Fail to Start

**Symptoms:** 
- Docker containers don't start or exit immediately after starting
- `docker-compose ps` shows services in an exited state

**Potential Causes and Solutions:**

1. **Port Conflicts**

   **Problem:** The default ports (6333, 9090, 3000) are already in use.
   
   **Solution:**
   ```bash
   # Check if ports are in use
   lsof -i :6333
   lsof -i :9090
   lsof -i :3000
   
   # Modify docker-compose.yml to use different ports
   # Example:
   #   ports:
   #     - "6334:6333"  # Maps container's 6333 to host's 6334
   ```

2. **Insufficient Permissions**

   **Problem:** Docker doesn't have permission to create or access storage directories.
   
   **Solution:**
   ```bash
   # Give appropriate permissions to the data directory
   sudo chmod -R 777 deployments/docker/data
   ```

3. **Configuration Errors**

   **Solution:** Check container logs for specific error messages:
   ```bash
   docker-compose logs qdrant_node1
   ```

### Cluster Configuration Issues

**Symptoms:**
- Nodes start but don't connect to each other
- Searches only return results from one node

**Solutions:**

1. **Check Connectivity**
   ```bash
   # Enter a container to test connectivity
   docker exec -it qdrant_node1 sh
   
   # Test inter-node connectivity
   wget -q -O- http://qdrant_node2:6335
   ```

2. **Verify Cluster Status**
   ```bash
   # Check cluster status via API
   curl http://localhost:6333/cluster
   ```

3. **Restart the Bootstrap Node**
   ```bash
   docker-compose restart qdrant_node1
   # Wait a moment, then restart other nodes
   docker-compose restart qdrant_node2 qdrant_node3
   ```

## Python Client Issues

### Connection Errors

**Symptoms:**
- `Connection refused` errors when running the demo script
- Timeouts when attempting to connect to Qdrant

**Solutions:**

1. **Check Qdrant Readiness**
   ```bash
   # Verify Qdrant is ready to accept connections
   curl http://localhost:6333/readiness
   
   # Should return:
   # {"status":"ok"}
   ```

2. **Network Isolation Issues**
   
   If running in different network namespaces:
   ```bash
   # Check the network settings
   docker network ls
   
   # Ensure the client can reach the Qdrant service
   # If running outside Docker, use localhost:6333
   # If running inside Docker, use the service name
   ```

3. **Version Compatibility**
   
   Ensure the Python client version matches the Qdrant server version:
   ```bash
   # Check installed client version
   pip show qdrant-client
   
   # Adjust in requirements.txt and reinstall if needed
   pip install -U qdrant-client==1.6.1
   ```

### Collection Operations Failing

**Symptoms:**
- `CollectionNotFound` errors
- Collection creation fails

**Solutions:**

1. **Check Collection Existence**
   ```python
   # In your Python code
   collections = client.get_collections().collections
   print([c.name for c in collections])
   ```

2. **Delete and Recreate**
   ```python
   try:
       client.delete_collection(collection_name="sharding_collection")
   except:
       pass  # Ignore if collection doesn't exist
   
   # Create collection with proper configuration
   ```

3. **Check for Shard Allocation Failures**
   ```bash
   curl http://localhost:6333/collections/sharding_collection
   ```
   
   Look for errors in the shard allocation section.

## Search and Query Issues

### Empty Search Results

**Symptoms:**
- Vector searches return empty results
- Filtered searches don't return expected points

**Solutions:**

1. **Check Vector Size**
   ```python
   # Ensure query vector dimensions match collection vector size
   print(f"Vector dimensions: {len(query_vector)}")
   collection_info = client.get_collection("sharding_collection")
   print(f"Expected dimensions: {collection_info.config.params.vectors.size}")
   ```

2. **Verify Data Insertion**
   ```python
   # Check if points were actually inserted
   collection_info = client.get_collection("sharding_collection")
   print(f"Points in collection: {collection_info.points_count}")
   ```

3. **Review Filter Criteria**
   ```python
   # Try a simpler filter first
   simpler_filter = models.Filter(
       must=[
           models.FieldCondition(
               key="category",
               match=models.MatchValue(value="electronics")
           )
       ]
   )
   ```

4. **Check Payload Indexing**
   ```bash
   # Verify payload indexes
   curl http://localhost:6333/collections/sharding_collection/index
   ```

### Slow Search Performance

**Symptoms:**
- Searches take longer than expected
- Increasing latency over time

**Solutions:**

1. **Check Segment Count**
   ```python
   collection_info = client.get_collection("sharding_collection")
   print(f"Segments: {collection_info.segments_count}")
   ```
   
   If segment count is high, optimize the collection:
   ```python
   client.update_collection(
       collection_name="sharding_collection",
       optimizers_config=models.OptimizersConfigDiff(
           default_segment_number=5
       )
   )
   ```

2. **Reduce Search Parameters**
   ```python
   # Use a lower ef parameter for faster (less accurate) search
   search_result = client.search(
       collection_name="sharding_collection",
       query_vector=query_vector,
       limit=10,
       params=models.SearchParams(hnsw_ef=40)
   )
   ```

3. **Monitor Resource Usage**
   
   Check Prometheus/Grafana for:
   - High CPU usage
   - Memory pressure
   - Disk I/O bottlenecks

## Monitoring Issues

### Prometheus Not Collecting Metrics

**Symptoms:**
- No data in Prometheus UI
- "No data points" in Grafana

**Solutions:**

1. **Check Prometheus Targets**
   
   Open `http://localhost:9090/targets` and verify:
   - All Qdrant nodes are listed
   - Status is "UP" for each target

2. **Verify Prometheus Configuration**
   ```bash
   # Check prometheus.yml
   cat config/prometheus.yml
   
   # Ensure targets are correctly specified
   # - targets: ['qdrant_node1:6333', 'qdrant_node2:6333', 'qdrant_node3:6333']
   ```

3. **Restart Prometheus**
   ```bash
   docker-compose restart prometheus
   ```

### Grafana Dashboard Not Working

**Symptoms:**
- Grafana dashboard shows no data
- Connection errors to Prometheus

**Solutions:**

1. **Check Prometheus Data Source**
   
   In Grafana (`http://localhost:3000`):
   - Go to Configuration > Data Sources
   - Verify Prometheus URL is set to `http://prometheus:9090`
   - Test connection

2. **Import Dashboard Again**
   ```bash
   # Check dashboard JSON
   cat config/grafana.json
   
   # In Grafana UI:
   # 1. Create a new dashboard
   # 2. Import via dashboard JSON
   # 3. Paste the content of grafana.json
   ```

3. **Check Grafana Permissions**
   
   Ensure the Grafana container has access to the dashboard file:
   ```bash
   # Update permissions if needed
   chmod 644 config/grafana.json
   docker-compose restart grafana
   ```

## Performance Issues

### High Memory Usage

**Symptoms:**
- Docker containers using excessive memory
- OOM (Out Of Memory) errors

**Solutions:**

1. **Set Memory Limits**
   
   Update `docker-compose.yml`:
   ```yaml
   qdrant_node1:
     # ... other config
     deploy:
       resources:
         limits:
           memory: 2G
   ```

2. **Optimize Collection Configuration**
   ```python
   # Store payloads on disk
   client.create_collection(
       collection_name="memory_optimized",
       vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
       on_disk_payload=True
   )
   ```

3. **Reduce Vector Dimensions**
   
   If possible, use lower-dimensional vectors:
   ```python
   # Adjust in settings.py
   VECTOR_SIZE = 256  # Instead of 768
   ```

### Disk Space Issues

**Symptoms:**
- "No space left on device" errors
- Docker containers exiting unexpectedly

**Solutions:**

1. **Clean Up Docker**
   ```bash
   # Remove unused Docker resources
   docker system prune -a
   ```

2. **Monitor Disk Usage**
   ```bash
   # Check disk usage in the data directory
   du -sh deployments/docker/data/*
   ```

3. **Configure Disk Storage Limits**
   
   Set limits in collection creation:
   ```python
   client.create_collection(
       # ... other parameters
       optimizers_config=models.OptimizersConfigDiff(
           indexing_threshold=20000,
           memmap_threshold=50000
       ),
   )
   ```

## Troubleshooting Commands Reference

### Docker Commands

```bash
# View all containers
docker-compose ps

# Check container logs
docker-compose logs qdrant_node1

# Follow logs in real-time
docker-compose logs -f qdrant_node1

# Restart a specific service
docker-compose restart qdrant_node1

# Restart all services
docker-compose restart

# Stop and remove all containers
docker-compose down

# Rebuild and restart all containers
docker-compose up -d --build
```

### Qdrant API Commands

```bash
# Check Qdrant health
curl http://localhost:6333/health

# Check readiness
curl http://localhost:6333/readiness

# List collections
curl http://localhost:6333/collections

# Get collection details
curl http://localhost:6333/collections/sharding_collection

# Check cluster status (if available)
curl http://localhost:6333/cluster
```

### Python Debugging

```python
# Debug connection issues
from qdrant_client import QdrantClient
import logging

# Enable verbose logging
logging.basicConfig(level=logging.DEBUG)

# Test connection
client = QdrantClient(host="localhost", port=6333)
try:
    result = client.get_collections()
    print("Success:", result)
except Exception as e:
    print("Error:", e)
```

If you encounter issues not covered in this guide, please [open an issue](https://github.com/Mohitkr95/qdrant-multi-node-cluster/issues) on the GitHub repository with detailed information about the problem. 