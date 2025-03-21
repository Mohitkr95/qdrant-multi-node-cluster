# Configuration Guide

This guide covers the various configuration options available in the Qdrant Multi-Node Cluster project. Understanding these options will help you customize the deployment to meet your specific requirements.

## Docker Compose Configuration

The `docker-compose.yml` file is the primary configuration point for the deployment. It defines the Qdrant nodes, Prometheus, and Grafana services.

### Qdrant Node Configuration

Each Qdrant node has several configurable parameters:

```yaml
qdrant_node1:
  image: qdrant/qdrant:v1.6.1
  container_name: qdrant_node1
  volumes:
    - ./data/node1:/qdrant/storage
  ports:
    - "6333:6333"
  environment:
    QDRANT__CLUSTER__ENABLED: "true"
    QDRANT__LOG_LEVEL: "INFO"
  command: "./qdrant --uri http://qdrant_node1:6335"
```

#### Image Version

- `image: qdrant/qdrant:v1.6.1`: The Qdrant docker image version. Update this to use newer versions as they become available.

#### Storage Configuration

- `volumes: - ./data/node1:/qdrant/storage`: Maps the local directory `./data/node1` to the Qdrant storage path inside the container. This ensures data persistence between container restarts.

#### Network Configuration

- `ports: - "6333:6333"`: Maps the container's port 6333 to the host's port 6333. This is the HTTP API port used for client interactions.

#### Environment Variables

Several environment variables control Qdrant's behavior:

| Variable | Description | Default |
|----------|-------------|---------|
| `QDRANT__CLUSTER__ENABLED` | Enables clustering mode | `"true"` |
| `QDRANT__LOG_LEVEL` | Sets logging verbosity | `"INFO"` |

Additional environment variables you might want to configure:

| Variable | Description | Example |
|----------|-------------|---------|
| `QDRANT__STORAGE__OPTIMIZERS__DEFAULT_SEGMENT_NUMBER` | Number of segments to maintain | `"5"` |
| `QDRANT__STORAGE__OPTIMIZERS__MEMMAP_THRESHOLD` | Threshold to store vectors on disk | `"20000"` |
| `QDRANT__STORAGE__OPTIMIZERS__INDEXING_THRESHOLD` | Threshold to create index | `"10000"` |

#### Cluster Command

- `command: "./qdrant --uri http://qdrant_node1:6335"`: Specifies the URI that other nodes will use to connect to this node.
  
For peer nodes, the command includes a `--bootstrap` parameter:

```yaml
command: "./qdrant --bootstrap http://qdrant_node1:6335 --uri http://qdrant_node2:6335"
```

This tells the node to connect to the bootstrap node at the specified address.

### Prometheus Configuration

Prometheus is configured through the `prometheus.yml` file:

```yaml
global:
  scrape_interval: 10s

scrape_configs:
  - job_name: 'qdrant'
    static_configs:
      - targets: ['qdrant_node1:6333', 'qdrant_node2:6333', 'qdrant_node3:6333']
```

- `scrape_interval`: Defines how often Prometheus collects metrics (in seconds)
- `targets`: Lists the Qdrant nodes to collect metrics from

### Grafana Configuration

Grafana is configured through environment variables and volume mounts:

```yaml
grafana:
  image: grafana/grafana:latest
  container_name: grafana
  ports:
    - "3000:3000"
  environment:
    GF_SECURITY_ADMIN_USER: 'admin'
    GF_SECURITY_ADMIN_PASSWORD: 'admin'
    GF_USERS_ALLOW_SIGN_UP: 'true'
  volumes:
    - grafana-data:/var/lib/grafana
    - ../../config/grafana.json:/etc/grafana/provisioning/dashboards/qdrant-dashboard.json
```

- `GF_SECURITY_ADMIN_USER` and `GF_SECURITY_ADMIN_PASSWORD`: Default admin credentials
- `GF_USERS_ALLOW_SIGN_UP`: Controls whether new users can sign up
- The Grafana dashboard configuration is mounted from `../../config/grafana.json`

## Python Client Configuration

The Python client is configured through settings in `src/qdrant_demo/config/settings.py`.

### Connection Settings

```python
# Qdrant connection settings
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
```

### Collection Settings

```python
# Collection settings
COLLECTION_NAME = "sharding_collection"
SHARD_KEY = "tempKey"
VECTOR_SIZE = 768
SHARD_NUMBER = 4
```

- `COLLECTION_NAME`: Name of the collection to create in Qdrant
- `SHARD_KEY`: Key used for sharding data across nodes
- `VECTOR_SIZE`: Dimensionality of vectors stored in the collection
- `SHARD_NUMBER`: Number of shards to create

### Data Generation Settings

```python
# Data generation settings
DEFAULT_POINT_COUNT = 1000
SCORE_MIN = 0
SCORE_MAX = 10
CATEGORIES = ["electronics", "clothing", "food", "books", "sports"]
```

- `DEFAULT_POINT_COUNT`: Default number of random vectors to generate
- `SCORE_MIN` and `SCORE_MAX`: Range for random score values
- `CATEGORIES`: List of categories to randomly assign to vectors

### Search Settings

```python
# Search settings
DEFAULT_SEARCH_LIMIT = 5
DEFAULT_BATCH_SIZE = 10
DEFAULT_BATCH_COUNT = 3
```

- `DEFAULT_SEARCH_LIMIT`: Maximum number of results to return from vector searches
- `DEFAULT_BATCH_SIZE`: Number of results per batch for scrolling demonstration
- `DEFAULT_BATCH_COUNT`: Number of batches to retrieve for scrolling demonstration

## Runtime Configuration

The demo application accepts command line arguments to override default settings:

```bash
python src/run_demo.py --host localhost --port 6333 --points 2000
```

Available arguments:

- `--host`: Qdrant server hostname or IP address
- `--port`: Qdrant server port
- `--points`: Number of random points to generate and insert

## Scaling Configuration

To scale the cluster, you can modify the `docker-compose.yml` file to add more nodes:

```yaml
qdrant_node4:
  image: qdrant/qdrant:v1.6.1
  container_name: qdrant_node4
  volumes:
    - ./data/node4:/qdrant/storage
  depends_on:
    - qdrant_node1
  environment:
    QDRANT__CLUSTER__ENABLED: "true"
    QDRANT__LOG_LEVEL: "INFO"
  command: "./qdrant --bootstrap http://qdrant_node1:6335 --uri http://qdrant_node4:6335"
```

Make sure to add any new nodes to the Prometheus configuration as well:

```yaml
scrape_configs:
  - job_name: 'qdrant'
    static_configs:
      - targets: ['qdrant_node1:6333', 'qdrant_node2:6333', 'qdrant_node3:6333', 'qdrant_node4:6333']
```

## Production Considerations

For production deployments, consider these additional configuration options:

### Memory and CPU Allocation

Limit and reserve resources for each container:

```yaml
qdrant_node1:
  # ... other configuration ...
  deploy:
    resources:
      limits:
        cpus: '2'
        memory: 4G
      reservations:
        cpus: '1'
        memory: 2G
```

### Authentication

Enable Qdrant authentication in a production environment:

```yaml
environment:
  QDRANT__SERVICE__API_KEY: "your-secure-api-key"
```

### Network Security

For production, use a dedicated Docker network:

```yaml
networks:
  qdrant_network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.28.0.0/16
```

Apply this network to all services:

```yaml
qdrant_node1:
  # ... other configuration ...
  networks:
    - qdrant_network
``` 