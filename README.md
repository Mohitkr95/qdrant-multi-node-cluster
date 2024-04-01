# Scalable Qdrant Distributed Deployment

This project is a demonstration of deploying Qdrant, a high-performance vector database, in a distributed manner. By leveraging Docker Compose, we set up a scalable architecture that consists of multiple Qdrant nodes, ensuring high availability and efficient load distribution for vector search operations.

<p align="center">
  <img src="https://qdrant.tech/images/logo_with_text.svg">
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

## Setup Instructions

### 1. Preparing the Deployment

Clone the repository and install the necessary dependencies:

```bash
git clone https://github.com/Mohitkr95/qdrant-multi-node-cluster.git
cd qdrant-multi-node-cluster
pip install -r requirements.txt
```

### 2. Launching the Qdrant Nodes

Initiate the deployment of the Qdrant nodes using Docker Compose:

```bash
docker-compose up -d
```

This command spins up the configured number of Qdrant nodes, setting up a distributed vector search environment.

## Running the Client Application

To interact with the distributed Qdrant database, run the `main.py` script:

```bash
python main.py
```

This demonstrates essential database operations, tailored to a distributed setup, including data sharding and replication strategies.

## License

This project is licensed under the MIT License. See the LICENSE file for full details.
