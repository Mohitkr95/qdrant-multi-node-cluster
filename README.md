# Scalable Qdrant Distributed Deployment

This project is a demonstration of deploying Qdrant, a high-performance vector database, in a distributed manner. By leveraging Docker Compose, we set up a scalable architecture that consists of multiple Qdrant nodes, ensuring high availability and efficient load distribution for vector search operations.

<p align="center">
  <img src="https://dbdb.io/media/logos/qdrant.svg">
</p>

## Key Features

- **Scalable Multi-Node Setup:** Deploys multiple instances of Qdrant, each running in its own Docker container, to form a robust, distributed vector database.
- **Customizable Sharding and Replication:** Features advanced configuration options for sharding and replication, optimizing data distribution and search efficiency across nodes.
- **Python Client for Database Operations:** Includes a Python script that demonstrates how to interact with the distributed Qdrant setup, performing operations such as creating collections, managing shard keys, and inserting vector data.

## Prerequisites

- Docker and Docker Compose must be installed on your system.
- Python 3.8 or newer for executing the client script.

## Deployment Configuration

### Number of Nodes

This setup is configured to deploy **4 Qdrant nodes**. Each node serves as a separate instance within the distributed database system, enhancing redundancy and query processing capabilities.

### Configuring Nodes

The deployment of Qdrant nodes is managed through a `docker-compose.yml` file, which specifies the container setup, network configurations, and environment variables for each node. This file is crafted to ensure optimal performance and scalability of the database.

### Features and Parameters

- **Sharding:** The database utilizes custom sharding to distribute data evenly across nodes, enhancing query performance and scalability. Sharding parameters can be adjusted based on dataset size and query load.
- **Replication:** To ensure data availability and fault tolerance, replication can be configured across the nodes. This project sets the groundwork for such configurations, highlighting how Qdrant supports distributed data management.
- **Resource Allocation:** Each node's resources (CPU and memory limits) can be customized in the `docker-compose.yml` file, allowing for tailored deployment based on the available infrastructure.

## Project Structure

The project is organized as follows:

```
qdrant-multi-node-cluster/
├── config/                    # Configuration files
│   ├── grafana.json           # Grafana dashboard configuration
│   └── prometheus.yml         # Prometheus configuration
├── deployments/               # Deployment files
│   └── docker/                # Docker-related files
│       └── docker-compose.yml # Docker Compose configuration
├── src/                       # Source code
│   ├── qdrant_demo/           # Main package
│   │   ├── config/            # Configuration settings
│   │   │   ├── __init__.py
│   │   │   └── settings.py    # Configuration parameters
│   │   ├── core/              # Core functionality
│   │   │   ├── __init__.py
│   │   │   └── cluster_demo.py # Main demo class
│   │   ├── utils/             # Utility functions
│   │   │   ├── __init__.py
│   │   │   └── data_generator.py # Data generation utilities
│   │   └── __init__.py
│   └── run_demo.py            # Main entry point
├── tests/                     # Test files
├── LICENSE
├── README.md
├── requirements.txt
└── setup.py                   # Package setup file
```

## Setup Instructions

### 1. Preparing the Deployment

Clone the repository and install the necessary dependencies:

```bash
git clone https://github.com/Mohitkr95/qdrant-multi-node-cluster.git
cd qdrant-multi-node-cluster
pip install -e .
```

### 2. Launching the Qdrant Nodes

Initiate the deployment of the Qdrant nodes using Docker Compose:

```bash
cd deployments/docker
docker-compose up -d
```

This command spins up the configured number of Qdrant nodes, setting up a distributed vector search environment.

## Running the Client Application

To interact with the distributed Qdrant database, run the demo script:

```bash
# Run with default settings
python src/run_demo.py

# Run with custom settings
python src/run_demo.py --host localhost --port 6333 --points 2000
```

## Monitoring and Visualization with Prometheus and Grafana

This project also integrates Prometheus for monitoring and Grafana for visualization, enhancing the observability of the distributed Qdrant deployment directly within the Docker Compose environment.

### Prometheus Configuration

Prometheus is configured to automatically scrape metrics from the Qdrant nodes. This is achieved by mounting a custom `prometheus.yml` configuration file into the Prometheus container, specifying the targets and metrics to collect.

To add Prometheus to your deployment:

1. Prometheus is included as a service in the `docker-compose.yml` file. Ensure the `prometheus.yml` file is correctly configured to scrape metrics from your Qdrant nodes.
2. Launch Prometheus along with your services using Docker Compose:
   ```bash
   docker-compose up -d prometheus
   ```
3. Access Prometheus UI by navigating to `http://localhost:9090`.

### Grafana Dashboard

Grafana is set up to visualize the metrics collected by Prometheus. A volume is created for Grafana data persistence, and initial login credentials are configured through environment variables.

To use the Grafana dashboard:

1. Grafana is included as a service in the `docker-compose.yml` file and depends on Prometheus being up and running.
2. Start Grafana along with your services:
   ```bash
   docker-compose up -d grafana
   ```
3. Access the Grafana UI by navigating to `http://localhost:3000`. Login with the default credentials (admin/admin) or as specified in the `docker-compose.yml`.
4. Connect Grafana to the Prometheus data source by specifying Prometheus's URL (`http://prometheus:9090`) in the data source settings.
5. Import the `grafana.json` dashboard file to visualize the Qdrant metrics.

This setup enables you to monitor the health and performance of your Qdrant deployment seamlessly, utilizing Docker Compose for an integrated monitoring and visualization solution.

## License

This project is licensed under the MIT License. See the LICENSE file for full details.
