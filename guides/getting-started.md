# Getting Started

This guide will help you set up the Qdrant Multi-Node Cluster project on your local environment. Follow these step-by-step instructions to get a fully functional distributed vector database running with monitoring capabilities.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker** (version 20.10.0 or higher) and **Docker Compose** (version 2.0.0 or higher)
- **Python** (version 3.8 or higher)
- **pip** (Python package manager)
- **git** (for cloning the repository)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Mohitkr95/qdrant-multi-node-cluster.git
cd qdrant-multi-node-cluster
```

### 2. Set Up Python Environment

It's recommended to use a virtual environment:

```bash
# Create a virtual environment
python -m venv env

# Activate the virtual environment
# On Windows:
env\Scripts\activate
# On macOS/Linux:
source env/bin/activate

# Install the package and dependencies
pip install -e .
```

This will install all required dependencies, including:
- qdrant-client==1.6.1
- numpy==1.24.3
- rich==13.6.0

## Deploying the Qdrant Cluster

### 1. Using Docker Compose

The project includes a pre-configured Docker Compose file for easy deployment:

```bash
# Navigate to the Docker deployment directory
cd deployments/docker

# Launch the cluster
docker-compose up -d
```

This command will start:
- 3 Qdrant nodes in cluster mode
- Prometheus for metrics collection
- Grafana for visualization

### 2. Verify Deployment

Check if all containers are running:

```bash
docker-compose ps
```

You should see all services in the "Up" state.

## Accessing the Services

After successful deployment, you can access:

- **Qdrant API** at `http://localhost:6333`
- **Prometheus** at `http://localhost:9090`
- **Grafana** at `http://localhost:3000` (default login: admin/admin)

## Running the Demo Application

The project includes a demonstration application that shows how to interact with the Qdrant cluster:

```bash
# Run the demo with default settings
python src/run_demo.py

# Run with custom settings
python src/run_demo.py --host localhost --port 6333 --points 2000
```

This will:
1. Create a collection with appropriate sharding configuration
2. Insert vector data with metadata
3. Demonstrate various search operations
4. Showcase scrolling pagination for large result sets
5. Display collection statistics

## What's Next?

Now that you have a running Qdrant cluster, explore the following resources:

- Read the [Architecture Overview](architecture.md) to understand the system design
- Learn about [Configuration Options](configuration.md) to customize your deployment
- Study the [API Reference](../api/reference.md) for detailed information about available functions
- Check the [Performance Tuning](performance.md) guide for optimization tips

## Troubleshooting

If you encounter any issues during setup:

1. Ensure all required ports (6333, 9090, 3000) are available
2. Check Docker container logs for errors: `docker-compose logs qdrant_node1`
3. Verify network connectivity between containers
4. Consult the [Troubleshooting Guide](troubleshooting.md) for common issues

For additional help, [open an issue](https://github.com/Mohitkr95/qdrant-multi-node-cluster/issues) on the GitHub repository. 